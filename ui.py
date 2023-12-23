# Import the necessary modules from Tkinter
import tkinter as tk
from tkcolorpicker import askcolor  # Import the color picker
from game import GameManager
from api import HttpManager
from static import canvas_height
from static import canvas_width
from static import window_color
from static import leaderboard_alt_color
from static import info_text

class UIController:

    # All UI Elements
    window = None
    canvas = None
    header_text = None
    default_header_text = "Welcome To PySnake!"
    score_text = None
    high_score_text_label = None
    high_score_text_value = None
    easy_button = None
    normal_button = None
    hard_button = None

    # leaderboard ui elements
    leaderboard_frame = None
    leaderboard_canvas = None
    leaderboard_scrollbar = None
    leaderboard_error_text = None


    scrollbar = None
    back_button = None # used in multiple views
    game_over_text = None
    name_label = None
    name_input = None
    submit_button = None
    leaderboard_button = None
    info_button = None
    settings_button = None
    info_text_box = None

    # settings ui elements
    snake_color_label = None
    snake_color_button = None
    snake_color_canvas = None

    food_color_label = None
    food_color_button = None
    food_color_canvas = None

    unlock_message_label = None
    enable_rainbow_snake_checkbox = None
    enable_slither_sound_checkbox = None
    enable_eat_sound_checkbox = None
    save_button = None

    # setting variables to pass to GameManager

    SNAKE_COLOR = None
    FOOD_COLOR = None
    RAINBOW_SNAKE = None
    ENABLE_SLITHER_SOUND = None
    ENABLE_FOOD_SOUND = None


    # constructor
    def __init__(self):
        print('ui initialized')
 
    # start the ui loop
    def Start(self):
        self.window = tk.Tk()
        self.window.geometry('400x510')
        self.window.title('PySnake')
        self.window.resizable(False, False)
        self.window.configure(bg=window_color)
        self.InitializeUI()
        self.window.mainloop()

    def InitializeUI(self):
        # Header 
        self.header_text = tk.Label(self.window, text=self.default_header_text, font=('Terminal', 22, 'bold'),background=window_color,  fg='white')
        self.header_text.pack(pady=35)

        # create the game canvas
        self.canvas = tk.Canvas(self.window, width=canvas_width, height=canvas_height, bg="black")
        self.canvas.pack()
        
        # Score text label
        self.score_text = tk.Label(self.window, text='Score: 0', font=('Terminal', 10), fg='white', background=window_color)
        self.score_text.place(relx=0, rely=0.16, anchor=tk.NW)
        
        # High Score text label & value
        self.high_score_text_label = tk.Label(self.window, text=('High Score: '), font=('Terminal', 10), fg='white', background=window_color)
        self.high_score_text_label.place(relx=0.2, rely=0.16, anchor=tk.NW)

        self.high_score_text_value = tk.Label(self.window, text=(str(GameManager.instance.GetPersonalHighScore())), font=('Terminal', 10), fg=self.GetDifficultyColor(GameManager.instance.PersonalBestDifficulty), background=window_color, width=1, justify='left')
        self.high_score_text_value.place(relx=0.445, rely=0.1617, anchor=tk.NW)
        
        # Game Over Text
        self.game_over_text = tk.Label(self.canvas, text='Game Over', font=('Terminal', 22, 'bold'), background='black', fg='white')

        # Player Name Input
        self.name_label = tk.Label(self.canvas, text='Enter Your Name: ', font=('Terminal', 10), fg='white', background='black', justify='center')
        self.name_input = tk.Entry(self.canvas, font=('Terminal', 10), justify='center', background='black', fg='white', bd=0, insertbackground='white')
        self.submit_button = tk.Button(self.canvas, text='Submit', font=('Terminal', 12), fg='black', background='white', command=lambda: self.SubmitScore())

        # Start Game Butons
        self.easy_button = tk.Button(self.window, cursor='hand2', text="Easy", font=('Terminal', 18),bd=20, border='0', background='green', fg='white', command=lambda: GameManager.instance.StartGame(1))
        self.normal_button = tk.Button(self.window, cursor='hand2', text="Normal", font=('Terminal', 18),bd=20,border='0', background='orange', fg='white', command=lambda: GameManager.instance.StartGame(2))
        self.hard_button = tk.Button(self.window, cursor='hand2', text="Hard", font=('Terminal', 18),bd=20,border='0', background='red', fg='white', command=lambda: GameManager.instance.StartGame(3))

        # View Leaderboard button
        self.leaderboard_button = tk.Button(self.window, cursor='hand2', text="Leaderboard", font=('Terminal', 18), bd=20, border='0', background='white', fg='black', command=lambda: self.ViewLeaderboard())

        # Info Button
        self.info_button = tk.Button(self.window, cursor='hand2', text="ℹ", width=2, padx=5, font=('Terminal', 18), bd=20, border='0', background='white', fg='black', command=lambda: self.ViewInfoPage())

        # Settings Button
        self.settings_button = tk.Button(self.window, cursor='hand2', text="⚙", width=2, padx=5, font=('Terminal', 18, 'bold'), bd=20, border='0', background='white', fg='black', command=lambda: self.ViewSettingsPage())



        # Show start buttons
        self.ShowStartButtons()

    def GetDifficultyColor(self, difficulty):
        color = 'green'
        if difficulty.lower() == 'easy':
            color = 'green'
        if difficulty.lower() == 'normal':
            color = 'orange'
        if difficulty.lower() == 'hard':
            color = 'red'
        return color

    def ShowStartButtons(self):
        # Place the button in the center of the window
        self.easy_button.place(relx=0.23, rely=0.5, anchor=tk.CENTER)
        self.normal_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.hard_button.place(relx=0.77, rely=0.5, anchor=tk.CENTER)

        self.leaderboard_button.place(relx=0.375, rely=0.6, anchor=tk.CENTER)
        self.info_button.place(relx=0.69, rely=0.6, anchor=tk.CENTER)
        self.settings_button.place(relx=0.82, rely=0.6, anchor=tk.CENTER)

    def HideStartButtons(self):
        # Hide start buttons
        self.easy_button.place_forget()
        self.normal_button.place_forget()
        self.hard_button.place_forget()
        self.leaderboard_button.place_forget()
        self.info_button.place_forget()
        self.settings_button.place_forget()

    def ShowGameOver(self):
        # show text
        self.game_over_text.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        #show leaderboard inputs
        self.name_label.place(relx=0.5225, rely=0.45, anchor=tk.CENTER)
        self.name_input.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.name_input.focus()
        self.submit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def HideGameOver(self):
        # show text
        self.game_over_text.place_forget()

        #show leaderboard inputs
        self.name_label.place_forget()
        self.name_input.place_forget()
        self.submit_button.place_forget()

        self.UpdateHighScore()

    def SubmitScore(self):
       name = self.name_input.get()
       # Clear the inputted text
       self.name_input.delete(0, tk.END)
       score = GameManager.instance.GetCurrentScore()   
       if len(name) > 0:
        response = HttpManager.instance.submit_score(name, score, GameManager.instance.GameDifficulty)
        print('submit score response:' + str(response))
       self.HideGameOver()
       self.ShowStartButtons()

    def UpdateHighScore(self):
        # Update High Score Text
        self.high_score_text_value.config(text=(str(GameManager.instance.PersonalBest)), fg=self.GetDifficultyColor(GameManager.instance.PersonalBestDifficulty))

    def ViewMainUI(self):
        # Change header text to Leaderboard
        self.header_text.config(text=(self.default_header_text))

        # show canvas and destroy other widgets
        self.score_text.place(relx=0, rely=0.16, anchor=tk.NW)
        self.high_score_text_label.place(relx=0.2, rely=0.16, anchor=tk.NW)
        self.high_score_text_value.place(relx=0.445, rely=0.1617, anchor=tk.NW)
        self.canvas.pack()
        self.ShowStartButtons()

        # Update High Score Value
        self.UpdateHighScore()

    def HideMainUI(self):
        # Hide canvas and destroy other widgets
        self.score_text.place_forget()
        self.high_score_text_label.place_forget()
        self.high_score_text_value.place_forget()
        self.canvas.pack_forget()
        self.easy_button.place_forget()
        self.HideStartButtons()

    def ViewLeaderboard(self):
        # Change header text to Leaderboard
        self.header_text.config(text="Leaderboard")

        # Hide Main UI
        self.HideMainUI()

        # Create canvas
        self.leaderboard_canvas = tk.Canvas(self.window,background=window_color, bg=window_color)
        self.leaderboard_canvas.pack(expand=True, fill=tk.BOTH, pady=(15, 90))

        # Scrollbar 
        self.leaderboard_scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL,background=window_color,troughcolor=window_color, activebackground=window_color, command=self.leaderboard_canvas.yview)
        self.leaderboard_scrollbar.place(relx=1, rely=0.225, relheight=0.599, relwidth=0.033, anchor='ne')

        self.leaderboard_canvas.configure(yscrollcommand=self.leaderboard_scrollbar.set)

        # leaderboard frame
        self.leaderboard_frame = tk.Frame(self.leaderboard_canvas, background=window_color, width=canvas_width)

        # Insert leaderboard data into the Canvas
        get_leaderboard_response = HttpManager.instance.get_leaderboard()

        # Get number of rows in the leaderboard
        num_rows = len(get_leaderboard_response['leaderboard'])

        if get_leaderboard_response['success'] and  num_rows > 0:
            #spacer = tk.Frame(self.leaderboard_frame,height=(0 * num_rows), background=window_color)
            #spacer.pack()
            for i, player in enumerate(get_leaderboard_response['leaderboard'], start=1):
                # normalize leaderboard place values to have 2 digits
                i_display = f"{i:02d}"

                # normalize no name provided
                name = player.get('name', "N/A")

                # normalize score values to have 2 digits
                score = f"{player['score']:02d}"

                # Alternate Row Color
                _color = window_color if i % 2 == 0 else leaderboard_alt_color
        
                # Create a Label for each row directly on the Canvas
                row = tk.Frame(self.leaderboard_frame, background=_color)
                tk.Label(row,width=10, justify='center',fg='white', background=_color, text=i_display, font=('Terminal', 15)).pack(side=tk.LEFT, expand=True, fill=tk.X)
                tk.Label(row,width=10, justify='center', fg='white', background=_color, text=name, font=('Terminal', 15)).pack(side=tk.LEFT, expand=True, fill=tk.X)
                tk.Label(row,width=10, justify='center', fg=self.GetDifficultyColor(player['difficulty']), background=_color, text=score, font=('Terminal', 15)).pack(side=tk.LEFT, expand=True, fill=tk.X)
                
                row.pack(fill=tk.X, expand=True)

            self.leaderboard_canvas.create_window((canvas_width // 2) - 10, (num_rows * 12.2), anchor=tk.CENTER, window=self.leaderboard_frame, width=canvas_width)
            # Make sure you can scroll to see all rows
            self.leaderboard_canvas.configure(scrollregion=(0,0,0,canvas_height + (2.7 * num_rows)))
        else:
            self.leaderboard_canvas.pack_forget()
            self.leaderboard_scrollbar.place_forget()
            # Display "Cannot connect to Leaderboard" text
            self.leaderboard_error_text = tk.Label(self.window, text="Could not retrieve leaderboard", font=('Terminal', 12), bg=window_color, fg='white')
            self.leaderboard_error_text.pack(pady=100)

        # Create a Back button to return to the main game
        self.back_button = tk.Button(self.window, text="Back", font=('Terminal', 18), bd=20, border='0', background='white', fg='black', command=self.GoBack)
        self.back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def HideLeaderboard(self):

        # Change header text to Leaderboard
        self.header_text.config(text=(self.default_header_text))

        if self.leaderboard_canvas != None:
            self.leaderboard_canvas.destroy()

        if self.leaderboard_scrollbar != None:
            self.leaderboard_scrollbar.destroy()

        if self.leaderboard_error_text != None:
            self.leaderboard_error_text.pack_forget()

        self.back_button.place_forget()

        # Show the main user interface
        self.ViewMainUI()
         
    def ViewInfoPage(self):
        # Change header text to Leaderboard
        self.header_text.config(text=("Leaderboard"))

        # Hide Main UI
        self.HideMainUI()

        # Update Page Header
        self.header_text.config(text=('Info'))

        # Create info text box
        self.info_text_box = tk.Text(self.window, wrap=tk.WORD, width=100, height=40, background=window_color, fg='white', font=('Terminal', 10))
        self.info_text_box.pack(pady=(0,90))  # Adjust the padding as needed

        # Set initial text in the info box
        self.info_text_box.insert(tk.END, info_text)


        # Create a Back button to return to the main game
        self.back_button = tk.Button(self.window, text="Back", font=('Terminal', 18), bd=20, border='0', background='white', fg='black', command=self.GoBack)
        self.back_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def HideInfoPage(self):
        # Change header text to Leaderboard
        self.header_text.config(text=(self.default_header_text))

        if self.info_text_box != None:
            self.info_text_box.pack_forget()
        
    def ViewSettingsPage(self):
        # Change header text to Leaderboard
        self.header_text.config(text=("Settings"))

        # Hide Main UI
        self.HideMainUI()

        self.SNAKE_COLOR = eval(GameManager.instance.GetContext('snake_color'))
        self.FOOD_COLOR = eval(GameManager.instance.GetContext('food_color'))
        self.RAINBOW_SNAKE = tk.BooleanVar(self.window, value=eval(GameManager.instance.GetContext('rainbow_snake')))
        self.ENABLE_SLITHER_SOUND = tk.BooleanVar(self.window, value=eval(GameManager.instance.GetContext('enable_slither_sound')))
        self.ENABLE_FOOD_SOUND = tk.BooleanVar(self.window, value=eval(GameManager.instance.GetContext('enable_food_sound')))

        # Snake Color Label
        self.snake_color_label = tk.Label(self.window, text="Snake Color:",fg='white', background=window_color, font=('Terminal', 15))
        self.snake_color_label.place(relx=0.17, rely=0.26, anchor=tk.CENTER)

        # Snake Color Button
        self.snake_color_button = tk.Button(self.window, text="Choose", command=lambda: self.choose_snake_color(self.SNAKE_COLOR, self.snake_color_canvas), cursor='hand2', fg='white', background=window_color, font=('Terminal', 10))
        self.snake_color_button.place(relx=0.50, rely=0.26, anchor=tk.CENTER)

        # Snake Color Canvas
        self.snake_color_canvas = tk.Canvas(self.window, width=20, height=20, background=self.rgba_to_hex(self.SNAKE_COLOR))
        self.snake_color_canvas.place(relx=0.65, rely=0.26, anchor=tk.CENTER)

        # Food Color Label
        self.food_color_label = tk.Label(self.window, text="Food Color :",fg='white', background=window_color, font=('Terminal', 15))
        self.food_color_label.place(relx=0.17, rely=0.36, anchor=tk.CENTER)

        # Food Color Button
        self.food_color_button = tk.Button(self.window, text="Choose", command=lambda: self.choose_food_color(self.FOOD_COLOR, self.food_color_canvas), cursor='hand2', fg='white', background=window_color, font=('Terminal', 10))
        self.food_color_button.place(relx=0.50, rely=0.36, anchor=tk.CENTER)

        # Food Color Canvas
        self.food_color_canvas = tk.Canvas(self.window, width=20, height=20, background=self.rgba_to_hex(self.FOOD_COLOR))
        self.food_color_canvas.place(relx=0.65, rely=0.36, anchor=tk.CENTER)

        yModifier = 0

        # Enable Rainbow Snake
        if GameManager.instance.GetPersonalHighScore() >= 100:
            # Enabled
            yModifier = 0.10
            self.enable_rainbow_snake_checkbox = tk.Checkbutton(
                self.window,
                text="Rainbow Snake",
                background=window_color,
                font=('Terminal', 15),
                fg='white',
                selectcolor=window_color,
                highlightcolor=window_color,
                highlightbackground=window_color,
                highlightthickness=0,
                variable=self.RAINBOW_SNAKE
            )
            self.enable_rainbow_snake_checkbox.place(relx=0.22, rely=(0.56 - yModifier), anchor=tk.CENTER)
        else:
            # Disabled
            # Show a message
            message = "Achieve a high score of 100 to unlock rainbow snake!"
            self.unlock_message_label = tk.Label(
                self.window,
                text=message,
                font=('Terminal', 8),
                fg='red',
                background=window_color
            )
            self.unlock_message_label.place(relx=0.43, rely=0.46, anchor=tk.CENTER)

            self.enable_rainbow_snake_checkbox = tk.Checkbutton(
                self.window,
                text="Rainbow Snake",
                background=window_color,
                font=('Terminal', 15),
                fg='white',
                selectcolor=window_color,
                highlightcolor=window_color,
                highlightbackground=window_color,
                highlightthickness=0,
                state='disabled'  # Set the state to 'disabled'
            )
            self.enable_rainbow_snake_checkbox.place(relx=0.22, rely=0.56, anchor=tk.CENTER)

        # Enable Slither Sound
        self.enable_slither_sound_checkbox = tk.Checkbutton(self.window, text="Enable Slither Sound", variable=self.ENABLE_SLITHER_SOUND, background=window_color, font=('Terminal', 15), fg='white',selectcolor=window_color, highlightcolor=window_color, highlightbackground=window_color, highlightthickness=0)
        self.enable_slither_sound_checkbox.place(relx=0.30, rely=(0.66 - yModifier), anchor=tk.CENTER)

        # Enable Eat Sound
        self.enable_eat_sound_checkbox = tk.Checkbutton(self.window, text="Enable Eat Sound",variable=self.ENABLE_FOOD_SOUND, background=window_color, font=('Terminal', 15), fg='white',selectcolor=window_color, highlightcolor=window_color, highlightbackground=window_color, highlightthickness=0)
        self.enable_eat_sound_checkbox.place(relx=0.25, rely=(0.76 - yModifier), anchor=tk.CENTER)

        # Save and Back Buttons
        self.save_button = tk.Button(self.window, text="Save", font=('Terminal', 18), bd=20, border='0', background='white', fg='black', command=lambda : self.save_settings())
        self.save_button.place(relx=0.3, rely=0.9, anchor=tk.CENTER)

        self.back_button = tk.Button(self.window, text="Back", font=('Terminal', 18), bd=20, border='0', background='white', fg='black', command=self.GoBack)
        self.back_button.place(relx=0.7, rely=0.9, anchor=tk.CENTER)

    def choose_snake_color(self, var, canvas):
        color = askcolor(var)
        if color:
            t = tuple(color[0])
            self.SNAKE_COLOR = [t[0],t[1],t[2]]
            canvas.config(background=color[1])
    
    def choose_food_color(self, var, canvas):
        color = askcolor(var)
        if color:
             t = tuple(color[0])
             self.FOOD_COLOR = [t[0],t[1],t[2]]
             canvas.config(background=color[1])

    def rgba_to_hex(self, rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return "#{:02x}{:02x}{:02x}".format(r,g,b)

    def save_settings(self):
        # Save settings to a file or perform necessary actions
        GameManager.instance.SetContext('snake_color', self.SNAKE_COLOR)
        GameManager.instance.SetContext('food_color', self.FOOD_COLOR)
        GameManager.instance.SetContext('rainbow_snake', self.RAINBOW_SNAKE.get())
        GameManager.instance.SetContext('enable_slither_sound', self.ENABLE_SLITHER_SOUND.get())
        GameManager.instance.SetContext('enable_food_sound', self.ENABLE_FOOD_SOUND.get())
        #self.ViewSettingsPage()

    def HideSettingsPage(self):

        if self.snake_color_label:
            self.snake_color_label.place_forget()
            self.snake_color_button.place_forget()
            self.snake_color_canvas.place_forget()

        if self.food_color_label:
            self.food_color_label.place_forget()
            self.food_color_button.place_forget()
            self.food_color_canvas.place_forget()

        if self.unlock_message_label != None:
            self.unlock_message_label.place_forget()

        if self.enable_rainbow_snake_checkbox:   
            self.enable_rainbow_snake_checkbox.place_forget()
            self.enable_slither_sound_checkbox.place_forget()
            self.enable_eat_sound_checkbox.place_forget()
            self.save_button.place_forget()

    def GoBack(self):
        # Hide Other Screens
        self.HideInfoPage()
        self.HideSettingsPage()
        self.HideLeaderboard()
        # Show Main UI
        self.ViewMainUI()