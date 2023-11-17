import os
import matplotlib.pyplot as plt

# Number of cycles to skip at the start
PERIODS_TO_SKIP = 5

# Whether to use interpolation to determine zero locations
# (if false, uses the first positive data point)
INTERPOLATION_ENABLED = True

# Returns the x-coordinate of the x-intercept of the line
# given by (a,b) and (c,d).
def getZeroX(a, b, c, d):
    if INTERPOLATION_ENABLED:
        return b * (a - c) / (d - b) + a
    else:
        return c


def avg(array):
    return sum(array) / len(array)


def stdev(array):
    mean = avg(array)
    return (sum([(x - mean) ** 2 for x in array]) / (len(array) - 1)) ** 0.5


def stderr(array):
    return stdev(array) / (len(array) ** 0.5)


def rawPeriodList(csvFile):
    with open(csvFile) as file:
        data = file.read().split("\n")[1:-1]

    data = [[float(e) for e in x.split(",")] for x in data]

    prevPoint = data[0]
    prevZeroTime = None
    measuredPeriods = []

    for currPoint in data:
        currZeroTime = None

        if currPoint[1] == 0:
            currZeroTime = currPoint[0]
        elif prevPoint[1] < 0 and currPoint[1] > 0:
            currZeroTime = getZeroX(prevPoint[0], prevPoint[1],
                                    currPoint[0], currPoint[1])

        if currZeroTime != None:
            if prevZeroTime != None:
                measuredPeriods.append(currZeroTime - prevZeroTime)
            prevZeroTime = currZeroTime

        prevPoint = currPoint

    return measuredPeriods


def plotRawPeriods(csvFile):
    measuredPeriods = rawPeriodList(csvFile)
    plt.plot(range(len(measuredPeriods)), measuredPeriods, "b.")
    plt.xlabel("Observation Index")
    plt.ylabel("Period (s)")
    plt.title("Measured Periods")
    plt.show()


def printPeriodInfo(csvFile):
    measuredPeriods = rawPeriodList(csvFile)
    measuredPeriods = measuredPeriods[PERIODS_TO_SKIP:]

    print(f"The period is {avg(measuredPeriods):.5f} s "
          + f"(std. err. = {stderr(measuredPeriods):.5f} s, n = {len(measuredPeriods)})")


def analyzeAllFiles():
    for file in sorted(os.listdir()):
        if file.endswith(".csv"):
            print(f"File \"{file}\":")
            printPeriodInfo(file)
            print("")

analyzeAllFiles()
