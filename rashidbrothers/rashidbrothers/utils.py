from datetime import date

import frappe


@frappe.whitelist()
def journal_entry_broker_payable(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry_broker_payable_done:
        # master data-----------------
        voucher_type = "Journal Entry"
        posting_date = date.today()
        vehicle_no = source_name.vehicle_no
        from_location = source_name.from_location
        to_location = source_name.to_location
        user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
        entry_nature = "Broker Payable Entry"
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
            je.entry_nature = entry_nature
            je.bilty_no = source_name.bilty_no
            je.to_location = to_location
            je.vehicle_no = vehicle_no
            je.paid_to_broker = source_name.paid_to_broker
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

        source_name.journal_entry_broker_payable_done = 1
        source_name.save()
    else:
        frappe.throw("Journal Entry For Broker Payable already created")


@frappe.whitelist()
def journal_entry_broker_payment(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry_broker_payment_done:
        if not source_name.paid_to_broker <= 0:
            # master data-----------------
            voucher_type = "Journal Entry"
            posting_date = date.today()
            vehicle_no = source_name.vehicle_no
            from_location = source_name.from_location
            to_location = source_name.to_location
            user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
            entry_nature = "Broker Payment Entry"
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
                je.entry_nature = entry_nature
                je.bilty_no = source_name.bilty_no
                je.to_location = to_location
                je.vehicle_no = vehicle_no
                je.paid_to_broker = source_name.paid_to_broker
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

            source_name.journal_entry_broker_payment_done = 1
            source_name.save()
        else:
            frappe.throw("Paid to broker can not be 0 or less")
    else:
        frappe.throw("Journal Entry For Broker Payment already created")


@frappe.whitelist()
def journal_entry_service_charges(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry_service_charges_done:
        if not source_name.service_charges <= 0:
            # master data-----------------
            voucher_type = "Journal Entry"
            posting_date = date.today()
            vehicle_no = source_name.vehicle_no
            from_location = source_name.from_location
            to_location = source_name.to_location
            user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
            entry_nature = "Service Charges Entry"
            # detail data-------------------
            # for credit
            credit_account = "Creditors - RB"
            party_type = "Supplier"
            party = source_name.broker
            credit = source_name.service_charges
            # for debit
            debit_account = "Cost of Goods Sold - RB"
            debit = source_name.service_charges
            try:
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = voucher_type
                je.posting_date = posting_date
                je.user_remark = user_remark
                je.sales_invoice_id = source_name.name
                je.entry_nature = entry_nature
                je.bilty_no = source_name.bilty_no
                je.to_location = to_location
                je.vehicle_no = vehicle_no
                je.paid_to_broker = source_name.paid_to_broker
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

            source_name.journal_entry_service_charges_done = 1
            source_name.save()
        else:
            frappe.throw("Service charges can not be 0 or less")
    else:
        frappe.throw("Journal Entry For Service Charges already created")


@frappe.whitelist()
def journal_entry_empty_container(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry_empty_container_done:
        if not source_name.empty_container <= 0:
            # master data-----------------
            voucher_type = "Journal Entry"
            posting_date = date.today()
            vehicle_no = source_name.vehicle_no
            from_location = source_name.from_location
            to_location = source_name.to_location
            user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
            entry_nature = "Empty Container Entry"
            # detail data-------------------
            # for credit
            credit_account = "Creditors - RB"
            party_type = "Supplier"
            party = source_name.broker
            credit = source_name.empty_container
            # for debit
            debit_account = "Cost of Goods Sold - RB"
            debit = source_name.empty_container
            try:
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = voucher_type
                je.posting_date = posting_date
                je.user_remark = user_remark
                je.sales_invoice_id = source_name.name
                je.entry_nature = entry_nature
                je.bilty_no = source_name.bilty_no
                je.to_location = to_location
                je.vehicle_no = vehicle_no
                je.paid_to_broker = source_name.paid_to_broker
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

            source_name.journal_entry_empty_container_done = 1
            source_name.save()
        else:
            frappe.throw("Empty container can not be 0 or less")
    else:
        frappe.throw("Journal Entry For Empty Container already created")


@frappe.whitelist()
def journal_entry_custom_charges(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry_custom_charges_done:
        if not source_name.custom_charges <= 0:
            # master data-----------------
            voucher_type = "Journal Entry"
            posting_date = date.today()
            vehicle_no = source_name.vehicle_no
            from_location = source_name.from_location
            to_location = source_name.to_location
            user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
            entry_nature = "Custom Charges Entry"
            # detail data-------------------
            # for credit
            credit_account = "Creditors - RB"
            party_type = "Supplier"
            party = source_name.broker
            credit = source_name.custom_charges
            # for debit
            debit_account = "Cost of Goods Sold - RB"
            debit = source_name.custom_charges
            try:
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = voucher_type
                je.posting_date = posting_date
                je.user_remark = user_remark
                je.sales_invoice_id = source_name.name
                je.entry_nature = entry_nature
                je.bilty_no = source_name.bilty_no
                je.to_location = to_location
                je.vehicle_no = vehicle_no
                je.paid_to_broker = source_name.paid_to_broker
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

            source_name.journal_entry_custom_charges_done = 1
            source_name.save()
        else:
            frappe.throw("Custom charges can not be 0 or less")
    else:
        frappe.throw("Journal Entry For Custom Charges already created")


@frappe.whitelist()
def journal_entry_agent_commission(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry_agent_commission_done:
        if not source_name.agent_commission <= 0:
            if source_name.agent:
                # master data-----------------
                voucher_type = "Journal Entry"
                posting_date = date.today()
                vehicle_no = source_name.vehicle_no
                from_location = source_name.from_location
                to_location = source_name.to_location
                user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
                entry_nature = "Agent Commission Entry"
                # detail data-------------------
                # for credit
                credit_account = "Creditors - RB"
                party_type = "Supplier"
                party = source_name.agent
                credit = source_name.agent_commission
                # for debit
                debit_account = "Cost of Goods Sold - RB"
                debit = source_name.agent_commission
                try:
                    je = frappe.new_doc("Journal Entry")
                    je.voucher_type = voucher_type
                    je.posting_date = posting_date
                    je.user_remark = user_remark
                    je.sales_invoice_id = source_name.name
                    je.entry_nature = entry_nature
                    je.bilty_no = source_name.bilty_no
                    je.to_location = to_location
                    je.vehicle_no = vehicle_no
                    je.paid_to_broker = source_name.paid_to_broker
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

                source_name.journal_entry_agent_commission_done = 1
                source_name.save()
            else:
                frappe.throw("Agent Not selected")
        else:
            frappe.throw("Agent commission can not be 0 or less")
    else:
        frappe.throw("Journal Entry For Agent Commission already created")


@frappe.whitelist()
def journal_entry_addon_charges(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry_addon_charges_done:
        if not source_name.addon_charges <= 0:
            # master data-----------------
            voucher_type = "Journal Entry"
            posting_date = date.today()
            vehicle_no = source_name.vehicle_no
            from_location = source_name.from_location
            to_location = source_name.to_location
            user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
            entry_nature = "Addon Charges Entry"
            # detail data-------------------
            # for credit
            credit_account = "Sales - RB"
            credit = source_name.addon_charges
            # for debit
            debit_account = "Debtors - RB"
            debit_party_type = "Customer"
            debit_party = source_name.customer
            debit = source_name.addon_charges
            try:
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = voucher_type
                je.posting_date = posting_date
                je.user_remark = user_remark
                je.sales_invoice_id = source_name.name
                je.entry_nature = entry_nature
                je.bilty_no = source_name.bilty_no
                je.to_location = to_location
                je.vehicle_no = vehicle_no
                je.paid_to_broker = source_name.paid_to_broker
                # credit
                jea_credit = frappe.new_doc("Journal Entry Account")
                jea_credit.account = credit_account
                jea_credit.credit_in_account_currency = credit
                je.accounts.append(jea_credit)
                # debit
                jea_debit = frappe.new_doc("Journal Entry Account")
                jea_debit.account = debit_account
                jea_debit.party_type = debit_party_type
                jea_debit.party = debit_party
                jea_debit.debit_in_account_currency = debit
                je.accounts.append(jea_debit)
                je.submit()
                # return je
            except Exception as error:
                frappe.throw(f"{error}")

            source_name.journal_entry_addon_charges_done = 1
            source_name.save()
        else:
            frappe.throw("Addon Charges can not be 0 or less")
    else:
        frappe.throw("Journal Entry For Addon Charges already created")

@frappe.whitelist()
def journal_entry_daily_expense(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry_daily_expense_done:
        if not source_name.daily_expense <= 0:

            # master data-----------------
            voucher_type = "Journal Entry"
            posting_date = date.today()
            vehicle_no = source_name.vehicle_no
            from_location = source_name.from_location
            to_location = source_name.to_location
            user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
            entry_nature = "Daily Expense Entry"
            # detail data-------------------
            # for credit
            credit_account = "Creditors - RB"
            party_type = "Supplier"
            party = source_name.broker
            credit = source_name.daily_expense
            # for debit
            debit_account = "Cost of Goods Sold - RB"
            debit = source_name.daily_expense
            try:
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = voucher_type
                je.posting_date = posting_date
                je.user_remark = user_remark
                je.sales_invoice_id = source_name.name
                je.entry_nature = entry_nature
                je.bilty_no = source_name.bilty_no
                je.to_location = to_location
                je.vehicle_no = vehicle_no
                je.paid_to_broker = source_name.paid_to_broker
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

            source_name.journal_entry_daily_expense_done = 1
            source_name.save()

        else:
            frappe.throw("Daily Expense can not be 0 or less")
    else:
        frappe.throw("Journal Entry For Daily Expense already created")

@frappe.whitelist()
def journal_entry_addon_daily_expense(source_name):
    source_name = frappe.get_doc("Sales Invoice", source_name)
    if not source_name.journal_entry__addon_daily_expense_done:
        if not source_name.addon_daily_expense <= 0:
            # master data-----------------
            voucher_type = "Journal Entry"
            posting_date = date.today()
            vehicle_no = source_name.vehicle_no
            from_location = source_name.from_location
            to_location = source_name.to_location
            user_remark = f"Vehicle No : {vehicle_no}, From : {from_location}, To : {to_location}"
            entry_nature = "Addon Daily Expense Entry"
            # detail data-------------------
            # for credit
            credit_account = "Sales - RB"
            credit = source_name.addon_daily_expense
            # for debit
            debit_account = "Debtors - RB"
            debit_party_type = "Customer"
            debit_party = source_name.customer
            debit = source_name.addon_daily_expense
            try:
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = voucher_type
                je.posting_date = posting_date
                je.user_remark = user_remark
                je.sales_invoice_id = source_name.name
                je.entry_nature = entry_nature
                je.bilty_no = source_name.bilty_no
                je.to_location = to_location
                je.vehicle_no = vehicle_no
                je.paid_to_broker = source_name.paid_to_broker
                # credit
                jea_credit = frappe.new_doc("Journal Entry Account")
                jea_credit.account = credit_account
                jea_credit.credit_in_account_currency = credit
                je.accounts.append(jea_credit)
                # debit
                jea_debit = frappe.new_doc("Journal Entry Account")
                jea_debit.account = debit_account
                jea_debit.party_type = debit_party_type
                jea_debit.party = debit_party
                jea_debit.debit_in_account_currency = debit
                je.accounts.append(jea_debit)
                je.submit()
                # return je
            except Exception as error:
                frappe.throw(f"{error}")

            source_name.journal_entry__addon_daily_expense_done = 1
            source_name.save()
        else:
            frappe.throw("Addon Daily Expense can not be 0 or less")
    else:
        frappe.throw("Journal Entry For Addon Daily Expense already created")