# PySnake

Welcome to PySnake, an immersive Python classic snake game that brings the iconic gameplay to life with the power of tkinter. Not just your ordinary snake experience, PySnake incorporates a dynamic twist by integrating Node.js API functions for a public leaderboard, enabling you to compete and showcase your skills on a global stage.

## Gameplay

In PySnake, you'll maneuver the snake using either the WASD keys or Arrow keys. Your mission: collect food to accumulate points and extend the snake's length. But be cautious! Colliding with your own body or the walls marks the end of the game. After each exhilarating round, claim your spot on the leaderboard, where your achievements are color-coded (Green: Easy, Orange: Normal, Red: Hard), allowing you to gauge your performance against players worldwide. Will you rise to the challenge and secure the title of the ultimate PySnake player?

## Customization

PySnake offers a personalized gaming experience with a settings page where you can customize the snake color, food color, and sounds to match your preferences. Reach a top score of at least 100 to unlock the coveted Rainbow Snake, injecting an extra layer of excitement into your gameplay.

## Developer Insights

PySnake is the brainchild of Sean Brill, blending the power of Python and tkinter to create an engaging UI and gameplay. Behind the scenes, the backend services leverage Azure Cloud Functions with Node.js, ensuring a seamless and connected gaming experience. Explore the open-source code on [GitHub](https://github.com/yourusername/pysnake) to delve into the intricacies of PySnake's development.

## Installation

To get started, follow these steps:

1. Download the latest release or clone the repository.
2. Run the PyInstaller command to build the executable:

    ```bash
    pyinstaller --noconsole --onefile --name PySnake main.py
    ```

    or

   Run the provided `build.bat` script to copy `player_data.txt` and the `assets` folder to the `dist` directory:

    ```bash
    build.bat
    ```

    If you encounter any issues, ensure that the script is in the same directory as your Python script (`main.py`).

For additional information and insights, visit [Sean Brill's website](https://seanbrill.com).

Enjoy the thrill of PySnake!
