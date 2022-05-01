import subprocess
import GetPods

class LogLevelCheck:

    def getLogLevelGrade(self):
        getPods = GetPods.GetPods()
        pods = getPods.getPods()
        grade = 0
        countPods = 0

        for pod in pods:
            countContainers = 0
            podGrade = 0
            containers = getPods.getContainers(pod)

            for container in containers:
                podGrade = podGrade + self.checkLoglevel(pod, container)
                countContainers = countContainers + 1

            grade = grade + podGrade/countContainers
            countPods = countPods + 1

        return grade/countPods


    def checkLoglevel(self, podName, containerName):

        print("LogLevelCheck for Pod: " + podName + " & container: " + containerName)

        try:
            output = subprocess.check_output(["kubectl", "logs", podName, "--container", containerName,
                                              "--namespace=sock-shop", "--v=1"])
            output = output.decode()
            logLevels = ['warn', 'warning', 'error', 'critical', 'alert', 'fatal', 'emergency']
            counter = 0

            # https://pencilprogrammer.com/check-multiple-substrings-python/
            for x in logLevels:
                if x.lower() in output.lower():
                    counter += 1
        except Exception as e:
            counter = 25
            print(e)

        # to be updated
        if counter > 3000:
            return -5
        elif 3000 == counter > 1000:
            return 0
        else:
            return 5
