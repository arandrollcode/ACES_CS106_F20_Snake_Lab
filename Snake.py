## Snake Game

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

##----------------------------------------------------------------------------##
## Heading Constants
## (x_direction, y_direction)
STOP  = (0, 0)
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)

## Colors Constants (r, g, b)
BLACK = (0, 0, 0)
GREY  = (50, 50, 50)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

##----------------------------------------------------------------------------##

## Game Dimensions (Pixels)
WINDOW_WIDTH   = 850
WINDOW_HEIGHT  = 600
TILE_DIMENSION = 25

if WINDOW_WIDTH % TILE_DIMENSION != 0:
    print('ERROR: TILE_DIMENSION must evenly divide WINDOW_WIDTH!')
    print('Stopping Program')
    exit()

if WINDOW_HEIGHT % TILE_DIMENSION != 0:
    print('ERROR: TILE_DIMENSION must evenly divide WINDOW_HEIGHT!')
    print('Stopping Program')
    exit()

## Size of tile grid
ROWS    = WINDOW_HEIGHT / TILE_DIMENSION
COLUMNS = WINDOW_WIDTH  / TILE_DIMENSION

##----------------------------------------------------------------------------##

## Tile Object
## Tile.position: (x, y) coordinates of the tile
## Tile.heading:  (x, y) direction that the snake is moving
## Tile.color:    Color of the tile

class Tile:
    def __init__(self, position, heading, color):
        self.position = position
        self.heading = heading
        self.color = color

    ## Draw the Tile on the surface
    def draw(self, surface):
        x = int(self.position[0])
        y = int(self.position[1])

        pygame.draw.rect(surface, self.color, (x * TILE_DIMENSION - 1, \
                                               y * TILE_DIMENSION - 1, \
                                               TILE_DIMENSION - 2,     \
                                               TILE_DIMENSION - 2))

    ## Draw eyes on the Tile
    def draw_eyes(self, surface):
        x = int(self.position[0])
        y = int(self.position[1])
        centre = TILE_DIMENSION // 2
        radius = 3
        leftEye  = (x * TILE_DIMENSION + centre - 2*radius, \
                    y * TILE_DIMENSION + TILE_DIMENSION // 3)
        rightEye = (x * TILE_DIMENSION + centre + radius, \
                    y * TILE_DIMENSION + TILE_DIMENSION // 3)
        
        pygame.draw.circle(surface, BLACK, leftEye, radius)
        pygame.draw.circle(surface, BLACK, rightEye, radius)

    ## Set the Tile heading and move Tile one step in that direction
    def move(self, heading):
        self.heading = heading

        ## TODO: Calculate the new position
        x_pos = self.heading[0]
        y_pos = self.heading[1]

        x_pos_snake = self.position[0]
        y_pos_snake = self.position[1]
        

        self.position = (x_pos_snake + x_pos, y_pos_snake + y_pos)

##----------------------------------------------------------------------------##

## Snake Object
## Snake.head:   First Tile of the snake
## Snake.body:   List of Tiles that make the snake
## Snake.color:  Color of the snake
## Snake.turnAt: Positions where the snake changes directions

class Snake:
    def __init__(self, position, color=RED):
        self.head = Tile(position, STOP, color)
        self.body = [self.head]
        self.color = color
        self.turnAt = dict()

    ## Moves each tile of the snake so the entire snake moves one step
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
 
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                if self.head.heading != DOWN:
                    self.turnAt[self.head.position[:]] = UP
            elif keys[pygame.K_DOWN]:
                if self.head.heading != UP:
                    self.turnAt[self.head.position[:]] = DOWN
            elif keys[pygame.K_LEFT]:
                if self.head.heading != RIGHT:
                    self.turnAt[self.head.position[:]] = LEFT
            elif keys[pygame.K_RIGHT]:
                if self.head.heading != LEFT:
                    self.turnAt[self.head.position[:]] = RIGHT

        for segment in self.body:
            position = segment.position
            if position in self.turnAt:
                heading = self.turnAt[position]
                segment.move(heading)
                if segment is self.body[-1]:
                    del self.turnAt[position]
            else:
                segment.move(segment.heading)

    def draw(self, surface):       
        for segment in self.body:
            segment.draw(surface)

        self.head.draw_eyes(surface)

    ## Add a tile to the end of the snake
    def addSegment(self):
        self.heading = self.body[len(self.body)-1].heading
        if self.heading == UP:
            self.opposite = DOWN
        elif self.heading == RIGHT:
            self.opposite = LEFT
        elif self.heading == DOWN:
            self.opposite = UP
        elif self.heading == LEFT:
            self.opposite = RIGHT
        self.last_x = self.body[len(self.body)-1].position[0] #current last block on snake (x)
        self.last_y = self.body[len(self.body)-1].position[1] #current last block on snake (y)

        self.direct_x = self.opposite[0] #direction (x)
        self.direct_y = self.opposite[1] #direction (y)

        self.new_x = self.last_x + self.direct_x #new (x)
        self.new_y = self.last_y + self.direct_y #new (y)

        self.body.append(Tile((self.new_x,self.new_y),self.heading, self.color))
    
##----------------------------------------------------------------------------##

## Object that runs the game
## SnakeGame.snake:  A Snake object that the player controls
## SnakeGame.food:   A Tile object that the snake tries to eat
## SnakeGame.window: The window that the game runs in
class SnakeGame:
    def __init__(self):
        ## TODO: The game needs a snake!
        self.snake = Snake((1, ROWS - 2))
        ## TODO: Make a green tile to represent the food
        ## The position of the food tile should be randomly generated using randomPosition()
        self.food = Tile((self.randomPosition()), STOP, GREEN)
        
        
    ## Draws the next frame of the game
    def redrawWindow(self, surface):
        surface.fill((50,50,50))
        self.food.draw(surface)
        self.snake.draw(surface)
        pygame.display.update()


    ## Generate a random position that is not occupied
    def randomPosition(self):
        ## TODO: Generate a random (x, y) position
        x = 1 
        y = 1

        ## TODO: Make sure that the snake is not already at (x, y)
        ## Keep generating random positions until we find an empty position
        x = random.randint(1, COLUMNS-2)
        y = random.randint(1, ROWS-2)
        
        for self.block in self.snake.body:
            if self.block.position[0] == x and self.block.position[1] == y:
                self.randomPosition()

        return x, y


    ## Return True if the snake has run into itself
    def game_over(self):
        snake = self.snake
    
        ## TODO: Check if any part of the snake is overlapping            
        for i in range(0, len(snake.body)):
            for m in range(i+1, len(snake.body)):
                i_thing = snake.body[i]
                m_thing = snake.body[m] 
                if (i_thing.position[0] == m_thing.position[0] and
                    i_thing.position[1] == m_thing.position[1]):
                    return True
        return False


    ## Detect if the snake has gotten food
    ## Return True if the snake has gotten food
    ## Return False if the snake has not gotten food
    def snake_on_food(self):
        snake = self.snake
        food = self.food
        for block in snake.body:
            if (block.position[0] == food.position[0] and
                block.position[1] == food.position[1]):
                return True
        return False

    
    ## Check if the snake has left the screen
    ## Return True if the snake has left the screen
    ## Return False if the snake is still on screen
    def check_bounds(self):
        snake = self.snake
        
        for block in snake.body:
            if (block.position[0] < 0 or block.position[0] == COLUMNS or
            block.position[1] < 0 or block.position[1] == ROWS):
                return True        
        return False
        
    ## Run the game
    def start(self):
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        clock = pygame.time.Clock()

        snake = self.snake
        food = self.food
        
        while True:
            clock.tick(12)
            snake.move()
            out_of_bounds = self.check_bounds()
            
            if self.snake_on_food():
                ## TODO: If the snake has gotten the food, grow the snake
                ## Also, move the food to a random new position                
                self.food = Tile((self.randomPosition()),STOP,GREEN)
                snake.addSegment()
                
            if out_of_bounds or self.game_over():
                print('Game Over\nScore: {0}\nUse \"snake_game.start()\" to play again.'.format(len(snake.body)))
                self.__init__()
                return

            self.redrawWindow(window)

##----------------------------------------------------------------------------##

## Main
if __name__ == "__main__":
    snake_game = SnakeGame()
    snake_game.start()
