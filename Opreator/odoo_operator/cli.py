from argparse import ArgumentParser
from os import getenv

import kubernetes

from odoo_operator.load_crd import load_crd
from odoo_operator.operators import handle

try:
    kubernetes = kubernetes.config.load_incluster_config()
except:
    kubernetes = kubernetes.config.load_kube_config()

# except kubernetes.config.config_exception.ConfigException:
#     raise RuntimeError(
#         'Can not read Kubernetes cluster configuration.'
#     )


def main():
    """
    Application's entry point.
    Here, application's settings are read from the command line,
    environment variables and CRD. Then, retrieving and processing
    of Kubernetes events are initiated.
    """

    try:
        # specs = load_crd("default", "odoo-instances-1")
        CRD_NAMESPACE = 'default'
        OPERATOR_TIMEOUT = 60*60*60
        handle(CRD_NAMESPACE, OPERATOR_TIMEOUT)

    except KeyboardInterrupt:
        pass

    except Exception as err:
        raise RuntimeError('Oh no! I am dying...') from err


if __name__ == '__main__':
    main()
