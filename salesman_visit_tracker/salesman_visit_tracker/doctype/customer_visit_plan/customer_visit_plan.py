# -*- coding: utf-8 -*-
# Copyright (c) 2021, Greycube and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class CustomerVisitPlan(Document):
    # def on_update(self):
    def after_insert(self):
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
                }
            )
            visit.insert()
            print('*//'*100)
            print(visit.name)
            frappe.db.set_value('Customer Visit Plan Detail', d.name, 'customer_visit_reference_cf', visit.name)
        self.reload()
        # frappe.db.commit()
