# menus.py

import arcade
# Remove module-level imports that cause circular dependencies
# from game import SinglePlayerGame
# from network import MultiplayerGame

from settings import SettingsMenu    # Ensure this is implemented
from credits import CreditsScreen    # Ensure this is implemented
from leaderboard import LeaderboardScreen

class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.selected_option = 0
        self.options = ["Start Game", "Multiplayer", "Options", "Credits", "Leaderboard", "Quit"]

    def setup(self):
        pass  # Any setup code

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        y_start = self.window.height - 200
        for index, option in enumerate(self.options):
            color = arcade.color.WHITE
            if index == self.selected_option:
                color = arcade.color.YELLOW
            arcade.draw_text(
                option,
                self.window.width / 2,
                y_start - index * 60,
                color,
                36,
                anchor_x="center",
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif key == arcade.key.DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif key == arcade.key.ENTER or key == arcade.key.SPACE:
            self.select_option()

    def select_option(self):
        option = self.options[self.selected_option]
        if option == "Start Game":
            # Import SinglePlayerGame locally to avoid circular import
            from game import SinglePlayerGame
            game_view = SinglePlayerGame()
            game_view.setup()
            self.window.show_view(game_view)
        elif option == "Multiplayer":
            # Import MultiplayerGame locally if necessary
            from network import MultiplayerGame
            multiplayer_view = MultiplayerGame()
            multiplayer_view.setup()
            self.window.show_view(multiplayer_view)
        elif option == "Options":
            settings_view = SettingsMenu()
            settings_view.setup()
            self.window.show_view(settings_view)
        elif option == "Credits":
            credits_view = CreditsScreen()
            credits_view.setup()
            self.window.show_view(credits_view)
        elif option == "Leaderboard":
            leaderboard_view = LeaderboardScreen()
            leaderboard_view.setup()
            self.window.show_view(leaderboard_view)
        elif option == "Quit":
            arcade.close_window()
