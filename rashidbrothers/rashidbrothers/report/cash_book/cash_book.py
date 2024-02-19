# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def decimal_format(value, decimals):
    formatted_value = "{:.{}f}".format(value, decimals)
    return formatted_value


def get_columns():
    columns = [
        {
            "label": _("Voucher Type"),
            "fieldname": "voucher_type",
            "fieldtype": "Link",
            "options": "DocType",
            "width": 120
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Voucher No"),
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 140
        },
        {
            "label": _("Account"),
            "fieldname": "party",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type.party",
            "width": 180
        },
        {
            "label": _("Debit"),
            "fieldname": "debit",
            "fieldtype": "Currency",
            "width": 120
        },

        {
            "label": _("Credit"),
            "fieldname": "credit",
            "fieldtype": "Currency",
            "width": 120
        },

        {
            "label": _("Against"),
            "fieldname": "against",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Remarks"),
            "fieldname": "remarks",
            "fieldtype": "Data",
            "width": 150
        }

    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []

    if filters.get("from_date"):
        conditions.append(f"`tab{doctype}`.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"`tab{doctype}`.posting_date <= %(to_date)s")

    if doctype == "Journal Entry":
        conditions.append("`tabJournal Entry`.is_opening = 0")

    return " AND ".join(conditions)


def get_account_type_from_name(account_name):
    try:
        account_doc = frappe.get_doc("Account", account_name)
        account_type = account_doc.account_type
        return account_type
    except frappe.DoesNotExistError:
        return None


def get_data(filters):
    data = []
    sum_debit_and_credit = """
                    SELECT
                        SUM(CASE WHEN `tabGL Entry`.debit > 0 THEN `tabGL Entry`.debit ELSE 0 END) AS total_debit,
                        SUM(CASE WHEN `tabGL Entry`.credit > 0 THEN `tabGL Entry`.credit ELSE 0 END) AS total_credit
                    FROM
                        `tabGL Entry`
                    WHERE
                        `tabGL Entry`.is_cancelled = 0
                        AND `tabGL Entry`.posting_date < '{start_date}'
                        AND (SELECT `account_type` FROM `tabAccount` WHERE `name` = `tabGL Entry`.account) = 'Cash'
                """.format(start_date=filters.get("from_date"))
    cash_receipt = """SELECT
						`tabGL Entry`.posting_date,
						`tabGL Entry`.account as party,
						`tabGL Entry`.party_type,
						`tabGL Entry`.voucher_no,
						`tabGL Entry`.debit,
						`tabGL Entry`.credit,
						`tabGL Entry`.against,
						`tabGL Entry`.remarks
					FROM
						`tabGL Entry`
					WHERE
						{conditions} AND `tabGL Entry`.is_cancelled = 0
						AND `tabGL Entry`.debit >0
						AND (SELECT `account_type` FROM `tabAccount` WHERE `name` = `tabGL Entry`.account) ='Cash'
					""".format(conditions=get_conditions(filters, "GL Entry"))

    cash_payment = """SELECT
						`tabGL Entry`.posting_date,
						`tabGL Entry`.account as party,
						`tabGL Entry`.party_type,
						`tabGL Entry`.voucher_no,
						`tabGL Entry`.debit,
						`tabGL Entry`.credit,
						`tabGL Entry`.against,
						`tabGL Entry`.remarks
					FROM
						`tabGL Entry`
					WHERE
						{conditions} AND `tabGL Entry`.is_cancelled = 0
						AND `tabGL Entry`.credit >0
						AND (SELECT `account_type` FROM `tabAccount` WHERE `name` = `tabGL Entry`.account) ='Cash'
				""".format(conditions=get_conditions(filters, "GL Entry"))

    sum_debit_and_credit_result = frappe.db.sql(sum_debit_and_credit, as_dict=1)
    cash_receipt_result = frappe.db.sql(cash_receipt, filters, as_dict=1)
    cash_payment_result = frappe.db.sql(cash_payment, filters, as_dict=1)

    # ====================OPENING BALANCE ROW====================#
    opening_balance_dict = [{'voucher_type': '<b>OPENING BALANCE</b>', 'posting_date': '', 'voucher_no': '',
                                 'party': '', 'debit': '', 'credit': '','remarks':''
                                 }]
    opening_balance_dict[0]['debit'] = sum_debit_and_credit_result[0]['total_debit']
    opening_balance_dict[0]['credit'] = sum_debit_and_credit_result[0]['total_credit']
    opening_balance_dict[0]['remarks'] = sum_debit_and_credit_result[0]['total_debit'] - sum_debit_and_credit_result[0]['total_credit']

    # ====================CALCULATING TOTAL IN CASH RECEIVED====================
    cash_receipt_header_dict = [{'voucher_type': '<b><u>Cash Receipt</b></u>', 'posting_date': '', 'voucher_no': '',
                                 'party': '', 'debit': '', 'credit': ''
                                 }]
    cash_receipt_total_dict = {'voucher_type': '<b>Sum</b>', 'posting_date': '-------', 'voucher_no': '-------',
                               'party': '-------', 'debit': None, 'credit': 0,
                               'remarks': '--------------'}
    debit = 0
    for index, cr in enumerate(cash_receipt_result):
        debit += cr.debit
        cash_receipt_result[index][
            'party'] = f"{cash_receipt_result[index]['party']}  {' / ' + cash_receipt_result[index]['party_type'] if cash_receipt_result[index]['party_type'] else ''} {' / ' + cash_receipt_result[index]['party'] if cash_receipt_result[index]['party'] else ''}"

    cash_receipt_total_dict['debit'] = debit
    cash_receipt_result = opening_balance_dict + cash_receipt_header_dict + cash_receipt_result
    cash_receipt_result.append(cash_receipt_total_dict)
    # ====================CALCULATING TOTAL IN CASH RECEIVED END====================

    # ====================CALCULATING TOTAL IN CASH PAID====================
    cash_payment_header_dict = [{'voucher_type': '<b><u>Cash Payment</b></u>', 'posting_date': '', 'voucher_no': '',
                                 'party': '', 'debit': '', 'credit': ''
                                 }]
    cash_payment_total_dict = {'voucher_type': '<b>Sum</b>', 'posting_date': '-------', 'voucher_no': '-------',
                               'party': '-------', 'debit': None, 'credit': 0,
                               'remarks': '--------------'}
    credit = 0
    for index, cr in enumerate(cash_payment_result):
        credit += cr.credit
        cash_payment_result[index][
            'party'] = f"{cash_payment_result[index]['party']}  {' / ' + cash_payment_result[index]['party_type'] if cash_payment_result[index]['party_type'] else ''} {' / ' + cash_payment_result[index]['party'] if cash_payment_result[index]['party'] else ''}"

    cash_payment_total_dict['credit'] = credit
    cash_payment_result =  cash_payment_header_dict + cash_payment_result
    cash_payment_result.append(cash_payment_total_dict)
    # ====================CALCULATING TOTAL IN CASH PAID END====================
    # ====================BALANCE====================
    cash_payment_total_dict = {'voucher_type': '<b>BALANCE</b>', 'posting_date': '', 'voucher_no': '',
                               'party': '', 'debit': debit + sum_debit_and_credit_result[0]['total_debit'], 'credit': credit + sum_debit_and_credit_result[0]['total_credit'],
                               'remarks': f"<b>{(debit + sum_debit_and_credit_result[0]['total_debit']) - (credit + sum_debit_and_credit_result[0]['total_credit'])}</b>"}

    cash_payment_result.append(cash_payment_total_dict)
    # ====================BALANCE END====================

    #
    # ====================TRANSACTION TYPE FILTER====================
    if filters.get('transaction_types') == "All":
        data.extend(cash_receipt_result)
        data.extend(cash_payment_result)
    if 'Cash Receipt' in filters.get('transaction_types'):
        data.extend(cash_receipt_result)
    if 'Cash Payment' in filters.get('transaction_types'):
        data.extend(cash_payment_result)
        # ====================FILTERS END====================

    return data
