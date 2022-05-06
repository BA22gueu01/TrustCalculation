import PrometheusRequest
import numpy

class PerformanceGradeCalculation:

    def __init__(self, prometheus):
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus)
        self.responseTimeGrades = numpy.zeros(24)
        self.responseTimeWeight = 0.4
        self.memoryUsageGrades = numpy.zeros(24)
        self.memoryUsageWeight = 0.2
        self.diskReadGrades = numpy.zeros(24)
        self.diskReadWeight = 0.1
        self.diskWriteGrades = numpy.zeros(24)
        self.diskWriteWeight = 0.1
        self.cpuUsageGrades = numpy.zeros(24)
        self.cpuUsageWeight = 0.2

    def calculateGrade(self):

        return (self.responseTimeWeight * numpy.average(self.responseTimeGrades) + self.memoryUsageWeight * numpy.average(self.memoryUsageGrades)
                + self.diskReadWeight * numpy.average(self.diskReadGrades) + self.diskWriteWeight * numpy.average(self.diskWriteGrades)
                + self.cpuUsageWeight * numpy.average(self.cpuUsageGrades))


    def calculateResponseTimeGrade(self, value):
        responseTime = value[1]
        responseTime = float(responseTime)

        if responseTime > 1:
            grade = -5
        elif responseTime >= 0.5:
            grade = 0
        else:
            grade = 5

        return grade

    def calculateMemoryUsageGrade(self, value):
        memoryUsage = value[1]
        memoryUsage = float(memoryUsage) * 100

        if memoryUsage > 85:
            grade = -5
        elif memoryUsage > 70:
            grade = 0
        else:
            grade = 5
        return grade

    def calculateDiskGrade(self, value):
        diskUsage = value[1]
        # seconds to ms
        diskUsage = float(diskUsage) * 1000

        if diskUsage > 50:
            grade = -5
        elif diskUsage > 25:
            grade = 0
        else:
            grade = 5
        return grade

    def calculateCpuUsageGrade(self, cpuUsage):
        cpuUsage = float(cpuUsage) * 100

        if cpuUsage > 90:
            grade = -5
        elif cpuUsage > 75:
            grade = 0
        else:
            grade = 5
        print("CPU UsageGrade: ", grade)
        self.addNewGrade(grade, self.cpuUsageGrades)

    def addNewGrade(self, newGrade, grades):
        length = len(grades) - 1
        for x in range(length):
            grades[x] = grades[x + 1]
        grades[length] = newGrade

    def update(self):
        responseTimeValues = self.prometheusRequest.makeRequest('response_time')
        grade = 0
        counter = 0
        for x in range(len(responseTimeValues)):
            grade = grade + self.calculateResponseTimeGrade(responseTimeValues[x][1])
            counter = counter + 1
        grade = grade / counter
        self.addNewGrade(grade, self.responseTimeGrades)
        print("Response Time Grade: ", grade)

        memoryUsageValues = self.prometheusRequest.makeRequest('memory_usage')
        grade = 0
        counter = 0
        for x in range(len(memoryUsageValues)):
            grade = grade + self.calculateMemoryUsageGrade(memoryUsageValues[x][1])
            counter = counter + 1
        grade = grade / counter
        self.addNewGrade(grade, self.memoryUsageGrades)
        print("Memory Usage Grade: ", grade)

        diskReadUsageValues = self.prometheusRequest.makeRequest('disk_read')
        grade = 0
        counter = 0
        for x in range(len(diskReadUsageValues)):
            grade = grade + self.calculateDiskGrade(diskReadUsageValues[x][1])
            counter = counter + 1
        grade = grade / counter
        self.addNewGrade(grade, self.diskReadGrades)
        print("Disk Read Grade: ", grade)

        diskWriteUsageValues = self.prometheusRequest.makeRequest('disk_write')
        for x in range(len(diskWriteUsageValues)):
            grade = grade + self.calculateDiskGrade(diskWriteUsageValues[x][1])
            counter = counter + 1
        grade = grade / counter
        self.addNewGrade(grade, self.diskWriteGrades)
        print("Disk Write Grade: ", grade)

        cpuUsageValues = self.prometheusRequest.makeRequest('container_spec_cpu_quota')
        self.calculateCpuUsageGrade(cpuUsageValues[1])

    def initialCalculation(self):
        responseTimeValues = self.prometheusRequest.makeRequest('response_time_history')
        print(responseTimeValues)
        for x in range(len(responseTimeValues[0])):
            grade = 0
            counter = 0
            for y in range(len(responseTimeValues)):
                if x < len(responseTimeValues[y]):
                    grade = grade + self.calculateResponseTimeGrade(responseTimeValues[y][x])
                    counter = counter + 1
            grade = grade / counter
            self.addNewGrade(grade, self.responseTimeGrades)
            print("Response Time Grade: ", grade)

        memoryUsageValues = self.prometheusRequest.makeRequest('memory_usage_history')
        for x in range(len(memoryUsageValues[0])):
            grade = 0
            counter = 0
            for y in range(len(memoryUsageValues)):
                if x < len(memoryUsageValues[y]):
                    grade = grade + self.calculateMemoryUsageGrade(memoryUsageValues[y][x])
                    counter = counter + 1
            grade = grade / counter
            self.addNewGrade(grade, self.memoryUsageGrades)
            print("Memory Usage Grade: ", grade)

        diskReadUsageValues = self.prometheusRequest.makeRequest('disk_read_history')
        self.subGradeCalculation(diskReadUsageValues, self.calculateDiskGrade(), self.diskReadGrades, "Disk Read Grade: ")

        diskWriteUsageValues = self.prometheusRequest.makeRequest('disk_write_history')
        for x in range(len(diskReadUsageValues[0])):
            grade = 0
            counter = 0
            for y in range(len(diskWriteUsageValues)):
                grade = grade + self.calculateDiskGrade(diskWriteUsageValues[y][x])
                counter = counter + 1
            grade = grade / counter
            self.addNewGrade(grade, self.diskWriteGrades)
            print("Disk Write Grade: ", grade)

        cpuUsageValues = self.prometheusRequest.makeRequest('container_spec_cpu_quota_history')
        self.calculateCpuUsageGrade(cpuUsageValues[1])

    def subGradeCalculation(self, values, func, gradeArray, gradeName):
        length = 0
        for value in values:
            if len(value) > length:
                length = len(value)

        for x in range(length):
            grade = 0
            counter = 0
            for y in range(len(values)):
                if x < len(values[y]):
                    grade = grade + func(values[y][x])
                    counter = counter + 1
            grade = grade / counter
            self.addNewGrade(grade, gradeArray)
            print(gradeName, grade)
