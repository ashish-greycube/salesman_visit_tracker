# -*- coding: utf-8 -*-
# Copyright (c) 2021, Greycube and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class CustomerVisitPlan(Document):
    def on_submit(self):
        for d in self.customer_visit_plan_detail:
            visit = frappe.new_doc("Customer Visit")
            visit.update(
                {
                    "planned_date": d.plan_date,
                    "plan_reference": self.name,
                    "customer": d.customer,
                    "customer_name": d.customer_name,
                    "contact": d.contact,
                    "sales_partner": d.sales_partner,
                    "status": "Open",
                    "from_time": d.from_time,
                    "to_time": d.to_time,
                }
            )
            visit.insert()
            frappe.db.set_value(
                "Customer Visit Plan Detail",
                d.name,
                "customer_visit_reference_cf",
                visit.name,
            )
        self.reload()


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_customer_contacts(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        """select `tabContact`.name from `tabContact`, `tabDynamic Link`
		where `tabDynamic Link`.link_doctype = 'Customer' and (`tabDynamic Link`.link_name=%(name)s
		and `tabDynamic Link`.link_name like %(txt)s) and `tabContact`.name = `tabDynamic Link`.parent
		limit %(start)s, %(page_len)s""",
        {
            "start": start,
            "page_len": page_len,
            "txt": "%%%s%%" % txt,
            "name": filters.get("customer"),
        },
        debug=True,
    )
