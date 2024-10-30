import arcade

class CreditsScreen(arcade.Window):
    def __init__(self):
        super().__init__(1024, 1024, "Snake Game - Credits")

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        credits = [
            "Person 1 - Lead Programmer",
            "Person 2 - Orchestral Lead",
            # Add more credits as needed
        ]
        y_start = 900
        for index, line in enumerate(credits):
            arcade.draw_text(line, 512, y_start - index * 40, arcade.color.WHITE, 24, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.close()
            menu = MainMenu()
            menu.setup()
            arcade.run()
