# Self Driving Car

# Importing the libraries
import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
import time

# Importing the Kivy packages
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.config import Config
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

# Importing the Dqn object from our AI in ai.py
from ai import Dqn

# Adding this line if we don't want the right click to put a red point
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Introducing last_x and last_y, used to keep the last point in memory when we draw the sand on the map
last_x = 0
last_y = 0
n_points = 0
length = 0

# Getting our AI, which we call "brain", and that contains our neural network that represents our Q-function
brain = Dqn(7,7,0.9)
action2rotation = [-30,-20,-10,0,10,20,30]
last_reward = 0
scores = []

# Initializing the map
first_update = True
def init():
    global sand
    global goals
    goals = [(40,260),(300,300),(500,500)]
    global goal_x
    global goal_y
    global first_update
    sand = np.zeros((longueur,largeur))
    goal_x = randint(100,500)
    goal_y = randint(100,500)
    #print(goal_x,"  ",goal_y)#largeur - 20
    first_update = False

# Initializing the last distance
last_distance = 0

# Creating the car class

class Car(Widget):
    
    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)
    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)
    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)
    sensor4_x = NumericProperty(0)
    sensor4_y = NumericProperty(0)
    sensor4 = ReferenceListProperty(sensor4_x, sensor4_y)
    sensor5_x = NumericProperty(0)
    sensor5_y = NumericProperty(0)
    sensor5 = ReferenceListProperty(sensor5_x, sensor5_y)
    sensor6_x = NumericProperty(0)
    sensor6_y = NumericProperty(0)
    sensor6 = ReferenceListProperty(sensor6_x, sensor6_y)
    sensor7_x = NumericProperty(0)
    sensor7_y = NumericProperty(0)
    sensor7 = ReferenceListProperty(sensor7_x, sensor7_y)
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)
    signal4 = NumericProperty(0)
    signal5 = NumericProperty(0)
    signal6 = NumericProperty(0)
    signal7 = NumericProperty(0)

    def move(self, rotation):
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        self.sensor1 = Vector(30, 0).rotate((self.angle-30)%360) + self.pos
        self.sensor2 = Vector(30, 0).rotate((self.angle-20)%360) + self.pos
        self.sensor3 = Vector(30, 0).rotate((self.angle-10)%360) + self.pos
	self.sensor4 = Vector(30, 0).rotate(self.angle) + self.pos
	self.sensor5 = Vector(30, 0).rotate((self.angle+10)%360) + self.pos
	self.sensor6 = Vector(30, 0).rotate((self.angle+20)%360) + self.pos
	self.sensor7 = Vector(30, 0).rotate((self.angle+30)%360) + self.pos
        self.signal1 = int(np.sum(sand[int(self.sensor1_x)-2:int(self.sensor1_x)+2, int(self.sensor1_y)-2:int(self.sensor1_y)+2]))/16.#int(np.sum(sand[int(self.sensor1_x),int(self.sensor1_y)]))/2. 
        self.signal2 = int(np.sum(sand[int(self.sensor2_x)-2:int(self.sensor2_x)+2, int(self.sensor2_y)-2:int(self.sensor2_y)+2]))/16.#int(np.sum(sand[int(self.sensor2_x),int(self.sensor2_y)]))/2. 
        self.signal3 = int(np.sum(sand[int(self.sensor3_x)-2:int(self.sensor3_x)+2, int(self.sensor3_y)-2:int(self.sensor3_y)+2]))/16.#int(np.sum(sand[int(self.sensor3_x),int(self.sensor3_y)]))/2. 
        self.signal4 = int(np.sum(sand[int(self.sensor4_x)-2:int(self.sensor4_x)+2, int(self.sensor4_y)-2:int(self.sensor4_y)+2]))/16.#int(np.sum(sand[int(self.sensor4_x),int(self.sensor4_y)]))/2. 
        self.signal5 = int(np.sum(sand[int(self.sensor5_x)-2:int(self.sensor5_x)+2, int(self.sensor5_y)-2:int(self.sensor5_y)+2]))/16.#int(np.sum(sand[int(self.sensor5_x),int(self.sensor5_y)]))/2. 
        self.signal6 = int(np.sum(sand[int(self.sensor6_x)-2:int(self.sensor6_x)+2, int(self.sensor6_y)-2:int(self.sensor6_y)+2]))/16.#int(np.sum(sand[int(self.sensor6_x),int(self.sensor6_y)]))/2. 
        self.signal7 = int(np.sum(sand[int(self.sensor7_x)-2:int(self.sensor7_x)+2, int(self.sensor7_y)-2:int(self.sensor7_y)+2]))/16.#int(np.sum(sand[int(self.sensor7_x),int(self.sensor7_y)]))/2.
        if self.sensor1_x>longueur-10 or self.sensor1_x<10 or self.sensor1_y>largeur-10 or self.sensor1_y<10:
            self.signal1 = 0.
        if self.sensor2_x>longueur-10 or self.sensor2_x<10 or self.sensor2_y>largeur-10 or self.sensor2_y<10:
            self.signal2 = 0.
        if self.sensor3_x>longueur-10 or self.sensor3_x<10 or self.sensor3_y>largeur-10 or self.sensor3_y<10:
            self.signal3 = 0.
        if self.sensor4_x>longueur-10 or self.sensor4_x<10 or self.sensor4_y>largeur-10 or self.sensor4_y<10:
            self.signal4 = 0.
        if self.sensor5_x>longueur-10 or self.sensor5_x<10 or self.sensor5_y>largeur-10 or self.sensor5_y<10:
            self.signal5 = 0.
        if self.sensor6_x>longueur-10 or self.sensor6_x<10 or self.sensor6_y>largeur-10 or self.sensor6_y<10:
            self.signal6 = 0.
        if self.sensor7_x>longueur-10 or self.sensor7_x<10 or self.sensor7_y>largeur-10 or self.sensor7_y<10:
            self.signal7 = 0.

class Ball1(Widget):
    pass
class Ball2(Widget):
    pass
class Ball3(Widget):
    pass
class Ball4(Widget):
    pass
class Ball5(Widget):
    pass
class Ball6(Widget):
    pass
class Ball7(Widget):
    pass

# Creating the game class

class Game(Widget):

    car = ObjectProperty(None)
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)
    ball4 = ObjectProperty(None)
    ball5 = ObjectProperty(None)
    ball6 = ObjectProperty(None)
    ball7 = ObjectProperty(None)

    def serve_car(self):
        self.car.center = self.center
        self.car.velocity = Vector(6, 0)

    def update(self, dt):

        global brain
        global last_reward
        global scores
        global last_distance
        global goal_x
        global goal_y
        global longueur
        global largeur
	global goals

        longueur = self.width
        largeur = self.height
        if first_update:
            init()

        xx = goal_x - self.car.x
        yy = goal_y - self.car.y
        orientation = Vector(*self.car.velocity).angle((xx,yy))/180.
        last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, self.car.signal4, self.car.signal5, self.car.signal6, self.car.signal7]#, orientation, -orientation]
        #if(self.car.signal1)
        action = brain.update(last_reward, last_signal)
        scores.append(brain.score())
        rotation = action2rotation[action]
        self.car.move(rotation)
        distance = np.sqrt((self.car.x - goal_x)**2 + (self.car.y - goal_y)**2)
        self.ball1.pos = self.car.sensor1
        self.ball2.pos = self.car.sensor2
        self.ball3.pos = self.car.sensor3
        self.ball4.pos = self.car.sensor4
        self.ball5.pos = self.car.sensor5
        self.ball6.pos = self.car.sensor6
        self.ball7.pos = self.car.sensor7

        if  sand[int(self.car.x),int(self.car.y)] > 0:
            self.car.velocity = Vector(4, 0).rotate(self.car.angle)
	    for x,y in goals:
		if(self.car.x==x and self.car.y==y):
			last_reward=1
		else:
            		last_reward = 0
	#elif sand[int(self.car.x),int(self.car.y)] <=1.0 and sand[int(self.car.x),int(self.car.y)] >0.8:
            #self.car.velocity = Vector(3, 0).rotate(self.car.angle)
            #last_reward = +1
        else: # otherwise
            self.car.velocity = Vector(6, 0).rotate(self.car.angle)
            last_reward = -0.5
            #if distance < last_distance:
                #last_reward = 0.1

        if self.car.x < 10:
            self.car.x = 10
            last_reward = -1
        if self.car.x > self.width - 10:
            self.car.x = self.width - 10
            last_reward = -1
        if self.car.y < 10:
            self.car.y = 10
            last_reward = -1
        if self.car.y > self.height - 10:
            self.car.y = self.height - 10
            last_reward = -1

        '''if distance < 30:
            goal_x = self.width-goal_x
            goal_y = self.height-goal_y
        last_distance = distance'''

# Adding the painting tools

class MyPaintWidget(Widget):


    #def __init__(self):
         # with self.canvas:
         #    Color(*color, mode='hsv')
         #    d = 10.
         #    Ellipse(pos=(goal_x - d / 2, goal_y - d / 2), size=(d, d))


    def on_touch_down(self, touch):
        global length, n_points, last_x, last_y, goal_x, goal_y
        with self.canvas:
            '''Color(0.2,0.2,0.3)
            d = 10.
            Ellipse(pos=(goal_x - d / 2, goal_y - d / 2), size=(d, d))'''
            Color(0.8,0.7,0)
	    width = 2
            for x in range(600):
		y=x
            	touch.ud['line'] = Line(points=(x,y),width=width)#(touch.x, touch.y))
	        touch.ud['line'].points += [x,y]
                sand[int(x),int(y)] = 1
                sand[int(x) - width : int(x) + width, int(y) - width : int(y) + width] = 1
                y=-x+500
            	touch.ud['line'] = Line(points=(x,y),width=width)#(touch.x, touch.y))
	        touch.ud['line'].points += [x,y]
                sand[int(x),int(y)] = 1
		sand[int(x) - width : int(x) + width, int(y) - width : int(y) + width] = 1
		#y=x-500
            	#touch.ud['line'] = Line(points=(x,y),width=10)#(touch.x, touch.y))
	        #touch.ud['line'].points += [x,y]
		#sand[int(x),int(y)] = 1
		y=300
            	touch.ud['line'] = Line(points=(x,y),width=width)#(touch.x, touch.y))
	        touch.ud['line'].points += [x,y]
		sand[int(x),int(y)] = 1
		sand[int(x) - width : int(x) + width, int(y) - width : int(y) + width] = 1
                y=595
            	touch.ud['line'] = Line(points=(x,y),width=width)#(touch.x, touch.y))
	        touch.ud['line'].points += [x,y]
		sand[int(x),int(y)] = 1
		sand[int(x) - width : int(x) + width, int(y) - width : int(y) + width] = 1
                y=-x+300
            	touch.ud['line'] = Line(points=(x,y),width=width)#(touch.x, touch.y))
	        touch.ud['line'].points += [x,y]
      		sand[int(x),int(y)] = 1
                y=500
            	touch.ud['line'] = Line(points=(y,x),width=width)#(touch.x, touch.y))
	        touch.ud['line'].points += [y,x]
		sand[int(y),int(x)] = 1
		sand[int(y) - width : int(y) + width, int(x) - width : int(x) + width] = 1
            Color(1.0,1.0,1.0)
  	    d = 10.
            for x,y in goals:
  		Ellipse(pos=(x - d / 2, y - d / 2), size=(d, d))
                sand[int(x),int(y)] = 1
 		sand[int(x) - 10 : int(x) + 10, int(y) - 10 : int(y) + 10] = 1
	    Color(0.8,0.7,0)	
            touch.ud['line'] = Line(points = (touch.x, touch.y), width = 10)
            #Ellipse(pos=(goal_x - d / 2, goal_y - d / 2), size=(d, d))
            last_x = int(touch.x)
            last_y = int(touch.y)
            n_points = 0
            length = 0
            sand[int(touch.x),int(touch.y)] = 1

    def on_touch_move(self, touch):
        global length, n_points, last_x, last_y
        if touch.button == 'left':
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            #length += np.sqrt(max((x - last_x)**2 + (y - last_y)**2, 2))
            #n_points += 1.
            #density = n_points/(length)
            touch.ud['line'].width = 10#int(20 * density + 1)
            sand[int(touch.x) - 10 : int(touch.x) + 10, int(touch.y) - 10 : int(touch.y) + 10] = 1
            last_x = x
            last_y = y

# Adding the API Buttons (clear, save and load)

class CarApp(App):

    def build(self):
        self.painter = MyPaintWidget()
        
        parent = Game()
        parent.serve_car()
        #time.sleep(10)
        Clock.schedule_interval(parent.update, 1.0/60.0)
        clearbtn = Button(text = 'clear')
        savebtn = Button(text = 'save', pos = (parent.width, 0))
        loadbtn = Button(text = 'load', pos = (2 * parent.width, 0))
        clearbtn.bind(on_release = self.clear_canvas)
        savebtn.bind(on_release = self.save)
        loadbtn.bind(on_release = self.load)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        parent.add_widget(savebtn)
        parent.add_widget(loadbtn)
        return parent

    def clear_canvas(self, obj):
        global sand
        self.painter.canvas.clear()
        sand = np.zeros((longueur,largeur))

    def save(self, obj):
        print("saving brain...")
        brain.save()
        plt.plot(scores)
        plt.show()

    def load(self, obj):
        print("loading last saved brain...")
        brain.load()

# Running the whole thing
if __name__ == '__main__':
    CarApp().run()
