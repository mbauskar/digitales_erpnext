import frappe
from frappe.utils import get_fullname

def execute():
	for user_id in frappe.db.sql_list("""select distinct user_id from `tabEmployee`
		where ifnull(user_id, '')!=''
		group by user_id having count(name) > 1"""):
		
		fullname = get_fullname(user_id)
		employee = frappe.db.get_value("Employee", {"employee_name": fullname, "user_id": user_id})
		if employee:
			frappe.db.sql("""update `tabEmployee` set user_id=null
				where user_id=%s and name!=%s""", (user_id, employee))