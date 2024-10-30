# leaderboard.py

import requests

LEADERBOARD_URL = 'http://your-server-address:5000'  # Replace with your actual server URL

def submit_score(name, score):
    data = {'name': name, 'score': score}
    try:
        response = requests.post(f'{LEADERBOARD_URL}/submit_score', json=data, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {'success': False}
    except requests.exceptions.RequestException as e:
        print(f"Error submitting score: {e}")
        return {'success': False}

def get_high_scores():
    try:
        response = requests.get(f'{LEADERBOARD_URL}/get_scores', timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving high scores: {e}")
        return None

# LeaderboardScreen class for displaying the leaderboard
import arcade

class LeaderboardScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.scores = []
        self.error = False

    def setup(self):
        self.scores = get_high_scores()
        if self.scores is None:
            self.error = True

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        if self.error:
            arcade.draw_text(
                "Leaderboard Not Loaded",
                self.window.width / 2,
                self.window.height / 2,
                arcade.color.RED,
                24,
                anchor_x="center",
            )
        else:
            y_start = self.window.height - 50
            for index, entry in enumerate(self.scores):
                text = f"{index + 1}. {entry['name']} - {entry['score']}"
                arcade.draw_text(
                    text,
                    self.window.width / 2,
                    y_start - index * 30,
                    arcade.color.WHITE,
                    20,
                    anchor_x="center",
                )
                if index >= 9:  # Show top 10 scores
                    break

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from menus import MainMenu
            main_menu = MainMenu()
            main_menu.setup()
            self.window.show_view(main_menu)
