import tkinter as tk
from static import starting_player_size
from static import gameboard_size
from static import canvas_height
from static import canvas_width
from static import square_px


class Player:

    color = None
    isRainbow = False
    rainbow_colors = ['red','orange','yellow','green','blue','indigo','violet']
    rianbow_index = 3 # start at green
    player_health = 1
    #default length of snake
    player_size = starting_player_size
    player_score = 0
    body_positions = []
    score_text = None
    #these variables allow the snake to keep
    #moving in its previous direction
    #if the incoming direction is not valid (player turns in on its neck)
    prevXChange = 0
    prevYChange = 0

    moveSound = './assets/audio/effect1.wav'
    eatSound = './assets/audio/effect3.wav'

    def __init__(self, canvas : tk.Canvas, scoreText : tk.Label, color, isRainbow = False):
        self.canvas : tk.Canvas = canvas
        self.body_positions = []
        self.player_health = 1
        self.player_score = 0
        self.score_text = scoreText
        self.color = color
        self.isRainbow = isRainbow
        self.SpawnPlayer(canvas_height, canvas_width)
          
    def draw_square(self, x, y, color = None):
        x1, y1 = x * square_px, y * square_px
        x2, y2 = x1 + square_px, y1 + square_px
        if color == None and self.color:
            # custom snake color
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color)
        else:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def SpawnPlayer(self, height, width):
        x1 = (width // 2) // (square_px) - 3
        x2 = ((width // 2) // (square_px)) - 2
        x3 = ((width // 2) // (square_px)) - 1
        y = (height // 2) // (square_px)

        self.body_positions.append((x1, y))
        self.body_positions.append((x2, y))
        self.body_positions.append((x3, y))

        self.draw_square(x1, y)
        self.draw_square(x2, y)
        self.draw_square(x3, y)

    def Move(self, xChange = 1, yChange = 0):
        if not self.canvas: return
        if self.player_health < 1:
            #player is dead
            return
        #delete tail body part from the self.canvas
        self.draw_square(self.body_positions[0][0], self.body_positions[0][1], 'black')
        #draw the snake 
        pos = self.body_positions[-1]
        x = pos[0] + xChange
        y = pos[1] + yChange
        if (x < 0 or x >= gameboard_size) or (y < 0 or y >= gameboard_size):
            self.Die()
            return
        #don't allow the head to turn in on it's neck
        if (x,y) == self.body_positions[-2]:
            self.Move(self.prevXChange, self.prevYChange)
            return
        if (x,y) in self.body_positions:
            self.Die()
            return
        self.body_positions.append((x,y))
        if self.isRainbow:
            if self.rianbow_index > len(self.rainbow_colors) - 1:
                self.rianbow_index = 0
            self.draw_square(x,y, self.rainbow_colors[self.rianbow_index])
            self.rianbow_index += 1
        else:
            self.draw_square(x,y)
        #set PrevX and Y
        self.prevXChange = xChange
        self.prevYChange = yChange
        #clean up body positions
        while len(self.body_positions) > self.player_size:
            self.body_positions.pop(0)
    
    def Grow(self):
        print('growing!')
        self.body_positions.insert(0, self.body_positions[0])
        self.player_size+=1 
        self.player_score += 1
        self.score_text.config(text=("Score: " + str(self.player_score)))

    def TakeDamage(self, damage):
        self.player_health -= damage

    def Die(self):
        self.player_health = 0
        print('Player Died')

    def __del__(self):
        for bodyPart in self.body_positions:
            self.draw_square(bodyPart[0], bodyPart[1], 'black')
        
    def GetBodyPositions(self):
        return self.body_positions



