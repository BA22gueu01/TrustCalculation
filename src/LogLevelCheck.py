import subprocess

class LogLevelCheck:
    print('Check log level for: warning, error and fatal messages')

    def checkLoglevel(self):

        #output = subprocess.check_output(["microk8s.kubectl", "logs", "carts-77b9db4898-27w9m", "--namespace=sock-shop", "--v=1", "|", "grep", "-iE", "'(warning|error|fatal)'", "|", "wc", "-l"])
        output = subprocess.check_output(["kubectl", "logs", "queue-master-6bf76bbfc-4hcwf", "--namespace=sock-shop", "--v=1", "|", "grep", "-iE", "'(warning|error|fatal)'", "|", "wc", "-l"])
        print(output)
        #output = 20
        # to be updated
        if output > 25:
            return -5
        elif 25 == output > 10:
            return 0
        else:
            return 5