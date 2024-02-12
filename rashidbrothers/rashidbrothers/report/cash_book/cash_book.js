frappe.query_reports["Cash Book"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		  {
            "fieldname": "transaction_types",
            "label": __("Transaction Types"),
            "fieldtype": "Select",
            "options": ["All","Cash Receipt","Cash Payment"],
            "default": ["All"]  // Preselecting "Sales"
        }
	]
};
