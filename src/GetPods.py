import subprocess

class GetPods:

    def getPods(self):
        pods = []
        output = subprocess.check_output(["kubectl", "get", "pods", "-n", "sock-shop", "--no-headers",
                                          "--field-selector=status.phase=Running", "-o",
                                          "custom-columns=:metadata.name"])
        output = output.decode()
        for line in output:
            print(line)

        output = subprocess.popen(["kubectl", "get", "pods", "-n", "sock-shop", "--no-headers",
                                          "--field-selector=status.phase=Running", "-o",
                                           "custom-columns=:metadata.name"])
        print ("POPEN")
        for line in output.stdout:
            print(line)


        return pods

    def getContainers(podName):
        containers = []
        output = subprocess.Popen(["kubectl", "describe", "pod/"+podName, "-n", "sock-shop"], stdout=subprocess.PIPE)
        output.wait()
        for line in output.stdout.readlines():
            containers.append(line)

        return containers
