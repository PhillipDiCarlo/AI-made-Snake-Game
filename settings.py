import arcade
import json

class SettingsMenu(arcade.Window):
    def __init__(self):
        super().__init__(1024, 1024, "Snake Game - Settings")
        self.master_volume = 1.0
        self.fx_volume = 1.0
        self.music_volume = 1.0
        self.load_settings()

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        # Draw sliders and labels
        arcade.draw_text("Master Volume", 200, 700, arcade.color.WHITE, 24)
        arcade.draw_text("FX Volume", 200, 600, arcade.color.WHITE, 24)
        arcade.draw_text("Music Volume", 200, 500, arcade.color.WHITE, 24)
        # Draw sliders (this is a placeholder; actual sliders need to be implemented)
        arcade.draw_rectangle_filled(600, 700, self.master_volume * 200, 20, arcade.color.GRAY)
        arcade.draw_rectangle_filled(600, 600, self.fx_volume * 200, 20, arcade.color.GRAY)
        arcade.draw_rectangle_filled(600, 500, self.music_volume * 200, 20, arcade.color.GRAY)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # Adjust volumes based on mouse position
        if 590 < x < 610:
            if 690 < y < 710:
                self.master_volume = (x - 500) / 200
                arcade.set_sound_volume(self.master_volume)
            elif 590 < y < 610:
                self.fx_volume = (x - 500) / 200
                # Adjust FX volume
            elif 490 < y < 510:
                self.music_volume = (x - 500) / 200
                # Adjust music volume

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.save_settings()
            self.close()
            menu = MainMenu()
            menu.setup()
            arcade.run()

    def save_settings(self):
        settings = {
            'master_volume': self.master_volume,
            'fx_volume': self.fx_volume,
            'music_volume': self.music_volume
        }
        with open('config.json', 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open('config.json', 'r') as f:
                settings = json.load(f)
                self.master_volume = settings.get('master_volume', 1.0)
                self.fx_volume = settings.get('fx_volume', 1.0)
                self.music_volume = settings.get('music_volume', 1.0)
        except FileNotFoundError:
            self.save_settings()
