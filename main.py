import math
import time
import turtle

SCREEN = turtle.Screen()
SCREEN.setup(700,700) 
SCREEN.bgcolor("black")
turtle.tracer(0)

class Position2D :
    def __init__(self, x, y) :
        self.x = x
        self.y = y

    def pair(self) :
        return (self.x, self.y)
    def __repr__(self):
        return f"{type(self).__name__} ({self.x}, {self.y})"

class Vector2D :
    def __init__(self, i, j) :
        self.i = i
        self.j = j

    def plusEquals(self, vector) :
        self.i += vector.i
        self.j += vector.j

    def getMagnitude(self) :
        return math.sqrt(self.i**2 + self.j**2)
    def getAngle(self) :
        return math.degrees(math.atan2(self.j, self.i))
    def pair(self) :
        return (self.i, self.j)
    def __repr__(self):
        return f"{type(self).__name__} <{self.i}, {self.j}>"
    
class Force2D :
    def __init__(self, magnitude, angle):
        self.magnitude = magnitude
        self.angle = angle

    def toVector2D(self, mass) :
        a = self.magnitude/mass
        return Vector2D(a*math.cos(self.angle), a*math.sin(self.angle))
    
class Body :
    body_list = []
    def __init__(self, mass, x, y, i, j) :
        self.mass = mass
        self.position = Position2D(x,y)
        self.velocity = Vector2D(i,j)
        #self.acceleration = Vector2D(0,0)
        self.momentary_vectors = []
        
        Body.body_list.append(self)

        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.color('white')
        self.turtle.pensize(0.7)
        self.turtle.penup()
        self.turtle.goto(self.position.pair())
        self.turtle.pendown()
        self.turtle.shape('classic')

    def addMomentaryVectors(self, *vectors:Vector2D) :
        for vector in vectors :
            self.momentary_vectors.append(vector)

    def update(self) :
        #self.velocity.plusEquals(self.acceleration)
        for vector in self.momentary_vectors :
            print(vector)
            self.velocity.plusEquals(vector)
        self.momentary_vectors.clear()

        self.position.x += self.velocity.i
        self.position.y += self.velocity.j

    def render(self) :
        self.turtle.goto(self.position.pair())
        self.turtle.setheading(self.velocity.getAngle())
        #self.turtle.dot(3)

class StaticBody:
    def __init__(self, mass, x, y):
        self.mass = mass
        self.position = Position2D(x,y)

        self.turtle = turtle.Turtle()
        self.turtle.color('white')
        self.turtle.shape('circle')

    def render(self) :
        self.turtle.goto(self.position.pair())

def gravity(body1:Body, body2:Body) :
    # GMm/r^2
    G = (6.67)*(10**(-11))
    M = body1.mass
    m = body2.mass
    r = math.sqrt( (body2.position.x - body1.position.x)**2 + (body2.position.y - body1.position.y)**2 )
    return Force2D((G*M*m)/(r**2), math.atan2( (body1.position.y-body2.position.y), (body1.position.x-body2.position.x))-math.pi)

ship1 = Body(1, -10, 200, 5, 0)
ship2 = Body(5, 0, -100, -9, 1)
ship3 = Body(7, -380, 200, 10, -2)
ship4 = Body(10, -600, 200, 2, -1.5)
ship5 = Body(8, 100, -200, -1, -4)

planet = StaticBody(1e14, 0, 10)


while True:

    for body in Body.body_list :
        body.addMomentaryVectors(gravity(body, planet).toVector2D(body.mass))
        body.update()

    for body in Body.body_list :
        body.render()

    #planet.position = Position2D()

    planet.render()
    turtle.update()
    time.sleep(0.02)

turtle.mainloop()
