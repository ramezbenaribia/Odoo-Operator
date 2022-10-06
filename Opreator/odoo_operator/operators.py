from functools import partial
from avionix import ChartBuilder, ChartDependency, ChartInfo, Values

import os


import kubernetes.client as k8s_client
import kubernetes.config as k8s_config
import kubernetes.watch as k8s_watch

from .const import ALLOWED_EVENT_TYPES, CREATE_TYPES_MAP, \
    LIST_TYPES_MAP, CRD_GROUP, CRD_VERSION, CRD_PLURAL

__all__ = [
    'handle',
]


def handle(CRD_NAMESPACE, OPERATOR_TIMEOUT):
    """
    The main method to initiate events processing via odoo_operator.
    """

    try:
        k8s_config.load_incluster_config()

    except:
        k8s_config.load_kube_config()

    # v1 = kubernetes.client.CoreV1Api()
    api_client = k8s_client.ApiClient()
    api_instance = k8s_client.CustomObjectsApi(api_client)

    # Get the method to watch the objects
    # method = getattr(v1, LIST_TYPES_MAP[specs['branch']])
    method = getattr(api_instance, "list_namespaced_custom_object")
    func = partial(method, CRD_GROUP, CRD_VERSION, CRD_NAMESPACE, CRD_PLURAL)
    # func = partial(method)

    w = k8s_watch.Watch()
    for event in w.stream(func, _request_timeout=OPERATOR_TIMEOUT):
        handle_event(event)


def handle_event(event):
    """
    The method for processing one Kubernetes event.
    """
    # if event['type'] not in ALLOWED_EVENT_TYPES:
    #     return
    type_ = event['type']

    object_ = event['object']

    call_operator(object_, type_)


def call_operator(body, type):
    PATH = os.getcwd() + "/mychart"
    HELM_NAME = "odoo-instances-" + body['fullname']

    # we don't need the metadata field nor apiVersion for the values of our helm chart
    del body["metadata"]
    del body["apiVersion"]
    body["helmName"] = HELM_NAME
    body["replicaCount"] = 1
    values = Values(
        {
            "mychart": body
        }
    )

    builder = ChartBuilder(
        ChartInfo(
            api_version="3.2.4",
            name=HELM_NAME,
            version="0.1.0",
            app_version="v1",

            dependencies=[
                ChartDependency(
                    name="mychart",
                    version="0.1.0",
                    repository="file:///" + PATH,
                    local_repo_name="mychart",
                    is_local=True,
                ),
            ],
        ),

        [],
        values=values,
        keep_chart=True,
    )

    if not builder.is_installed:
        builder.install_chart({"dependency-update": None})
    else:
        if type == 'DELETED':
            builder.uninstall_chart({})
        else:
            builder.upgrade_chart({"dependency-update": None})
