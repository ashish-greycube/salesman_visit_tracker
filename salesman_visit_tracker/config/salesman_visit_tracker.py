from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
    config = [
        {
            "label": _("Documents"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Customer Visit Plan",
                    "description": _("Customer Visit Plan"),
                },
                {
                    "type": "doctype",
                    "name": "Customer Visit",
                    "description": _("Customer Visit"),
                },
            ],
        },
        {
            "label": _("Setup"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Salesman Visit Tracker Settings",
                    "description": _("Salesman Visit Tracker Settings"),
                },
            ],
        },
    ]
    return config
