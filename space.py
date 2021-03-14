import pygame
import sys
import random
import math

from math import cos, sin, radians, sqrt

from pygame import *
#from pygame import display

FPS = 30
WIN_WIDTH = 0
WIN_HEIGHT = 0
CENTERX = 0
CENTERY = 0

MAXSPEED = 10
STARSHIPSIZEMOD = 3

colorBlue = "#0000FF"
colorGreen = "#00FF00"
colorRed = "#FF0000"
colorBlack = "#000000"

asteroidVertexOriginal = [[70, 0], [70, 60], [70, 120], [70, 180], [70, 240], [70, 300], [70, 0]]
shipVertexOriginal = [[70, 225], [50, 270], [70, 315], [100, 0], [70, 45], [50, 90], [70, 135], [0, 0]]


class Asteroid:

    def __init__(self, x, y, color, velosityX, velosityY, life, degreesSpeed, sizeMod, uid):

        self.x = x
        self.y = y
        self.color = color
        self.velosityX = velosityX
        self.velosityY = velosityY
        self.life = life
        self.degrees = 0
        self.degreesSpeed = degreesSpeed
        self.asteroidVertexOriginal = [[item[0] // sizeMod , item[1]] for item in asteroidVertexOriginal]
        self.asteroidVertex = [item for item in self.asteroidVertexOriginal]
        self.sizeMod = sizeMod
        self.uid = uid

        for item in self.asteroidVertexOriginal:
            if item[1] == 0:
                self.radius = int( sqrt( ( self.x - (self.x + self.asteroidVertexOriginal[0][0] * sin(radians(self.asteroidVertexOriginal[0][1]))) ) ** 2 + ( self.y - (self.y + self.asteroidVertexOriginal[0][0] * cos(radians(self.asteroidVertexOriginal[0][1]))) ) ** 2 ) )

    def rotate (self):

        self.degrees += self.degreesSpeed

        if self.degrees >= 360:
            self.degrees = 0
        elif self.degrees < 0:
            self.degrees = 359

    def move (self):

        self.x += self.velosityX
        self.y += self.velosityY

        if self.x > WIN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIN_WIDTH

        if self.y > WIN_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = WIN_HEIGHT


    def draw (self, surface):

        for index in range(0, len(self.asteroidVertexOriginal)):

            deg = self.asteroidVertexOriginal[index][1] + self.degrees

            if deg > 360:
                deg = deg - 360

            if deg <= 90:
                angle = deg 
                coefx = 1
                coefy = 1

            elif deg > 90 and deg < 180:
                angle = 180 - deg 
                coefx = 1
                coefy = -1

            elif deg >= 180 and deg < 270:
                angle = deg - 180
                coefx = -1
                coefy = -1

            elif deg >= 270:
                angle = 360 - deg
                coefx = -1
                coefy = 1

            self.asteroidVertex[index] =  [int(self.x +  coefx * self.asteroidVertexOriginal[index][0] * sin(radians(angle))), int(self.y + coefy * self.asteroidVertexOriginal[index][0] * cos(radians(angle)))]

        pygame.draw.lines(surface, Color(self.color), False, self.asteroidVertex)


class SpaceShip:

    def __init__(self, x, y, color, velosityX, velosityY, life, degrees, sizeMod):

        self.x = x
        self.y = y
        self.color = color
        self.velosityX = velosityX
        self.velosityY = velosityY
        self.velosity = 0
        self.life = life
        self.degrees = degrees
        self.sizeMod = sizeMod

        self.shipVertexOriginal = [[item[0] // sizeMod , item[1]] for item in shipVertexOriginal]
        self.shipVertex = [item for item in self.shipVertexOriginal]

        self.points = list()
        

    def move (self, speed):

        self.velosity += speed

        if self.velosity < -MAXSPEED:
            self.velosity = -MAXSPEED
        elif self.velosity > MAXSPEED:
            self.velosity = MAXSPEED

        self.velosityX = int (self.velosity * sin(radians(self.degrees)))
        self.velosityY = int (self.velosity * cos(radians(self.degrees)))


        self.x += self.velosityX
        self.y += self.velosityY

        if self.x > WIN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIN_WIDTH

        if self.y > WIN_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = WIN_HEIGHT

        if self.velosity not in range(-1, 2):

            self.points.append(Point(self.x, self.y, self.color, FPS, self.sizeMod))


    def rotate (self, deg):

        self.degrees += deg

        if self.degrees >= 360:
            self.degrees = 0
        elif self.degrees < 0:
            self.degrees = 359

    def draw (self, surface):

        for index in range(0, len(self.shipVertexOriginal)):

            deg = self.shipVertexOriginal[index][1] + self.degrees

            if deg > 360:
                deg = deg - 360

            if deg <= 90:
                angle = deg 
                coefx = 1
                coefy = 1

            elif deg > 90 and deg < 180:
                angle = 180 - deg 
                coefx = 1
                coefy = -1

            elif deg >= 180 and deg < 270:
                angle = deg - 180
                coefx = -1
                coefy = -1

            elif deg >= 270:
                angle = 360 - deg
                coefx = -1
                coefy = 1

            self.shipVertex[index] =  [int(self.x +  coefx * self.shipVertexOriginal[index][0] * sin(radians(angle))), int(self.y + coefy * self.shipVertexOriginal[index][0] * cos(radians(angle)))]

        self.points = [ item for item in self.points if item.isDraw ]

        for point in self.points:
            point.draw(surface)

        pygame.draw.lines(surface, Color(self.color), True, self.shipVertex)

class Point:
    def __init__ (self, x, y, color, max_age, sizeMod):
        
        self.age = max_age
        self.ageStep = max_age // 10
        self.x = x
        self.y = y
        self.color = color
        self.isDraw = True
        self.sizeMod = sizeMod

    def draw(self, surface):

        pygame.draw.circle(surface, Color(self.color), (self.x, self.y), (self.age // self.ageStep) // (self.sizeMod // 2))
        self.age -= self.ageStep
        if self.age <= 0:
            self.isDraw = False    

class Bullet:

    def __init__ (self, x, y, color, velosity, power, degrees, sizeMod):

        self.x = x
        self.y = y
        self.color = color
        self.velosityX = int (velosity * sin(radians(degrees)))
        self.velosityY = int (velosity * cos(radians(degrees)))
        self.power = power
        self.sizeMod = sizeMod

        self.isDraw = True

        self.points = list()

    def move (self):

        self.x += self.velosityX
        self.y += self.velosityY

        self.points.append(Point(self.x, self.y, self.color, FPS, self.sizeMod))

        if (self.x not in range (0, WIN_WIDTH)) or (self.y not in range (0, WIN_HEIGHT)):
            self.isDraw = False
            del self

    def draw (self, surface):

        self.points = [ item for item in self.points if item.isDraw ]

        for point in self.points:
            point.draw(surface)

class Game:
    def __init__(self, caption, color = "#000000", frame_rate = 30, winHeight = 480, winWidth = 640):

        pygame.init()

        self.background_image = Surface((winWidth , winHeight))
        self.background_image.fill(Color(color))
        self.frame_rate = frame_rate
        
        self.surface = pygame.display.set_mode((winWidth , winHeight))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

        self.asteroids = list()
        self.maxNumAsteroids = 20
        self.asteroidUIN = 0

        self.bullet = list()

        self.spaceShip = list()
        self.spaceShipRotateSpeed = 2
        self.spaceShipRotate = 0
        self.spaceShipMoveSpeed = 1
        self.spaceShipMove = 0

        self.fontSize = 32
        self.font = pygame.font.Font(None, self.fontSize)

    def asteroidsPoleGeneration(self):

        if len(self.asteroids) < self.maxNumAsteroids // 2:
            for num in range(self.maxNumAsteroids - len(self.asteroids)):
                self.asteroidUIN += 1
                self.asteroids.append(Asteroid(random.randint(0, WIN_WIDTH), random.randint(0, WIN_HEIGHT), colorRed, random.randint(-2, 2), random.randint(-2, 2), 100, random.randint(-6, 6), random.randint(1, 5), self.asteroidUIN))


    def asteroidDestroy(self):

        for asteroid in self.asteroids:
            for bullet in self.bullet:

                if ( sqrt( (asteroid.x - bullet.x) ** 2 + (asteroid.y - bullet.y) ** 2  ) ) < asteroid.radius:
                    
                    
                    if asteroid.sizeMod < 5:
                        self.asteroidUIN += 1
                        vx = random.choice((-1, 1))
                        vy = random.choice((-1, 1))
                        self.asteroids.append(Asteroid(asteroid.x, asteroid.y, colorRed, -vx * asteroid.velosityX, vy * asteroid.velosityY, 100, random.randint(-6, 6), asteroid.sizeMod + 1, self.asteroidUIN))
                        self.asteroids.append(Asteroid(asteroid.x, asteroid.y, colorRed, vx * asteroid.velosityX, -vy * asteroid.velosityY, 100, random.randint(-6, 6), asteroid.sizeMod + 1, self.asteroidUIN))

                    asteroid.life = 0
                    bullet.isDraw = False


    def asteroidCollission(self):

        for selfAsteroid in self.asteroids:
            for otherAsteroid in self.asteroids:
                if selfAsteroid.uid != otherAsteroid.uid:

                    if ( sqrt( (selfAsteroid.x - otherAsteroid.x) ** 2 + (selfAsteroid.y - otherAsteroid.y) ** 2  ) ) < selfAsteroid.radius + otherAsteroid.radius:

                        selfAsteroid.velosityX = random.choice((-1, 0, 1))
                        selfAsteroid.velosityY = random.choice((-1, 0, 1))

    def handle_events(self):
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_LEFT:
                
                self.spaceShipRotate = self.spaceShipRotateSpeed
                
            if event.type == KEYUP and event.key == K_LEFT:
                
                self.spaceShipRotate = 0
                
            if event.type == KEYDOWN and event.key == K_RIGHT:
                
                self.spaceShipRotate = -self.spaceShipRotateSpeed
                
            if event.type == KEYUP and event.key == K_RIGHT:
                
                self.spaceShipRotate = 0

            if event.type == KEYDOWN and event.key == K_UP:
                
                self.spaceShipMove = self.spaceShipMoveSpeed
                
            if event.type == KEYUP and event.key == K_UP:
                
                self.spaceShipMove = 0

            if event.type == KEYDOWN and event.key == K_DOWN:
                
                self.spaceShipMove = -self.spaceShipMoveSpeed
                
            if event.type == KEYUP and event.key == K_DOWN:
                
                self.spaceShipMove = 0

            if event.type == KEYDOWN and event.key == K_SPACE:

                bigShot = random.randint (-1, 1)
                
                for ship in self.spaceShip:
                    if ship.life:
                        if bigShot != 0:
                            self.bullet.append(Bullet(ship.x, ship.y, colorBlue, int(MAXSPEED * 1.5), 1, ship.degrees, 5))
                        else:
                            self.bullet.append(Bullet(ship.x, ship.y, colorBlue, int(MAXSPEED * 1.5), 1, ship.degrees - 10, 5))
                            self.bullet.append(Bullet(ship.x, ship.y, colorBlue, int(MAXSPEED * 1.5), 1, ship.degrees, 5))
                            self.bullet.append(Bullet(ship.x, ship.y, colorBlue, int(MAXSPEED * 1.5), 1, ship.degrees + 10, 5))


    def rotate (self):

        for asteroid in self.asteroids:
            if asteroid.life:
                asteroid.rotate()

        for ship in self.spaceShip:
            if ship.life:
                ship.rotate(self.spaceShipRotate)

    def move (self):

        for asteroid in self.asteroids:
            if asteroid.life:
                asteroid.move()

        for ship in self.spaceShip:
            if ship.life:
                ship.move(self.spaceShipMove)

        for bullet in self.bullet:
            if bullet.isDraw:
                bullet.move()

    def draw (self):

        for asteroid in self.asteroids:
            if asteroid.life:
                asteroid.draw(self.surface)

        for ship in self.spaceShip:
            if ship.life:
                ship.draw(self.surface)

        for bullet in self.bullet:
            if bullet.isDraw:
                bullet.draw(self.surface)


    def run (self):

        while (True):

            self.bullet = [ item for item in self.bullet if item.isDraw ]
            self.spaceShip = [ item for item in self.spaceShip if item.life]
            self.asteroids = [ item for item in self.asteroids if item.life]

            #print (len(self.bullet), len (self.asteroids), len (self.spaceShip))

            self.surface.blit(self.background_image, (0, 0))

            speed_text = self.font.render("SPEED: " + " ".join( [ str(item.velosity) for item in self.spaceShip ] ), 1, Color(colorGreen))
            self.surface.blit(speed_text, (0, 0))
            asteroid_text = self.font.render("NUMBER OF ASTEROID IN POLE: " + str(len(self.asteroids)), 1, Color(colorGreen))
            self.surface.blit(asteroid_text, (0, 50))

            self.asteroidCollission ()
            self.asteroidDestroy ()
            self.asteroidsPoleGeneration ()

            self.handle_events ()


            self.rotate ()
            self.move ()
            self.draw ()

            

            pygame.display.update ()           
            self.clock.tick (self.frame_rate)


def main():

    game = Game ("SPACE !", colorBlack, FPS, WIN_HEIGHT, WIN_WIDTH)

    game.spaceShip.append(SpaceShip(CENTERX, CENTERY, colorRed, 0, 0, 100, 0, 5))

    
    
    
    game.run ()

    


if __name__ == "__main__":

    pygame.display.init()
    dispModes = pygame.display.list_modes()

    currentMode = dispModes[len (dispModes) // 3 - 1]

    WIN_WIDTH = currentMode[0]
    WIN_HEIGHT = currentMode[1]
    CENTERX = WIN_WIDTH // 2
    CENTERY = WIN_HEIGHT // 2

    print(WIN_WIDTH, WIN_HEIGHT, CENTERX, CENTERY)

    
    main()