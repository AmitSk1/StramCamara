import socket
import cv2
import pickle
import struct
from mss import mss
import numpy as np

fff = open()


class Client:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        print("Client connected to the server")

    def receive_video(self):
        data = b""
        payload_size = struct.calcsize("L")  # Use "L" for 8-byte unsigned integer

        try:
            while True:
                while len(data) < payload_size:
                    packet = self.client_socket.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("L", packed_msg_size)[0]  # Use "L" for unpacking

                while len(data) < msg_size:
                    data += self.client_socket.recv(4 * 1024)

                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame = pickle.loads(frame_data)

                # Check if the frame is valid
                if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
                    # Split the frame into camera and screen streams
                    camera_frame = frame[:, :640, :]
                    screen_frame = frame[:, 640:, :]

                    # Display camera stream
                    cv2.imshow("Camera Stream", camera_frame)

                    # Check if screen frame has valid dimensions
                    if screen_frame.shape[0] > 0 and screen_frame.shape[1] > 0:
                        # Display screen stream
                        cv2.imshow("Screen Stream", screen_frame)

                if cv2.waitKey(1) == ord('q'):
                    break

        except (socket.error, pickle.UnpicklingError) as e:
            print(f"Error: {e}")

        finally:
            cv2.destroyAllWindows()
            self.client_socket.close()


if __name__ == '__main__':
    client = Client('127.0.0.1', 5000)
    client.receive_video()