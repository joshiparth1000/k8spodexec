import sys
import os

from kubernetes import config, client
from kubernetes.stream import stream

config.load_incluster_config()

api = client.CoreV1Api()
label_selector = os.getenv('POD_LABEL_SECLECTOR')
namespace = os.getenv('POD_NAMESPACE')

resp = api.list_namespaced_pod(namespace=namespace, label_selector=label_selector)

for x in resp.items:
  name = x.metadata.name

  resp = api.read_namespaced_pod(name=name, namespace=namespace)

  exec_command = sys.argv[1:]

  resp = stream(api.connect_get_namespaced_pod_exec, name, namespace,
              command=exec_command,
              stderr=True, stdin=False,
              stdout=True, tty=False)

  print("Response: " + resp)