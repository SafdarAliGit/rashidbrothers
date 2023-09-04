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
            "label": _("Payment"),
            "fieldname": "payment",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("TOTAL"),
            "fieldname": "total",
            "fieldtype": "Currency",
            "width": 100,
            "default":0
        }

    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []
    party = None
    table = ''
    if doctype == 'Sales Invoice':
        party = 'broker'
        table = 'Sales Invoice'
    else:
        party = 'party'
        table = 'Journal Entry Account'

    if filters.get("from_date"):
        conditions.append(f"`tab{doctype}`.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"`tab{doctype}`.posting_date <= %(to_date)s")
    if filters.get("supplier"):
        conditions.append(f"`tab{table}`.{party} = %(supplier)s")

    conditions.append(f"`tab{doctype}`.docstatus = 1")  # Include only submitted documents

    return " AND ".join(conditions)


def get_data(filters):
    data = []
    jea = []
    si_query = """
            SELECT 
                'payment' AS payment,
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
                    `tabJournal Entry`.posting_date,
                    `tabJournal Entry Account`.debit,   
                    `tabJournal Entry Account`.credit   
                FROM 
                    `tabJournal Entry`, `tabJournal Entry Account`
                WHERE 
                     {conditions}
                """.format(conditions=get_conditions(filters, "Journal Entry"))

    si_result = frappe.db.sql(si_query, filters, as_dict=1)
    je_result = frappe.db.sql(je_entry, filters, as_dict=1)
    data.extend(si_result)
    # add Journal Entry
    for je in je_result:
        jea.append({'date': je.posting_date, 'payment': je.credit})
    data.extend(jea)
    return data
