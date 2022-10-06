
from odoo_operator.create_crd import create_crd
from odoo_operator.delete_crd import delete_crd
from odoo_operator.edit_crd import edit_crd


def create_instance(body):

    CRD_OBJECT_NAME = "odoo-instances-" + body["fullname"]

    CRD_OBJECT_BODY = {
        "apiVersion": "operators.com/v1",
        "kind": "OdooRule",
        "metadata": {
            "name": CRD_OBJECT_NAME,
        },
    }
    CRD_OBJECT_BODY.update(body)

    crd = create_crd("default", CRD_OBJECT_BODY)


def edit_instance(body):
    CRD_OBJECT_NAME = "odoo-instances-" + body["fullname"]

    CRD_OBJECT_BODY = {
        "apiVersion": "operators.com/v1",
        "kind": "OdooRule",
        "metadata": {
            "name": CRD_OBJECT_NAME,
        },
    }
    CRD_OBJECT_BODY.update(body)

    crd = edit_crd("default", CRD_OBJECT_NAME, CRD_OBJECT_BODY)


def delete_instance(fullname):
    CRD_OBJECT_NAME = "odoo-instances-" + fullname
    crd = delete_crd("default", CRD_OBJECT_NAME)
