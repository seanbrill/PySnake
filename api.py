import requests
from env import SECRET_KEY
from env import GET_LEADERBOARD_URL
from env import SUBMIT_SCORE_URL

class HttpManager:
    
    instance : 'HttpManager' = None

    def __init__(self):
        HttpManager.instance = self

    def get_leaderboard(self):
        url = GET_LEADERBOARD_URL

        headers = {
            'x-secretkey': SECRET_KEY,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            # You can now use response.json() to access the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def submit_score(self, name, score, difficulty):
        url = SUBMIT_SCORE_URL

        headers = {
            'x-secretkey': SECRET_KEY,
            'Content-Type': 'application/json'
        }

        data = {
            'playerName': name,
            'playerScore': score,
            'playerDifficulty' : difficulty
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            # You can now use response.json() to access the JSON response
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

