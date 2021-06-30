import time
import sys
import os

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.apis import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import urllib3

config.load_incluster_config()

configuration = Configuration()
configuration.verify_ssl = False
configuration.assert_hostname = False
urllib3.disable_warnings()
Configuration.set_default(configuration)

api = core_v1_api.CoreV1Api()
label_selector = os.getenv('POD_LABEL_SECLECTOR')
namespace = os.getenv('POD_NAMESPACE')

resp = api.list_namespaced_pod(namespace=namespace,
                               label_selector=label_selector)

for x in resp.items:
  name = x.spec.hostname

  resp = api.read_namespaced_pod(name=name,
                                 namespace=namespace)

  exec_command = sys.argv[1:]

  resp = stream(api.connect_get_namespaced_pod_exec, name, namespace,
              command=exec_command,
              stderr=True, stdin=False,
              stdout=True, tty=False)