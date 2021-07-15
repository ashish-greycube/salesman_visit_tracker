# -*- coding: utf-8 -*-
# Copyright (c) 2021, Greycube and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.utils import cint, cstr
from frappe.model.document import Document
import json


class CustomerVisit(Document):
    def onload(self):
        for d in frappe.db.get_values(
            "Customer",
            self.customer,
            ["is_location_validation_mandatory_cf", "client_location_cf"],
            as_dict=True,
        ):
            if d.is_location_validation_mandatory_cf == "Yes" and d.client_location_cf:
                for f in json.loads(d.client_location_cf).get("features", []):
                    coords = reversed(
                        [
                            cstr(coord)
                            for coord in f.get("geometry", {}).get("coordinates")
                        ]
                    )
                    self.set_onload("client_location_cf", coords)
                    break

    def on_submit(self):
        if not self.actual_date and self.status in [
            "Completed",
        ]:
            self.actual_date = frappe.utils.today()
        for d in frappe.get_all(
            "Customer Visit Plan Detail",
            filters=[["customer_visit_reference_cf", "=", self.name]],
        ):
            frappe.db.set_value(
                "Customer Visit Plan Detail", d.name, "status", self.status
            )

    def on_cancel(self):
        self.status = "Cancelled"

    def before_cancel(self):
        frappe.db.sql(
            """
            update `tabCustomer Visit Plan Detail`
            set customer_visit_reference_cf = null
            where customer_visit_reference_cf = %s""",
            (self.name),
        )
