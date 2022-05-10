import time
import AvailabilityGradeCalculation
import ReliabilityGradeCalculation
import PerformanceGradeCalculation
import CorrectnessGradeCalculation
import SecurityGradeCalculation
import schedule
import json
from datetime import datetime


PROMETHEUS = 'http://10.161.2.161:31090/'
SOCKSHOP = 'http://10.161.2.161:30001/'

trustScore = []
date = []

availabilityGradeList = []
reliabilityGradeList = []
performanceGradeList = []
correctnessGradeList = []
securityGradeList = []

availabilityGradeCalculation = AvailabilityGradeCalculation.AvailabilityGradeCalculation(PROMETHEUS)
reliabilityGradeCalculation = ReliabilityGradeCalculation.ReliabilityGradeCalculation(PROMETHEUS)
performanceGradeCalculation = PerformanceGradeCalculation.PerformanceGradeCalculation(PROMETHEUS)
correctnessGradeCalculation = CorrectnessGradeCalculation.CorrectnessGradeCalculation(SOCKSHOP)
securityGradeCalculation = SecurityGradeCalculation.SecurityGradeCalculation()


def trustCalculation():
    availabilityGrade = availabilityGradeCalculation.calculateGrade()
    availabilityWeight = 0.2
    print("AvailabilityGrade: ", availabilityGrade)

    reliabilityGrade = reliabilityGradeCalculation.calculateGrade()
    reliabilityWeight = 0.2
    print("ReliabilityGrade: ", reliabilityGrade)

    performanceGrade = performanceGradeCalculation.calculateGrade()
    performanceWeight = 0.2
    print("PerformanceGrade: ", performanceGrade)

    correctnessGrade = correctnessGradeCalculation.calculateGrade()
    correctnessWeight = 0.2
    print("CorrectnessGrade: ", correctnessGrade)

    securityGrade = securityGradeCalculation.calculateGrade()
    securityWeight = 0.2
    print("SecurityGrade: ", securityGrade)

    trustScore.append(
        (availabilityWeight * availabilityGrade + reliabilityWeight * reliabilityGrade + performanceWeight *
         performanceGrade + correctnessWeight * correctnessGrade + securityWeight * securityGrade))

    date.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    trustScoreDict = [{
        "Timestamp": date,
        "Trustscore": trustScore
    }]

    with open('trustscore.json', 'w') as fp:
        fp.write(json.dumps(trustScoreDict))

    availabilityGradeList.append(availabilityGrade)
    reliabilityGradeList.append(reliabilityGrade)
    performanceGradeList.append(performanceGrade)
    correctnessGradeList.append(correctnessGrade)
    securityGradeList.append(securityGrade)

    parameterScoreDict = [{
            "Timestamp": date,
            "availabilityGrade": availabilityGradeList,
            "reliabilityGrade": reliabilityGradeList,
            "performanceGrade": performanceGradeList,
            "correctnessGrade": correctnessGradeList,
            "securityGrade": securityGradeList
        }]

    with open('parameterscore.json', 'w') as fp:
        fp.write(json.dumps(parameterScoreDict))


    subParameterScoreDict = [{
            "Timestamp": date,
            "availabilityGrade": availabilityGradeList,
            "reliabilityGrade": reliabilityGradeList,
            "performanceGrade": performanceGradeList,
            "correctnessGrade": correctnessGradeList,
            "securityGrade": securityGradeList
        }]

    with open('subparameterscore.json', 'w') as fp:
        fp.write(json.dumps(subParameterScoreDict))


def initialCalculation():
    print("Initial Calculation")
    availabilityGradeCalculation.initialCalculation()
    reliabilityGradeCalculation.initialCalculation()
    performanceGradeCalculation.initialCalculation()
    correctnessGradeCalculation.initialCalculation()
    securityGradeCalculation.initialCalculation()
    trustCalculation()


def update():
    print("Update")
    availabilityGradeCalculation.update()
    reliabilityGradeCalculation.update()
    performanceGradeCalculation.update()
    correctnessGradeCalculation.update()
    trustCalculation()


def dailyUpdate():
    print("Daily Update")
    reliabilityGradeCalculation.dailyUpdate()
    securityGradeCalculation.dailyUpdate()


def main():
    print("Main Call!")

    initialCalculation()
    schedule.every().hour.do(update)
    schedule.every().day.do(dailyUpdate)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
