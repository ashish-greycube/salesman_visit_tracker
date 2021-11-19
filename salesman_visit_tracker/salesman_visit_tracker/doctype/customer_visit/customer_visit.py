# -*- coding: utf-8 -*-
# Copyright (c) 2021, Greycube and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
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
                    settings = frappe.db.get_singles_dict(
                        "Salesman Visit Tracker Settings"
                    )
                    if settings and settings.get("max_distance_from_client_location"):
                        max_distance = cint(settings.max_distance_from_client_location)
                        self.set_onload(
                            "max_distance_from_client_location", max_distance
                        )
                    break

    def validate_from_to_time(self):
        from frappe.utils import time_diff_in_seconds

        if self.from_time and cint(
            frappe.db.get_value("Customer", self.customer, "validate_in_time_cf")
        ):
            if time_diff_in_seconds(str(self.from_time), frappe.utils.nowtime()) > 0:
                frappe.throw(
                    _("Cannot save customer visit before {0}").format(self.from_time)
                )

        if self.to_time and cint(
            frappe.db.get_value("Customer", self.customer, "validate_out_time_cf")
        ):
            if time_diff_in_seconds(str(self.to_time), frappe.utils.nowtime()) < 0:
                frappe.throw(
                    _("Cannot save customer visit after {0}").format(self.to_time)
                )

    def on_submit(self):
        if not self.status in ["Completed", "Cancelled"]:
            frappe.throw(
                _(
                    "Invalid status {0}. Can submit Visit only when status is Completed or Cancelled."
                ).format(frappe.bold(self.status))
            )

        if not self.actual_date and self.status in ["Completed"]:
            self.validate_from_to_time()
            self.db_set("actual_date", frappe.utils.nowdate())
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
