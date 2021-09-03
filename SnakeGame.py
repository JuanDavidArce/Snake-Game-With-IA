from collections import namedtuple, deque
from random import choice, randint
from time import sleep
from os import system
from blessed import Terminal


# ALIAS
Pto = namedtuple('Point', ('y', 'x',))


# WORM MODEL
class Worm:
    def __init__(self, positionHead):
        self.positionHead = positionHead
        self.ubications = deque([positionHead, ])
        self.movingOptions = ['l', 'r', 'u', 'd']
        self.actualDirection = 'l'

    def selectDirection(self):
        return choice(self.movingOptions)

# COOKIE MODEL


class Cookie:
    def __init__(self, position):
        self.position = position

    def generateNewPosition(self, width, height, ubications):
        while True:
            newPosition = Pto(randint(0, height-1), randint(0, width-1))
            if newPosition not in ubications:
                self.position = newPosition
                break


# ENVIRONMENT MODEL
class Environment:
    def __init__(self, width, height):
        self.square = [['.']*width for i in range(height)]
        self.width = width
        self.height = height

    def newPosition(self, pos, character):
        self.square[pos.y][pos.x] = character

    def deletePosition(self, pos):
        self.square[pos.y][pos.x] = '.'

    def printSquare(self,term):
        #speed
        sleep(0.1)
        print(term.home)
        for row in self.square:
            for column in row:
                if column=='.':
                    print(term.blue_reverse(' '),end='')
                elif column=='*':
                    print(term.red_reverse(' '),end='')
                elif column=='$':
                    print(term.yellow_reverse(' '), end='')
                else:
                    print(term.black_reverse(' '),end='')
            print()
                
        

# FUNCTIONS
def selectPositionHead(worm, env):
    x=worm.positionHead.x
    y=worm.positionHead.y
    direc=worm.actualDirection
    while True:
        direction = worm.selectDirection()
        if direction == 'l' and direc != 'r':
            if x-1 >= 0 and env.square[y][x-1] != '*':
                return Pto(y,x-1), direction
        if direction == 'r' and direc != 'l':
            if x+1 <= env.width-1 and env.square[y][x+1] != '*':
                return Pto(y,x+1), direction
        if direction == 'u' and direc != 'd':
            if y-1 >= 0 and env.square[y-1][x] != '*':
                return Pto(y-1, x), direction
        if direction == 'd' and direc != 'u':
            if y+1 <= env.height-1 and env.square[y+1][x] != '*':
                return Pto(y+1,x), direction


def CookieEaten(cookie, worm):
    return cookie.position == worm.positionHead




# ENTRY POINT
def main():
    # @= head, *= body, $=cookie ,.=map
    #Interface to draw
    term=Terminal()
    # initial envirioment
    env = Environment(20, 10)
    worm = Worm(Pto(env.height//2, env.width//2))
    env.newPosition(worm.positionHead, "@")
    cookie = Cookie(Pto(worm.positionHead.y, worm.positionHead.x-2))
    env.newPosition(cookie.position, "$")
    print(term.clear)

    # Moving the worm
    while True:
        worm.positionHead, worm.actualDirection = selectPositionHead(worm, env)
        if CookieEaten(cookie, worm):
            toAdd = worm.positionHead
            worm.ubications.appendleft(toAdd)
            cookie.generateNewPosition(env.width, env.height, worm.ubications)
            env.newPosition(cookie.position, "$")
        else:
            toDelete = worm.ubications.pop()
            toAdd = worm.positionHead
            worm.ubications.appendleft(toAdd)
            env.deletePosition(toDelete)

        # update the square
        if len(worm.ubications) > 1:
            env.newPosition(worm.ubications[1], "*")
        env.newPosition(toAdd, "@")
        env.printSquare(term)

main()
