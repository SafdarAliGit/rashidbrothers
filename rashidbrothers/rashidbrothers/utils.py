from datetime import date

import frappe


@frappe.whitelist()
def journal_entry_of_sale(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry_of_sale_done:
        # master data-----------------
        voucher_type = "Journal Entry"
        posting_date = date.today()
        vehicle_no = source_name.vehicle_no
        from_location = source_name.from_location
        to_location = source_name.to_location
        user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
        # detail data-------------------
        # for credit
        credit_account = "Creditors - RB"
        party_type = "Supplier"
        party = source_name.broker
        if source_name.vehicle_freight <= 0:
            frappe.throw("Vehicle freight can not be 0 or less")
        else:
            credit = source_name.vehicle_freight
        # for debit
        debit_account = "Cost of Goods Sold - RB"
        if source_name.vehicle_freight <= 0:
            frappe.throw("Vehicle freight can not be 0 or less")
        else:
            debit = source_name.vehicle_freight
        try:
            je = frappe.new_doc("Journal Entry")
            je.voucher_type = voucher_type
            je.posting_date = posting_date
            je.user_remark = user_remark
            je.sales_invoice_id = source_name.name
            # credit
            jea_credit = frappe.new_doc("Journal Entry Account")
            jea_credit.account = credit_account
            jea_credit.party_type = party_type
            jea_credit.party = party
            jea_credit.credit_in_account_currency = credit
            je.accounts.append(jea_credit)
            # debit
            jea_debit = frappe.new_doc("Journal Entry Account")
            jea_debit.account = debit_account
            jea_debit.debit_in_account_currency = debit
            je.accounts.append(jea_debit)
            je.submit()
            # return je
        except Exception as error:
            frappe.throw(f"{error}")

        source_name.journal_entry_of_sale_done = 1
        source_name.save()
    else:
        frappe.throw("Journal Entry For Sale already created")


@frappe.whitelist()
def journal_entry_of_purchase(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry_of_purchase_done:
        if not source_name.paid_to_broker <= 0:
            # master data-----------------
            voucher_type = "Journal Entry"
            posting_date = date.today()
            vehicle_no = source_name.vehicle_no
            from_location = source_name.from_location
            to_location = source_name.to_location
            user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
            # detail data-------------------
            # for debit
            debit_account = "Creditors - RB"
            debit_party_type = "Supplier"
            debit_party = source_name.broker
            debit = source_name.paid_to_broker
                # for credit
            credit_account = "Debtors - RB"
            credit_party_type = "Customer"
            credit_party = source_name.customer
            credit = source_name.paid_to_broker
            try:
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = voucher_type
                je.posting_date = posting_date
                je.user_remark = user_remark
                je.sales_invoice_id = source_name.name
                # debit
                jea_debit = frappe.new_doc("Journal Entry Account")
                jea_debit.account = debit_account
                jea_debit.party_type = debit_party_type
                jea_debit.party = debit_party
                jea_debit.debit_in_account_currency = debit
                je.accounts.append(jea_debit)
                # credit
                jea_credit = frappe.new_doc("Journal Entry Account")
                jea_credit.account = credit_account
                jea_credit.party_type = credit_party_type
                jea_credit.party = credit_party
                jea_credit.credit_in_account_currency = credit
                je.accounts.append(jea_credit)
                je.submit()
                # return je
            except Exception as error:
                frappe.throw(f"{error}")

            source_name.journal_entry_of_purchase_done = 1
            source_name.save()
        else:
            frappe.throw("Paid to broker can not be 0 or less")
    else:
        frappe.throw("Journal Entry For Sale already created")
