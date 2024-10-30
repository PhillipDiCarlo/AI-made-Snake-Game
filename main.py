import arcade
from menus import MainMenu

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
SCREEN_TITLE = "Snake Game"

def show_splash_screen():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    splash = arcade.load_texture("assets/images/splash_placeholder.png")
    start_time = time.time()

    @window.event
    def on_draw():
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, splash)

    while time.time() - start_time < 10:
        window.dispatch_events()
        window.on_draw()
        window.flip()

    window.close()

def main():
    window = arcade.Window(1024, 1024, "Snake Game")
    main_menu = MainMenu()
    main_menu.setup()
    window.show_view(main_menu)
    arcade.run()

if __name__ == "__main__":
    main()
