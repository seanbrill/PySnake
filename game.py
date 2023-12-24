import tkinter as tk
import math
import random
from audio import AudioPlayer
from player import Player
from static import canvas_height
from static import canvas_width
from static import square_px
from static import user_input_frequency
from static import easy_speed
from static import normal_speed
from static import hard_speed
from static import player_data

class GameManager:

    instance : 'GameManager' = None
    UIController = None
    GameOver = False
    player = None
    GameDifficulty = None
    PersonalBest = None
    PersonalBestDifficulty = None
    direction = (1,0) # defaults the snake in the +x direction
    tick_speed = normal_speed
    appleIsSpawned = False
    applePosition = None

    # Game Settings
    snake_color = None
    food_color = None
    rainbow_snake = False
    slither_sound_enabled = False
    eat_sound_enabled = False

    def __init__(self, UIController):
        print('game manager initialized')
        self.UIController = UIController
        GameManager.instance = self
        self.PersonalBest = self.GetPersonalHighScore()

    def draw_square(self, x, y, color="white"):
        x1, y1 = x * square_px, y * square_px
        x2, y2 = x1 + square_px, y1 + square_px
        self.UIController.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def StartGame(self, difficulty):
        global user_input_frequency
        global easy_speed
        global normal_speed
        global hard_speed
        if difficulty == 1:
            self.tick_speed = easy_speed
            self.GameDifficulty = 'Easy'
        if difficulty == 2:
            self.tick_speed = normal_speed
            self.GameDifficulty = 'Normal'
        if difficulty == 3:
            self.tick_speed = hard_speed
            self.GameDifficulty = 'Hard'
        self.direction = (1,0)

        # init settings
        self.snake_color = self.UIController.rgba_to_hex(eval(self.GetContext('snake_color')))
        self.food_color = self.UIController.rgba_to_hex(eval(self.GetContext('food_color')))
        self.rainbow_snake = eval(self.GetContext('rainbow_snake'))
        self.slither_sound_enabled = eval(self.GetContext('enable_slither_sound'))
        self.eat_sound_enabled = eval(self.GetContext('enable_food_sound'))

        # start the player
        if self.player:
            del self.player
        self.player = Player(self.UIController.canvas, self.UIController.score_text, self.snake_color, self.rainbow_snake)
        self.GameOver = False

        self.UIController.score_text.config(text=("Score: " + str(self.player.player_score)))

        self.UIController.window.bind("<KeyPress>", self.key_press)
        self.UIController.window.after(user_input_frequency, self.onUserInput)
        self.UIController.window.after(int(self.tick_speed * 1000), self.GameLoop)

        self.UIController.easy_button.place_forget()
        self.UIController.normal_button.place_forget()
        self.UIController.hard_button.place_forget()
        self.UIController.leaderboard_button.place_forget()
        self.UIController.info_button.place_forget()
        self.UIController.settings_button.place_forget()

    def key_press(self, event):
            key = event.keysym
            if key == "Right" or key.lower() == 'd':
                self.direction = (1,0)
            elif key == "Left" or key.lower() == 'a':
                self.direction = (-1,0)
            elif key == "Up" or key.lower() == 'w':
                self.direction = (0,-1)
            elif key == "Down" or key.lower() == 's':
                self.direction = (0,1)

    def onUserInput(self):
        global user_input_frequency
        if not self.GameOver:
            self.UIController.window.update()
            self.UIController.window.after(user_input_frequency, self.onUserInput)

    def GameLoop(self):
        if not self.GameOver:
            #increment frame count
            self.player.Move(self.direction[0], self.direction[1])
            if self.slither_sound_enabled:
                AudioPlayer.instance.Play(Player.moveSound , 'move')
            if not self.appleIsSpawned:
                self.SpawnApple()
            # check if the player reaches the apple with the head
            if len(self.player.body_positions) > 0 and self.CompareDistance(self.player.body_positions[-1], self.applePosition) <= 0.25:
                self.player.Grow()
                if self.eat_sound_enabled:
                    AudioPlayer.instance.Play(Player.eatSound)
                self.DestroyApple()
                # update the high score if the player beat it
                currentScore = self.GetCurrentScore()
                if currentScore > self.PersonalBest:
                    self.PersonalBest = currentScore
                    self.PersonalBestDifficulty = self.GameDifficulty
                    self.UIController.UpdateHighScore()
            # check for player death
            if self.player.player_health == 0:
                self.GameOver = True
                AudioPlayer.instance.StopAll()
                self.SubmitPersonalScore()
                self.UIController.ShowGameOver()
            # continue game loop if player is still alive
            else:
                self.UIController.window.after(int(self.tick_speed * 1000), self.GameLoop)

    def CompareDistance(self, posA, posB):
        #distance formula for 2 xy points 
        distance = math.sqrt(((posB[0] - posA[0])**2)  + ((posB[1] - posA[1])**2))
        #print('distance to food : ' + str(distance))
        return distance

    def SpawnApple(self):
        x = random.randrange(0, (canvas_width // (square_px) - 1))
        y = random.randrange(0, (canvas_height // (square_px) - 1))
        if (x,y) in self.player.GetBodyPositions():
            self.SpawnApple()
        else:
            self.applePosition = (x,y)
            _color = 'red'
            if self.food_color:
                _color = self.food_color
            self.draw_square(x,y,_color)
            print('apple spawned at :' + str(self.applePosition))
            self.appleIsSpawned = True

    def DestroyApple(self):
        self.draw_square(self.applePosition[0],self.applePosition[1],self.snake_color)
        self.appleIsSpawned = False

    def GetCurrentScore(self):
        return self.player.player_score

    def GetPersonalHighScore(self):
        context = self.GetContext('high_score')
        if context == None:
            self.SetContext('high_score', (0,'Easy'))
            context = self.GetContext('high_score')
        key_value = eval(context)
        best_score = key_value[0]
        difficulty = key_value[1]
        self.PersonalBestDifficulty = difficulty
        return best_score

    def SubmitPersonalScore(self):
        score = self.GetCurrentScore()
        difficulty = self.GameDifficulty
        old_best = eval(self.GetContext('high_score'))[0]
        if score > old_best:
            self.SetContext('high_score', (score, difficulty))

    def GetContext(self, key='all', file_path=player_data):
        try:
            print('player data file path :' + file_path)
            with open(file_path, 'r') as file:
                lines = file.readlines()
            if key == 'all':
                return lines
            else:
                for line in lines:
                    k = line.split('=')[0].strip()
                    v = line.split('=')[1].strip()
                    if k == key:
                        return v
                return None
        except FileNotFoundError:
            # Return an empty list if the file doesn't exist
            print('error')
            return None

    def SetContext(self, key, value, file_path=player_data):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            found = False
            for i, line in enumerate(lines):
                k = line.split('=')[0].strip()
                if k == key:
                    lines[i] = f"{key} = {value}\n"
                    found = True
                    break

            if not found:
                lines.append(f"{key} = {value}\n")

            with open(file_path, 'w') as file:
                file.writelines(lines)

            print(f"Context updated successfully for key: {key}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error updating context: {e}")

