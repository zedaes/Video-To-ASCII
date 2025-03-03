import cv2
import numpy as np
import curses
import time

ACII_CHARS = '@%#*+=-:. '

def frame_to_ascii(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    normalized_frame = (gray_frame - np.min(gray_frame)) / (np.max(gray_frame) - np.min(gray_frame))
    ascii_indices = (normalized_frame * (len(ACII_CHARS) - 1)).astype(int)
    ascii_frame = np.array([ACII_CHARS[i] for i in ascii_indices.flatten()])
    ascii_frame = ascii_frame.reshape(gray_frame.shape)

    return ascii_frame

def main(stdscr, video_path):
    stdscr.clear()
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        ascii_frame = frame_to_ascii(frame)
        stdscr.clear()
        for i, row in enumerate(ascii_frame):
            stdscr.addstr(i, 0, ''.join(row))
        
        stdscr.refresh()
        time.sleep(0.1)

    cap.release()

if __name__ == "__main__":
    video_path = ''
    curses.wrapper(main, video_path)
