import subprocess


class GetPods:

    def getPods(self):

        pods = []
        output = subprocess.Popen(["kubectl", "get", "pods", "-n", "sock-shop", "--no-headers",
                                            "--field-selector=status.phase=Running", "-o",
                                            "custom-columns=:metadata.name"], stdout=subprocess.PIPE)
        for line in output.stdout.readlines():
            line = line.decode().strip('\n')
            pods.append(line)

        return pods

    def getContainers(self, podName):
        containers = []
        output = subprocess.Popen(["kubectl", "describe", "pod/"+podName, "-n", "sock-shop"], stdout=subprocess.PIPE)
        for line in output.stdout.readlines():
            line = line.decode().strip('\n')
            print(line)
            containers.append(line)

        return containers
