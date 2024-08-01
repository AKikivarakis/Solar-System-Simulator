import math
import turtle

GravitationalConstant = 6.67*10**-11

# Screen Setup
screen = turtle.Screen()
screen.setup(600,600)
screen.bgcolor("black")

SCALE_BASE = 10
SCALE_FACTOR = 100

def logScale(distance, scale_base, scale_factor):
    return scale_factor * math.log(distance+1.1, scale_base)

class AstronomicalObject():
    
    minDisplaySize = 20

    def __init__(self, objectName, colour, distanceFromSun, radius, mass):

        # Turtle
        self.T = turtle.Turtle()
        self.T.shape("circle")
        self.T.color(colour)
        self.T.penup()
        self.T.hideturtle()

        self.objectName = objectName
        self.distanceFromSun = distanceFromSun
        self.radius = radius
        self.mass = mass

        self.position = [0, logScale(self.distanceFromSun, SCALE_BASE, SCALE_FACTOR)]
        self.velocity = [0,0]

        self.displaySize = max(math.log(self.radius, SCALE_BASE), self.minDisplaySize)

    def updatePosition(self):

        self.position[0] += self.velocity[0] * SCALE_FACTOR
        self.position[1] += self.velocity[1] * SCALE_FACTOR

        self.T.setx(self.position[0])
        self.T.sety(self.position[1])

    def calcDistance(self, otherObject):

        distance = math.sqrt((otherObject.position[0] - self.position[0])**2  + (otherObject.position[1] - self.position[1])**2)
        return distance
    
    # Horizontal Angle
    def calcAngle(self, otherObject):

        opposite = otherObject.position[1] - self.position[1]
        adjacent = otherObject.position[0] - self.position[0]

        if adjacent == 0:
            if opposite > 0:
                return math.radians(90)
            else:
                return math.radians(270)
            
        else:

            angle = math.atan(abs(opposite/adjacent))

            if opposite and adjacent > 0:
                return angle
            
            elif opposite and adjacent < 0:
                return math.pi + angle
            
            elif opposite < 0 and adjacent > 0:
                return  2*math.pi - angle
            
            elif opposite > 0 and adjacent < 0:
                return math.pi - angle

    def updateVelocity(self, otherObject):

        force = (GravitationalConstant * self.mass * otherObject.mass)/(self.calcDistance(otherObject)**2)

        acceleration = force/self.mass

        acceleration_x = acceleration*math.cos(self.calcAngle(otherObject))
        acceleration_y = acceleration*math.sin(self.calcAngle(otherObject))

        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y

    def draw(self):
        self.T.clear()
        self.T.dot(self.displaySize)


class Sun(AstronomicalObject):

    def __init__(self):

        super().__init__("Sun", "white", 0, 6.96*10**8, 2*10**30)

        self.position = [0,0]

class Planet(AstronomicalObject):

    def __init__(self, objectName, colour, distanceFromSun, radius, mass):
        super().__init__(objectName, colour, distanceFromSun, radius, mass)

sun = Sun()
mercury = Planet("mercury", "red", 4.6*10**10, 2.44*10**8, 3.3*10**23)

SOLAR_SYSTEM= [sun, mercury]

while True:
    for body in SOLAR_SYSTEM:

        for otherBody in SOLAR_SYSTEM:
            if body.objectName != otherBody.objectName and body.objectName != "Sun":
                body.updateVelocity(otherBody)

        body.updatePosition()
        body.draw()
    screen.update()