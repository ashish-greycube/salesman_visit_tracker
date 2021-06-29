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
    ]
    return config
