import math
import matplotlib.pyplot as plt

GRAVITY = -9.80665

# Make my own ranges, functions, and classes
def decimal_range(start, stop, change):
    while start >= stop:
        yield start
        start += change

class TrajectoriesInfo:
    def __init__(self):
        self.bestDistance, self.bestDistanceAngle, self.bestHeightAngle, self.bestHeight = [0,0,0,0]
        self.distancesForBestDistance = []
        self.distancesForBestHeight = []
        self.heightsForBestDistance = []
        self.heightsForBestHeight = []
    
    def Update(self, distance, height, angle, distances, heights):
        if height > self.bestHeight:
            self.bestHeight = height
            self.bestHeightAngle = angle
            self.distancesForBestHeight = distances
            self.heightsForBestHeight = heights

        if distance > trajectories_info.bestDistance:
            self.bestDistance = distance
            self.bestDistanceAngle = angle
            self.distancesForBestDistance = distances
            self.heightsForBestDistance = heights

def DrawProjectileLauncher(bodyHeight, armLength, axes):
    draw_inner_circle = plt.Circle((0, bodyHeight), -armLength / 8, color='black')
    draw_arm = plt.Rectangle((0, bodyHeight), -armLength, -armLength / 15, color='black')
    draw_body = plt.Rectangle((0, bodyHeight), -armLength / 10, -bodyHeight, color='black')
    axes.set_aspect(1)
    axes.add_artist(draw_inner_circle)
    axes.add_patch(draw_arm)
    axes.add_patch(draw_body)
    return
    
def DrawPlot():
    DEGREE_SIGN = u'\N{DEGREE SIGN}'
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.annotate("Best Distance: {2:.1f} ft at {0:.1f}{1}\nBest Height: {4:.1f} ft at {3:.1f}{1}".format(
                    trajectories_info.bestDistanceAngle, DEGREE_SIGN, 
                    trajectories_info.bestDistance, 
                    trajectories_info.bestHeightAngle, trajectories_info.bestHeight), 
                    xy=(trajectories_info.bestDistance,trajectories_info.bestHeight), ha='right', va='top')
    plt.ylabel('Height (ft)')
    plt.xlabel('Distance (ft)')
    plt.title('What Angle is Best?')
    plt.show() 
    return

def FeetToMeters(measurementInFeet):
    return measurementInFeet / 3.2808399

def MetersToFeet(measurementInMeters):
    return measurementInMeters * 3.2808399

def CalculateTrajectoryFromConditions(bodyHeight, angle, yVelocityInitial, xVelocity, timeTotal, heightFromBodyToArm, distanceFromBodyToArm):
    heights, distances = ([],[])
    currentHeight = bodyHeight + heightFromBodyToArm
    currentDistance = -distanceFromBodyToArm
    currentTime = 0
    bestHeight = 0
    increment = timeTotal / 1000
    while currentHeight >= 0:
        heightFT = MetersToFeet(currentHeight)
        distanceFT = MetersToFeet(currentDistance)
        heights.append(heightFT)
        distances.append(distanceFT)
        currentHeight = (yVelocityInitial * currentTime) + (.5 * GRAVITY * (currentTime**2)) + bodyHeight + heightFromBodyToArm
        currentDistance = (xVelocity * currentTime) - distanceFromBodyToArm
        if heightFT > bestHeight:
            bestHeight = heightFT
        # Makes so there is 1000 data points for each trajectory
        currentTime += increment
        
    trajectories_info.Update(distanceFT, bestHeight, angle, distances, heights)

def PlotData(velocityInitial, bodyHeight, armLength):
    for angle in decimal_range(90, 0, -.1):
        radians = math.radians(angle)
        yVelocityInitial = math.sin(radians) * velocityInitial
        xVelocity = math.cos(radians) * velocityInitial
        timeToReachApex = yVelocityInitial / -GRAVITY
        distanceFromStartToApex = (yVelocityInitial * timeToReachApex) + (.5 * GRAVITY * (timeToReachApex**2))
        timeFromApexToGround = math.sqrt((distanceFromStartToApex + bodyHeight) / (.5 * -GRAVITY))
        timeTotal = timeToReachApex + timeFromApexToGround
        heightFromBodyToArm = math.cos(radians) * armLength
        distanceFromBodyToArm = math.sin(radians) * armLength
        CalculateTrajectoryFromConditions(bodyHeight, angle, yVelocityInitial, xVelocity, timeTotal, heightFromBodyToArm, distanceFromBodyToArm)
        
    plt.plot(trajectories_info.distancesForBestDistance, trajectories_info.heightsForBestDistance)
    plt.plot(trajectories_info.distancesForBestHeight, trajectories_info.heightsForBestHeight)

def Main(bodyHeightFT:float, armLengthFT:float, armVelocityMPH:float):

    # Convert from US to Metric
    armVelocity = armVelocityMPH / 2.23693629
    bodyHeight = FeetToMeters(bodyHeightFT)
    armLength = FeetToMeters(armLengthFT)

    global trajectories_info
    trajectories_info = TrajectoriesInfo()
    figure, axes = plt.subplots()
    PlotData(armVelocity, bodyHeight, armLength)
    DrawProjectileLauncher(bodyHeightFT, armLengthFT, axes)
    DrawPlot()

if __name__ == '__main__':

    # Read in user input
    armVelocityString = input("Enter velocity of arm (mph):")
    bodyHeightString = input("Enter height of body (ft):")
    armLengthString = bodyHeightString
    while float(armLengthString) >= float(bodyHeightString): 
        armLengthString = input("Enter length of arm (ft):")

    armVelocity = float(armVelocityString)
    bodyHeight = float(bodyHeightString)
    armLength = float(armLengthString)

    Main(armVelocity, bodyHeight, armLength)