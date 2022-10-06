from cmath import pi
import kubernetes.client as k8s_client
import kubernetes.config as k8s_config
from .const import CRD_GROUP, CRD_PLURAL, CRD_VERSION


def delete_crd(CRD_OBJECT_NAMESPACE, CRD_OBJECT_NAME):
    try:
        k8s_config.load_incluster_config()
    except:
        k8s_config.load_kube_config()

    with k8s_client.ApiClient() as api_client:
        api_instance = k8s_client.CustomObjectsApi(api_client)
        try:
            crd = api_instance.delete_namespaced_custom_object(
                CRD_GROUP,
                CRD_VERSION,
                CRD_OBJECT_NAMESPACE,
                CRD_PLURAL,
                CRD_OBJECT_NAME,
            )
            print("crd is deleted ")


        except k8s_client.rest.ApiException as e:
            if e.status == 404:  # if the CRD dosen't exists the K8s API will respond with a 404 Conflict
                print("CRD dosen't exists")
                return
            else:
                raise e
