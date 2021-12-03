import math
import matplotlib.pyplot as plt

degree_sign = u'\N{DEGREE SIGN}'
def decimal_range(start, stop, decrement):
    while start >= stop:
        yield start
        start -= decrement

# Initialize multiple plots
figure, axis = plt.subplots(1, 2)
axis[0].set(xlabel='Time (s)', ylabel='Height (m)', title='Time of Flight')
axis[1].set(xlabel='Distance (m)', yticks=[], title='Range')

# Read in user input
velocityInitialString = input("Enter velocity:")
heightInitialString = input("Enter height:")

# Convert input to float
velocityInitial = float(velocityInitialString) 
heightInitial = float(heightInitialString)

# Plot data
for angle in decimal_range(75, 15, 15):

    yVelocityInitial = math.sin(angle * (math.pi / 180)) * velocityInitial
    xVelocity = math.cos(angle * (math.pi / 180)) * velocityInitial
    timeToReachApex = yVelocityInitial / 9.81
    distanceFromStartToApex = (yVelocityInitial * timeToReachApex) + (.5 * -9.81 * (timeToReachApex * timeToReachApex))
    timeFromApexToGround = math.sqrt((distanceFromStartToApex + heightInitial) / (.5 * 9.81))
    timeTotal = timeToReachApex + timeFromApexToGround
    timeIncrement = timeTotal / 1000
    
    times = []
    heights = []
    distances = []
    height = heightInitial
    time = 0
    distance = 0
    while height >= 0:
        heights.append(height)
        times.append(time)
        distances.append(distance)
        height = (yVelocityInitial * time) + (.5 * -9.81 * (time * time)) + heightInitial
        distance = xVelocity * time
        time += timeIncrement
    axis[0].plot(times, heights)
    axis[1].plot(distances, heights, label="{0}{1}".format(angle, degree_sign))

#figure.savefig("traj.png")
axis[1].legend(loc ="upper right")
plt.show() 
