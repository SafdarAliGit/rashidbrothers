from . import __version__ as app_version

app_name = "rashidbrothers"
app_title = "rashidbrothers"
app_publisher = "Tech Ventures"
app_description = "this is bussiness erp application"
app_email = "safdar211@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
# override_doctype_class = {
#        "Sales Invoice": "rashidbrothers.overrides.sales_invoice_overrides.SalesInvoiceOverrides",
#        "Journal Entry": "rashidbrothers.overrides.journal_entry_overrides.JournalEntryOverrides",
# }
# include js, css files in header of desk.html
app_include_css = "/assets/rashidbrothers/css/rashidbrothers.css"
# app_include_js = "/assets/rashidbrothers/js/rashidbrothers.js"

# include js, css files in header of web template
# web_include_css = "/assets/rashidbrothers/css/rashidbrothers.css"
# web_include_js = "/assets/rashidbrothers/js/rashidbrothers.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "rashidbrothers/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {"Sales Invoice": "public/js/sales_invoice.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "rashidbrothers.utils.jinja_methods",
#	"filters": "rashidbrothers.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "rashidbrothers.install.before_install"
# after_install = "rashidbrothers.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "rashidbrothers.uninstall.before_uninstall"
# after_uninstall = "rashidbrothers.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rashidbrothers.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes



# Document Events.
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"rashidbrothers.tasks.all"
#	],
#	"daily": [
#		"rashidbrothers.tasks.daily"
#	],
#	"hourly": [
#		"rashidbrothers.tasks.hourly"
#	],
#	"weekly": [
#		"rashidbrothers.tasks.weekly"
#	],
#	"monthly": [
#		"rashidbrothers.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "rashidbrothers.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "rashidbrothers.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "rashidbrothers.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["rashidbrothers.utils.before_request"]
# after_request = ["rashidbrothers.utils.after_request"]

# Job Events
# ----------
# before_job = ["rashidbrothers.utils.before_job"]
# after_job = ["rashidbrothers.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"rashidbrothers.auth.validate"
# ]
required_apps = ["erpnext"]