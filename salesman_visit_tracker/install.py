# -*- coding: utf-8 -*-
# Copyright (c) 2021, greycube.in and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def after_migrate(**args):
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

    custom_fields = {
        "Customer": [
            dict(
                fieldtype="Geolocation",
                fieldname="client_location_cf",
                label="Client Location",
                insert_after="lead_name",
                translatable=0,
                description="Client location for validation of 'Sales Man Visit'",
            ),
            dict(
                fieldtype="Select",
                options="\nYes\nNo",
                fieldname="is_location_validation_mandatory_cf",
                label="Validate Location",
                insert_after="client_location_cf",
                translatable=0,
                description="Validate salesman is within 200m of client location, on saving Customer Visit",
            ),
        ]
    }

    create_custom_fields(custom_fields)