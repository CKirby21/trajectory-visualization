import math
import matplotlib.pyplot as plt

# Make my own ranges, functions, and classes
def decimal_range(start, stop, change):
    while start >= stop:
        yield start
        start += change

class MyCircle:
    upX, upY, leftX, leftY = [0,0,0,0]

class TrajectoriesInfo:
    bestDistance, bestDistanceAngle, bestHeightAngle, bestHeight = [0,0,0,0]
    distancesForBestDistance = []
    distancesForBestHeight = []
    heightsForBestDistance = []
    heightsForBestHeight = []

def UpdateCircleLocation(angle, distance, height):
    if angle == 0:
        circle.upX = MetersToFeet(distance)
        circle.upY = MetersToFeet(height)
    if angle == 90:
        circle.leftX = MetersToFeet(distance)
        circle.leftY = MetersToFeet(height)

def UpdateBestHeightInfo(height, angle, distances, heights):
    if height > trajectories_info.bestHeight:
        trajectories_info.bestHeight = height
        trajectories_info.bestHeightAngle = angle
        trajectories_info.distancesForBestHeight = distances
        trajectories_info.heightsForBestHeight = heights

def UpdateBestDistanceInfo(distance, angle, distances, heights):
    if distance > trajectories_info.bestDistance:
        trajectories_info.bestDistance = distance
        trajectories_info.bestDistanceAngle = angle
        trajectories_info.distancesForBestDistance = distances
        trajectories_info.heightsForBestDistance = heights

def DrawProjectileLauncher():
    draw_inner_circle = plt.Circle((circle.upX, circle.leftY), (circle.leftX - circle.upX) / 8, color='black')
    draw_arm = plt.Rectangle((circle.upX, circle.leftY), (circle.leftX - circle.upX), (circle.leftX - circle.upX) / 15, color='black')
    draw_body = plt.Rectangle((circle.upX, circle.leftY), (circle.leftX - circle.upX) / 10, -circle.leftY, color='black')
    axes.set_aspect(1)
    axes.add_artist(draw_inner_circle)
    axes.add_patch(draw_arm)
    axes.add_patch(draw_body)
    return
    
def DrawPlot():
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.annotate("Best Distance: {2:.1f} ft at {0:.1f}{1}\nBest Height: {4:.1f} ft at {3:.1f}{1}".format(
                    trajectories_info.bestDistanceAngle, degree_sign, 
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
    height = bodyHeight + heightFromBodyToArm
    distance = -distanceFromBodyToArm
    currentTime = 0
    bestHeight = 0
    UpdateCircleLocation(angle, distance, height)
    while height >= 0:
        heightFT = MetersToFeet(height)
        distanceFT = MetersToFeet(distance)
        heights.append(heightFT)
        distances.append(distanceFT)
        height = (yVelocityInitial * currentTime) + (.5 * -9.81 * (currentTime * currentTime)) + bodyHeight + heightFromBodyToArm
        distance = (xVelocity * currentTime) - distanceFromBodyToArm
        # Makes so there is 1000 data points for each trajectory
        currentTime += (timeTotal / 1000)
        if heightFT > bestHeight:
            bestHeight = heightFT
        
    UpdateBestHeightInfo(bestHeight, angle, distances, heights)
    UpdateBestDistanceInfo(distanceFT, angle, distances, heights)

def PlotData(velocityInitial, bodyHeight, armLength):
    for angle in decimal_range(90, 0, -.1):

        yVelocityInitial = math.sin(angle * (math.pi / 180)) * velocityInitial
        xVelocity = math.cos(angle * (math.pi / 180)) * velocityInitial
        timeToReachApex = yVelocityInitial / 9.81
        distanceFromStartToApex = (yVelocityInitial * timeToReachApex) + (.5 * -9.81 * (timeToReachApex * timeToReachApex))
        timeFromApexToGround = math.sqrt((distanceFromStartToApex + bodyHeight) / (.5 * 9.81))
        timeTotal = timeToReachApex + timeFromApexToGround
        heightFromBodyToArm = math.cos(angle * (math.pi / 180)) * armLength
        distanceFromBodyToArm = math.sin(angle * (math.pi / 180)) * armLength
        CalculateTrajectoryFromConditions(bodyHeight, angle, yVelocityInitial, xVelocity, timeTotal, heightFromBodyToArm, distanceFromBodyToArm)
        
    plt.plot(trajectories_info.distancesForBestDistance, trajectories_info.heightsForBestDistance)
    plt.plot(trajectories_info.distancesForBestHeight, trajectories_info.heightsForBestHeight)



if __name__ == '__main__':
    
    # Initialize global variables
    circle = MyCircle()
    trajectories_info = TrajectoriesInfo()
    degree_sign = u'\N{DEGREE SIGN}'
    figure, axes = plt.subplots()

    # Read in user input
    velocityInitialString = input("Enter velocity of arm (mph):")
    bodyHeightString = input("Enter height of body (ft):")
    armHeightString = bodyHeightString
    while float(armHeightString) >= float(bodyHeightString): 
        armHeightString = input("Enter length of arm (ft):")

    # Convert from US to Metric
    velocityInitial = float(velocityInitialString) / 2.23693629
    bodyHeight = FeetToMeters(float(bodyHeightString))
    armLength = FeetToMeters(float(armHeightString))

    PlotData(velocityInitial, bodyHeight, armLength)
    DrawProjectileLauncher()
    DrawPlot()