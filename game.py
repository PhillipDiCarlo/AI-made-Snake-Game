# game.py

import arcade
import random

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
SNAKE_SIZE = 20

class SinglePlayerGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.snake = None
        self.food = None
        self.power_ups = []
        self.score = 0
        self.move_timer = 0
        self.move_rate = 0.1  # Adjust this value to control snake speed

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.snake = Snake()
        self.food = Food()
        self.power_ups = []
        self.score = 0
        # Schedule power-up spawning every 10 seconds
        arcade.schedule(self.spawn_power_up, 10)

    def on_draw(self):
        arcade.start_render()
        self.snake.draw()
        self.food.draw()
        for power_up in self.power_ups:
            power_up.draw()
        # Draw the score
        arcade.draw_text(
            f"Score: {self.score}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            20,
        )

    def on_update(self, delta_time):
        self.move_timer += delta_time
        if self.move_timer >= self.move_rate:
            self.snake.move()
            self.move_timer = 0

            # Check collision with food
            if self.snake.check_collision(self.food.position):
                self.snake.grow()
                self.score += 10
                self.food.reposition()

            # Check collision with power-ups
            for power_up in self.power_ups[:]:
                if self.snake.check_collision(power_up.position):
                    self.snake.shorten()
                    self.power_ups.remove(power_up)

            # Check self-collision (game over)
            if self.snake.check_self_collision():
                # Import GameOverView locally to avoid circular import
                from game_over import GameOverView
                # Transition to GameOverView
                game_over_view = GameOverView(self.score)
                self.window.show_view(game_over_view)
                # Unschedule functions and clean up
                arcade.unschedule(self.spawn_power_up)
                return  # Exit the update function

        # Handle other updates if necessary

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and self.snake.direction != 'DOWN':
            self.snake.change_direction('UP')
        elif key == arcade.key.DOWN and self.snake.direction != 'UP':
            self.snake.change_direction('DOWN')
        elif key == arcade.key.LEFT and self.snake.direction != 'RIGHT':
            self.snake.change_direction('LEFT')
        elif key == arcade.key.RIGHT and self.snake.direction != 'LEFT':
            self.snake.change_direction('RIGHT')

    def spawn_power_up(self, delta_time):
        power_up = PowerUp()
        self.power_ups.append(power_up)

class Snake:
    def __init__(self):
        self.size = SNAKE_SIZE
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'UP'
        self.color = arcade.color.GREEN
        self.width = self.size
        self.height = self.size
        self.growing = False  # Flag to indicate growth

    def move(self):
        x, y = self.positions[0]
        if self.direction == 'UP':
            y += self.size
        elif self.direction == 'DOWN':
            y -= self.size
        elif self.direction == 'LEFT':
            x -= self.size
        elif self.direction == 'RIGHT':
            x += self.size

        # Wrap around the screen
        x %= SCREEN_WIDTH
        y %= SCREEN_HEIGHT

        new_head = (x, y)
        self.positions.insert(0, new_head)  # Add new head to the front

        # If not growing, remove the tail
        if not self.growing:
            self.positions.pop()
        else:
            self.growing = False  # Reset the growing flag

    def change_direction(self, direction):
        opposite_directions = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT',
        }
        if direction != opposite_directions.get(self.direction):
            self.direction = direction

    def grow(self):
        self.growing = True  # Set the flag to grow on next move

    def shorten(self):
        # Shorten by 5 units or 20% of length, whichever is less
        amount_to_shorten = min(5, max(1, len(self.positions) // 5))
        for _ in range(amount_to_shorten):
            if len(self.positions) > 1:
                self.positions.pop()
            else:
                # The snake cannot be shortened further; game over
                break

    def check_collision(self, position):
        head_x, head_y = self.positions[0]
        obj_x, obj_y = position

        # Check if the rectangles overlap
        collision = (
            abs(head_x - obj_x) < self.width and
            abs(head_y - obj_y) < self.height
        )
        return collision

    def check_self_collision(self):
        return self.positions[0] in self.positions[1:]

    def draw(self):
        for position in self.positions:
            arcade.draw_rectangle_filled(
                position[0], position[1], self.size, self.size, self.color
            )

class Food:
    def __init__(self):
        self.size = SNAKE_SIZE
        self.position = self.random_position()
        self.color = arcade.color.RED
        self.width = self.size
        self.height = self.size

    def random_position(self):
        x = (
            random.randint(0, (SCREEN_WIDTH - self.size) // self.size) * self.size
            + self.size // 2
        )
        y = (
            random.randint(0, (SCREEN_HEIGHT - self.size) // self.size) * self.size
            + self.size // 2
        )
        return (x, y)

    def reposition(self):
        self.position = self.random_position()

    def draw(self):
        arcade.draw_rectangle_filled(
            self.position[0], self.position[1], self.size, self.size, self.color
        )

class PowerUp:
    def __init__(self):
        self.size = SNAKE_SIZE
        self.position = self.random_position()
        self.color = arcade.color.BLUE
        self.width = self.size
        self.height = self.size

    def random_position(self):
        x = (
            random.randint(0, (SCREEN_WIDTH - self.size) // self.size) * self.size
            + self.size // 2
        )
        y = (
            random.randint(0, (SCREEN_HEIGHT - self.size) // self.size) * self.size
            + self.size // 2
        )
        return (x, y)

    def draw(self):
        arcade.draw_circle_filled(
            self.position[0], self.position[1], self.size // 2, self.color
        )
