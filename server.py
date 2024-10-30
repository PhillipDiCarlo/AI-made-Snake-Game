# server.py

import socket
import threading

HOST = 'localhost'  # Replace with your server's IP address if necessary
PORT = 5555

clients = []
player_id_counter = 0

def handle_client(conn, addr, player_id):
    print(f"New connection: {addr}, Player ID: {player_id}")
    conn.send(str(player_id).encode())
    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                break
            # Process data and broadcast to other clients
            broadcast(f"Player {player_id}: {data}", conn)
        except:
            break
    conn.close()
    print(f"Connection closed: {addr}")
    clients.remove(conn)

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message.encode())
            except:
                pass

def main():
    global player_id_counter
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        player_id = player_id_counter
        player_id_counter += 1
        threading.Thread(target=handle_client, args=(conn, addr, player_id), daemon=True).start()

if __name__ == "__main__":
    main()
