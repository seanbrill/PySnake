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
PySnake, an enthralling snake game crafted in Python with the tkinter library, beckons players into a thrilling challenge. Navigate the snake gracefully using either the WASD keys or Arrow keys. Your mission: gather food to accrue points and elongate the snake, but exercise caution! Colliding with your own body or the walls brings the game to an abrupt end.

After each intense round, etch your name onto the leaderboard and measure your prowess against competitors from around the globe. The leaderboard cleverly uses color-coding (Green: Easy, Orange: Normal, Red: Hard) to denote the difficulty of each player's score. Who will emerge as the ultimate PySnake virtuoso?

Delve into a personalized gaming venture on the settings page by tweaking the snake color, food color, and sounds to align with your preferences. Achieve a stellar score of at least 100 to unlock the coveted Rainbow Snake, adding an extra layer of excitement to your gameplay.

Developed by Sean Brill, PySnake marries Python and tkinter for an immersive UI and gameplay experience. Behind the scenes, Azure Cloud Functions with Node.js power the game's backend services.

Contact: seanbrill54@gmail.com
Website: https://seanbrill.com
Github : https://github.com/seanbrill/PySnake

Copyright © 2023 Sean Brill.
'''

