import socket
import cv2
import numpy as np
import pickle
import struct
import threading


class Server:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = {}  # Dictionary to store client connections and their respective IDs
        self.client_counter = 1  # Counter for assigning unique IDs to clients
        print(f"Server listening on {host}:{port}")

    def handle_client(self, client_socket, client_id):
        connection = client_socket.makefile('wb')
        video_capture = cv2.VideoCapture(0)
        screen_capture = None

        try:
            while True:
                # Capture webcam stream
                ret, frame = video_capture.read()

                # Capture screen stream
                if screen_capture is not None:
                    screen_frame = screen_capture.grab_screen()
                    frame = cv2.resize(frame, (320, 240))
                    screen_frame = cv2.resize(screen_frame, (320, 240))
                    frame = np.hstack((frame, screen_frame))

                # Add client ID as an overlay on the video frame
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, f"Client {client_id}", (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

                data = pickle.dumps(frame)
                size = struct.pack("L", len(data))
                connection.write(size)
                connection.write(data)
        except (socket.error, KeyboardInterrupt):
            print(f"Client {client_id} disconnected.")
            del self.clients[client_id]  # Remove client from the clients dictionary
        finally:
            video_capture.release()
            connection.close()
            client_socket.close()

    def start(self):
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Connection from {address}")
                client_id = self.client_counter
                self.clients[client_id] = client_socket  # Add client socket to the clients dictionary
                self.client_counter += 1
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_id))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.server_socket.close()


if __name__ == '__main__':
    server = Server('127.0.0.1', 5000)
    server.start()
