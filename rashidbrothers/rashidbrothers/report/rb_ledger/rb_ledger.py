# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
import frappe
from frappe import _


def execute(filters=None):
    if not filters:
        filters = {}
    data = []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def decimal_format(value, decimals):
    formatted_value = "{:.{}f}".format(value, decimals)
    return formatted_value


def get_columns():
    columns = [
        {
            "label": _("DATE"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Voucher"),
            "fieldname": "voucher_no",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("VEHICLE"),
            "fieldname": "vehicle",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("STATION"),
            "fieldname": "station",
            "fieldtype": "Data",
            "width": 100
        },

        {
            "label": _("CNT SIZE"),
            "fieldname": "cnt_size",
            "fieldtype": "data",
            "width": 100
        },
        {
            "label": _("BILTY FR"),
            "fieldname": "bilty_fr",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("FREIGHT RCVD."),
            "fieldname": "freight_rcvd",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("VEHICLE FR"),
            "fieldname": "vehicle_fr",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("COMISION"),
            "fieldname": "commission",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("KATTOTI"),
            "fieldname": "kattoti",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("MT CHR"),
            "fieldname": "mt_chr",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("CUSTOM"),
            "fieldname": "custom",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("DETAIN"),
            "fieldname": "detain",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("EXTRA"),
            "fieldname": "extra",
            "fieldtype": "Currency",
            "width": 100
        },

        {
            "label": _("TOTAL"),
            "fieldname": "total",
            "fieldtype": "Currency",
            "width": 100,
            "default": 0
        },
        {
            "label": _("DEBIT"),
            "fieldname": "debit",
            "fieldtype": "Currency",
            "width": 100,
            "default":0
        },
        {
            "label": _("BALANCE"),
            "fieldname": "balance",
            "fieldtype": "Currency",
            "width": 100
        }

    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []
    party = None
    if doctype == 'Sales Invoice':
        party = 'broker'
    else:
        party = 'party'

    if filters.get("from_date"):
        conditions.append(f"`tab{doctype}`.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"`tab{doctype}`.posting_date <= %(to_date)s")
    if filters.get("supplier"):
        conditions.append(f"`tab{doctype}`.{party} = %(supplier)s")

    conditions.append(f"`tab{doctype}`.docstatus = 1")  # Include only submitted documents

    return " AND ".join(conditions)


def get_data(filters):
    data = []
    jea = []
    diff = 0
    balance = 0
    si_query = """
            SELECT 
                `tabSales Invoice`.posting_date AS date,
                `tabSales Invoice`.vehicle_no AS vehicle,
                `tabSales Invoice`.to_location AS station,
                `tabSales Invoice`.container_size AS cnt_size,
                `tabSales Invoice`.paid_to_broker AS freight_rcvd,
                `tabSales Invoice`.vehicle_freight AS vehicle_fr,
                `tabSales Invoice`.grand_total - `tabSales Invoice`.vehicle_freight AS commission,
                `tabSales Invoice`.grand_total -  `tabSales Invoice`.paid_to_broker AS kattoti,
                `tabSales Invoice`.empty_container AS mt_chr,
                `tabSales Invoice`.custom_charges AS custom,
                `tabSales Invoice`.daily_expense AS detain,
                `tabSales Invoice`.service_charges AS extra,
                `tabSales Invoice`.grand_total AS bilty_fr,
                `tabSales Invoice`.paid_to_broker - (`tabSales Invoice`.service_charges + `tabSales Invoice`.daily_expense + `tabSales Invoice`.custom_charges + `tabSales Invoice`.empty_container + `tabSales Invoice`.vehicle_freight) AS total   
            FROM 
                `tabSales Invoice`
            WHERE 
                 {conditions}
            """.format(conditions=get_conditions(filters, "Sales Invoice"))

    je_entry = """
                SELECT 
                    `tabGL Entry`.posting_date,
                    `tabGL Entry`.debit,   
                    `tabGL Entry`.credit ,
                    `tabGL Entry`.voucher_no 
                      
                FROM 
                    `tabGL Entry`
                WHERE 
                     {conditions}
                """.format(conditions=get_conditions(filters, "GL Entry"))

    si_result = frappe.db.sql(si_query, filters, as_dict=1)
    je_result = frappe.db.sql(je_entry, filters, as_dict=1)
    data.extend(si_result)
    # add Journal Entry
    for je in je_result:
        jea.append({'date': je.posting_date, 'debit': je.debit, 'credit': je.credit,'voucher_no': je.voucher_no})
    data.extend(jea)
    # calculate running balance and difference of debit and credit

    for dt in data:
        balance = dt.get('total', 0) + (balance + dt.get('debit', 0))
        dt['balance'] = balance

    return data
