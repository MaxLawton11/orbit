import math
import time
import turtle

# turtle screen
SCREEN = turtle.Screen()
SCREEN.setup(700,700) 
SCREEN.bgcolor("black")
turtle.tracer(0)

# object to store a position
class Position2D :
    def __init__(self, x, y) :
        self.x = x
        self.y = y

    def pair(self) -> tuple[float, float] : # return (x, y)
        return (self.x, self.y)
    
    def __repr__(self): # pretty printing
        return f"{type(self).__name__} ({self.x}, {self.y})"

# a vector object for vector stuff
class Vector2D :
    def __init__(self, i, j) :
        self.i = i
        self.j = j

    def plusEquals(self, vector) : # a += for easy vector addition  
        self.i += vector.i
        self.j += vector.j

    def getMagnitude(self) -> float : # ruturn the magnitude of the vector
        return math.sqrt(self.i**2 + self.j**2)
    
    def getAngle(self) -> float : # return angle in degrees
        return math.degrees(math.atan2(self.j, self.i))
    
    def pair(self) -> tuple[float, float] : # return (x, y)
        return (self.i, self.j)
    
    def __repr__(self): # pretty printing
        return f"{type(self).__name__} <{self.i}, {self.j}>"
    
# a force object for force stuff
class Force2D :
    def __init__(self, magnitude, angle):
        self.magnitude = magnitude
        self.angle = angle

    def toVector2D(self, mass:float) -> Vector2D: # convert this Force to a Vector
        a = self.magnitude/mass
        return Vector2D(a*math.cos(self.angle), a*math.sin(self.angle))
    
# a dynamic(moving) phyics body
class DynamicBody :
    bodys_list = [] # track all the current moving bodys
    def __init__(self, mass, x, y, i, j) :
        self.mass = mass
        self.position = Position2D(x,y)
        self.velocity = Vector2D(i,j)
        # self.acceleration = Vector2D(0,0) # if you wanted a constant acceleration (booster idk)
        # you could as make jerk and so one with this: self.jerk = Vector2D(0,0)

        self.momentary_vectors = [] # vectors that are only applied for one "tick"
        
        DynamicBody.bodys_list.append(self) # add self cuz we are a DynamicBody

        # possess a turtle
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.color('white')
        self.turtle.pensize(0.7)
        self.turtle.penup()
        self.turtle.goto(self.position.pair())
        self.turtle.pendown()
        self.turtle.shape('classic')

    def addMomentaryVectors(self, *vectors:Vector2D) : # add a momentary vector(s)
        for vector in vectors :
            self.momentary_vectors.append(vector)

    def update(self) : # update physics (current position, velocity,... etc)
        # self.velocity.plusEquals(self.acceleration) # apply that constant acceleration
        # or any other vectors you might have like jerk: self.acceleration.plusEquals(self.jerk)

        # apply all momentary vectors
        for vector in self.momentary_vectors :
            print(vector)
            self.velocity.plusEquals(vector)
        self.momentary_vectors.clear() # clear the momentary vectors cuz we used them this "tick"

        # update position (can't use +=(.plusEquals) because position isn't technically a vector so it can't be added)
        self.position.x += self.velocity.i
        self.position.y += self.velocity.j

    def render(self) : # moved, turn, and render the turtle
        self.turtle.goto(self.position.pair())
        self.turtle.setheading(self.velocity.getAngle())
        #self.turtle.dot(3) # if you wanted to show where it was at each tick (leave a dot each tick) (does make it run loads slower)

# a static(noot moving) phyics body
class StaticBody:
    def __init__(self, mass, x, y):
        self.mass = mass
        self.position = Position2D(x,y)

        # possess a turtle
        self.turtle = turtle.Turtle()
        self.turtle.color('white')
        self.turtle.shape('circle')

    def render(self) : # render turtle
        self.turtle.goto(self.position.pair())

# when givin a DynamicBody and corresponding StaticBody, it returns the appropriate force (as a Force) that the DynamicBody would be feeling
def gravity(body1:DynamicBody, body2:DynamicBody) -> Force2D:
    # GMm/r^2
    G = (6.67)*(10**(-11))
    M = body1.mass
    m = body2.mass
    r = math.sqrt( (body2.position.x - body1.position.x)**2 + (body2.position.y - body1.position.y)**2 )
    return Force2D((G*M*m)/(r**2), math.atan2( (body1.position.y-body2.position.y), (body1.position.x-body2.position.x))-math.pi)

# all DynamicBodys
ship1 = DynamicBody(1, -10, 200, 5, 0)
ship2 = DynamicBody(5, 23, -100, -9, 1)
ship3 = DynamicBody(7, -380, 200, 10, -2)
ship4 = DynamicBody(10, -600, 200, 2, -1.5)
ship5 = DynamicBody(8, 100, -200, -1, -4)

# the StaticBody
planet = StaticBody(1e14, 0, 10)

# a "ticker"
while True:

    for body in DynamicBody.bodys_list :
        body.addMomentaryVectors(gravity(body, planet).toVector2D(body.mass))
        body.update()

    for body in DynamicBody.bodys_list :
        body.render()

    planet.render()
    turtle.update()
    time.sleep(0.02)

turtle.mainloop()
