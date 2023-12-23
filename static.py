import tkinter as tk
starting_player_size = 3
gameboard_size = 20
square_px = 20
canvas_height = square_px * gameboard_size
canvas_width = square_px * gameboard_size
user_input_frequency = 100 #update frequency in ms
easy_speed = 0.20
normal_speed = 0.12
hard_speed = 0.095
window_color = '#101010'
leaderboard_alt_color = '#3c3c3c'
player_data = 'player_data.txt'
info_text = '''
PySnake is a captivating snake game built in Python using tkinter. 
Maneuver the snake with either the WASD keys or Arrow keys. 
Your objective: collect food to accumulate points and extend the snake's length. But beware! 
Touching your own body or the walls ends the game. 
Post your name on the leaderboard after each game and see how you stack up against players worldwide. 
The leaderboard also showcases the difficulty of each player's score with color-coding (Green: Easy, Orange: Normal, Red: Hard). 
Who will claim the title of the ultimate PySnake player?

Customize your gaming experience on the settings page by adjusting the snake color, food color, and sounds to match your preferences.
Reach a top score of at least 100 to unlock the coveted Rainbow Snake for an extra touch of excitement. 

Developed by Sean Brill using Python and tkinter for the UI and gameplay, 
the backend services leverage Azure Cloud Functions with Node.js. 
Explore the code on GitHub, and for more information, visit my website at https://seanbrill.com. 

Copyright [year].
'''

