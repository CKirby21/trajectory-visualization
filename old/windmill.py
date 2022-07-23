import math
import matplotlib.pyplot as plt

# Make my own ranges, functions, and classes
def decimal_range(start, stop, change):
    while start >= stop:
        yield start
        start += change

class MyCircle:
    upX, upY, leftX, leftY = [0,0,0,0]

class MyAnnotation:
    bestDistance, bestDistanceAngle, bestHeightAngle, bestHeight = [0,0,0,0]
    distancesForBestDistance = []
    distancesForBestHeight = []
    heightsForBestDistance = []
    heightsForBestHeight = []

def UpdateCircleLocation(angle, time, distance, height):
    if angle == 0 and time == 0:
        circle.upX = MetersToFeet(distance)
        circle.upY = MetersToFeet(height)
    if angle == 90 and time == 0:
        circle.leftX = MetersToFeet(distance)
        circle.leftY = MetersToFeet(height)

def UpdateBestHeightInfo(height, angle, distances, heights):
    if height > annotation.bestHeight:
            annotation.bestHeight = height
            annotation.bestHeightAngle = angle
            annotation.distancesForBestHeight = distances
            annotation.heightsForBestHeight = heights

def UpdateBestDistanceInfo(distance, angle, distances, heights):
    if distance > annotation.bestDistance:
        annotation.bestDistance = distance
        annotation.bestDistanceAngle = angle
        annotation.distancesForBestDistance = distances
        annotation.heightsForBestDistance = heights

def DrawProjectileLauncher():
    #draw_outer_circle = plt.Circle((circle.upX, circle.leftY), (circle.leftX - circle.upX), fill=False)
    draw_inner_circle = plt.Circle((circle.upX, circle.leftY), (circle.leftX - circle.upX) / 8, color='black')#, fill=False)
    draw_arm = plt.Rectangle((circle.upX, circle.leftY), (circle.leftX - circle.upX), (circle.leftX - circle.upX) / 15, color='black')
    draw_body = plt.Rectangle((circle.upX, circle.leftY), (circle.leftX - circle.upX) / 10, -circle.leftY, color='black')
    axes.set_aspect(1)
    #axes.add_artist(draw_outer_circle)
    axes.add_artist(draw_inner_circle)
    axes.add_patch(draw_arm)
    axes.add_patch(draw_body)
    return
    
def DrawPlot():
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.annotate("Best Distance: {2:.2f} at {0}{1}\nBest Height :{4:.2f} at {3}{1}".format(
                    annotation.bestDistanceAngle, degree_sign, annotation.bestDistance, 
                    annotation.bestHeightAngle, annotation.bestHeight), xy=(annotation.bestDistance, annotation.bestHeight), ha='right', va='top')
    plt.ylabel('Height (ft)')
    plt.xlabel('Distance (ft)')
    plt.title('Launch Trajectories')
    plt.show() 
    return

def FeetToMeters(measurementInFeet):
    return measurementInFeet / 3.2808399

def MetersToFeet(measurementInMeters):
    return measurementInMeters * 3.2808399

def PlotData(velocityInitial, bodyHeight, armLength):
    for angle in decimal_range(90, 0, -1):

        yVelocityInitial = math.sin(angle * (math.pi / 180)) * velocityInitial
        xVelocity = math.cos(angle * (math.pi / 180)) * velocityInitial
        timeToReachApex = yVelocityInitial / 9.81
        distanceFromStartToApex = (yVelocityInitial * timeToReachApex) + (.5 * -9.81 * (timeToReachApex * timeToReachApex))
        timeFromApexToGround = math.sqrt((distanceFromStartToApex + bodyHeight) / (.5 * 9.81))
        timeTotal = timeToReachApex + timeFromApexToGround
        heightFromBodyToArm = math.cos(angle * (math.pi / 180)) * armLength
        distanceFromBodyToArm = math.sin(angle * (math.pi / 180)) * armLength

        heights = []
        distances = []
        height = bodyHeight + heightFromBodyToArm
        distance = -distanceFromBodyToArm
        time = 0
        bestHeight = 0
        UpdateCircleLocation(angle, time, distance, height)
        while height >= 0:
            heightFT = MetersToFeet(height)
            distanceFT = MetersToFeet(distance)
            heights.append(heightFT)
            distances.append(distanceFT)
            height = (yVelocityInitial * time) + (.5 * -9.81 * (time * time)) + bodyHeight + heightFromBodyToArm
            distance = (xVelocity * time) - distanceFromBodyToArm
            time += (timeTotal / 1000)
            if heightFT > bestHeight:
                bestHeight = heightFT
        
        UpdateBestHeightInfo(bestHeight, angle, distances, heights)
        UpdateBestDistanceInfo(distanceFT, angle, distances, heights)
        # if angle % 12 == 0:
        #     plt.plot(distances, heights)
    plt.plot(annotation.distancesForBestDistance, annotation.heightsForBestDistance)
    plt.plot(annotation.distancesForBestHeight, annotation.heightsForBestHeight)


# Initialize global variables
circle = MyCircle()
annotation = MyAnnotation()
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
