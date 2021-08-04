import math
import matplotlib.pyplot as plt

degree_sign = u'\N{DEGREE SIGN}'
def decimal_range(start, stop, decrement):
    while start >= stop:
        yield start
        start -= decrement

figure, axes = plt.subplots()

# Read in user input
velocityInitialString = input("Enter velocity of arm (mph):")
bodyHeightString = input("Enter height of body up to the arm (ft):")
armHeightString = input("Enter length of arm (ft):")

# Convert input to float
velocityInitialMPH = float(velocityInitialString) 
bodyHeightFT = float(bodyHeightString)
armLengthFT = float(armHeightString)

velocityInitial = velocityInitialMPH / 2.23693629
bodyHeight = bodyHeightFT / 3.2808399
armLength = armLengthFT / 3.2808399

# Plot data
bestDistance, bestDistanceAngle, bestHeightAngle, bestHeight = [0,0,0,0]
upX, upY, leftX, leftY = [0, 0, 0, 0]
for angle in decimal_range(90, 0, 1):

    yVelocityInitial = math.sin(angle * (math.pi / 180)) * velocityInitial
    xVelocity = math.cos(angle * (math.pi / 180)) * velocityInitial
    timeToReachApex = yVelocityInitial / 9.81
    distanceFromStartToApex = (yVelocityInitial * timeToReachApex) + (.5 * -9.81 * (timeToReachApex * timeToReachApex))
    timeFromApexToGround = math.sqrt((distanceFromStartToApex + bodyHeight) / (.5 * 9.81))
    timeTotal = timeToReachApex + timeFromApexToGround
    timeIncrement = timeTotal / 1000
    angledArmHeight = math.cos(angle * (math.pi / 180)) * armLength
    distanceFromBodyToArm = math.sin(angle * (math.pi / 180)) * armLength

    heights = []
    distances = []
    height = bodyHeight + angledArmHeight
    time = 0
    distance = -distanceFromBodyToArm
    heightFT = height  * 3.2808399
    distanceFT = distance * 3.2808399
    if angle == 0 and time == 0:
        upX = distanceFT
        upY = heightFT
    if angle == 90 and time == 0:
        leftX = distanceFT
        leftY = heightFT
    while height >= 0:
        heightFT = height  * 3.2808399
        distanceFT = distance * 3.2808399
        heights.append(heightFT)
        distances.append(distanceFT)
        height = (yVelocityInitial * time) + (.5 * -9.81 * (time * time)) + bodyHeight + angledArmHeight
        distance = (xVelocity * time) - distanceFromBodyToArm
        time += timeIncrement
        if heightFT > bestHeight:
                bestHeight = heightFT
                bestHeightAngle = angle

    if distanceFT > bestDistance:
        bestDistance = distanceFT
        bestDistanceAngle = angle

    plt.plot(distances, heights)#, label="{0}{1}".format(angle, degree_sign)

#plt.legend(loc ="upper right")
draw_outer_circle = plt.Circle((upX, leftY), (leftX - upX), fill=False)
draw_inner_circle = plt.Circle((upX, leftY), (leftX - upX) / 10, color='black')#, fill=False)
axes.set_aspect(1)
axes.add_artist(draw_outer_circle)
axes.add_artist(draw_inner_circle)
axes.add_patch(plt.Rectangle((upX, leftY), (leftX - upX), (leftX - upX) / 20, color='black'))

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.annotate("Best Distance: {2:.2f} at {0}{1}\nBest Height :{4:.2f} at {3}{1}".format(bestDistanceAngle, degree_sign, bestDistance, bestHeightAngle, bestHeight), 
                xy=(bestDistance, bestHeight), ha='right', va='top')
plt.ylabel('Height(ft)')
plt.xlabel('Distance(ft)')
plt.title('Launch Trajectories')
figure.savefig("windmill.png")
plt.show() 
