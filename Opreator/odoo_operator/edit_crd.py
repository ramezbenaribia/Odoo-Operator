import kubernetes.client as k8s_client
import kubernetes.config as k8s_config

from .const import CRD_GROUP, CRD_PLURAL, CRD_VERSION


__all__ = [
    'edit_crd',
]


def edit_crd(CRD_OBJECT_NAMESPACE,CRD_OBJECT_NAME, CRD_OBJECT_BODY):
    try:
        k8s_config.load_incluster_config()
    except:
        k8s_config.load_kube_config()
    api_client = k8s_client.ApiClient()
    api_instance = k8s_client.CustomObjectsApi(api_client)
    try:
        crd = api_instance.patch_namespaced_custom_object(
            CRD_GROUP,
            CRD_VERSION,
            CRD_OBJECT_NAMESPACE,
            CRD_PLURAL,
            CRD_OBJECT_NAME,
            CRD_OBJECT_BODY
        )
        print("crd is edited ")
        return crd
        # return {x: crd[x] for x in ('ruleType', 'namespace',  'branch', 'repository')}

    except k8s_client.rest.ApiException as e:
        if e.status == 404:  # if the CRD dosen't exists the K8s API will respond with a 404 Conflict
            print("CRD Object Dosen't exists")
            return
        else:
            raise e
