# network.py

import arcade
import socket
import threading

class MultiplayerGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.network = Network()
        self.player_id = None
        self.players = {}
        self.setup()

    def setup(self):
        # Connect to the server and get the player ID
        self.player_id = self.network.connect()
        # Start a thread to receive data from the server
        threading.Thread(target=self.receive_data, daemon=True).start()

    def on_draw(self):
        arcade.start_render()
        # Draw the players
        for player in self.players.values():
            player.draw()

    def on_update(self, delta_time):
        # Update game state, handle network communication
        pass

    def on_key_press(self, key, modifiers):
        # Handle key presses and send movement commands to the server
        pass

    def receive_data(self):
        while True:
            try:
                data = self.network.receive()
                # Process incoming data and update players
                # For example, update self.players based on data
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'localhost'  # Replace with server IP if necessary
        self.port = 5555
        self.addr = (self.server, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            # Receive initial data, e.g., player ID
            player_id = self.client.recv(2048).decode()
            return player_id
        except Exception as e:
            print(f"Connection error: {e}")
            return None

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            print(e)
            return None

    def receive(self):
        try:
            data = self.client.recv(2048).decode()
            return data
        except socket.error as e:
            print(e)
            return None
