# game_over.py

import arcade
from leaderboard import submit_score  # Assuming this doesn't cause circular import

class GameOverView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.player_name = ""
        self.submission_status = None  # None, 'submitted', or 'failed'

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Game Over",
            self.window.width / 2,
            self.window.height / 2 + 100,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Your Score: {self.score}",
            self.window.width / 2,
            self.window.height / 2 + 50,
            arcade.color.WHITE,
            24,
            anchor_x="center",
        )
        if self.submission_status is None:
            arcade.draw_text(
                "Enter your name:",
                self.window.width / 2,
                self.window.height / 2,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )
            arcade.draw_text(
                self.player_name,
                self.window.width / 2,
                self.window.height / 2 - 30,
                arcade.color.YELLOW,
                24,
                anchor_x="center",
            )
        elif self.submission_status == 'submitted':
            arcade.draw_text(
                "Score Submitted!",
                self.window.width / 2,
                self.window.height / 2,
                arcade.color.GREEN,
                24,
                anchor_x="center",
            )
            arcade.draw_text(
                "Press ESC to return to the main menu.",
                self.window.width / 2,
                self.window.height / 2 - 50,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )
        elif self.submission_status == 'failed':
            arcade.draw_text(
                "Failed to submit score.",
                self.window.width / 2,
                self.window.height / 2,
                arcade.color.RED,
                24,
                anchor_x="center",
            )
            arcade.draw_text(
                "Press ESC to return to the main menu.",
                self.window.width / 2,
                self.window.height / 2 - 50,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )

    def on_key_press(self, key, modifiers):
        if self.submission_status is None:
            if key == arcade.key.BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif key == arcade.key.ENTER:
                if self.player_name:
                    result = submit_score(self.player_name, self.score)
                    if result.get('success'):
                        self.submission_status = 'submitted'
                    else:
                        self.submission_status = 'failed'
                else:
                    # Optionally, prompt user to enter a name
                    pass
            elif key == arcade.key.ESCAPE:
                # Import MainMenu locally to avoid circular import
                from menus import MainMenu
                main_menu = MainMenu()
                main_menu.setup()
                self.window.show_view(main_menu)
            else:
                # Handle character input
                if len(self.player_name) < 12:
                    if 32 <= key <= 126:
                        self.player_name += chr(key)
        else:
            if key == arcade.key.ESCAPE:
                # Import MainMenu locally to avoid circular import
                from menus import MainMenu
                main_menu = MainMenu()
                main_menu.setup()
                self.window.show_view(main_menu)
