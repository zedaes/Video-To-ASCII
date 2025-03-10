import cv2
import numpy as np
import curses
import time

ASCII_CHARS = '@$%#&!*+=-_. '

def frame_to_ascii(frame, width, height):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    resized_frame = cv2.resize(gray_frame, (width, height), interpolation=cv2.INTER_AREA)

    normalized_frame = (resized_frame - np.min(resized_frame)) / (np.max(resized_frame) - np.min(resized_frame) + 1e-7)
    ascii_indices = (normalized_frame * (len(ASCII_CHARS) - 1)).astype(int)
    ascii_frame = np.array([ASCII_CHARS[i] for i in ascii_indices.flatten()])
    ascii_frame = ascii_frame.reshape(resized_frame.shape)

    return ascii_frame

def run_curses(stdscr, video_path):
    curses.curs_set(0)  
    cap = cv2.VideoCapture(video_path)

    max_y, max_x = stdscr.getmaxyx()
    max_y -= 1  
    max_x -= 1

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = frame_to_ascii(frame, max_x, max_y)

        stdscr.move(0, 0)

        for i, row in enumerate(ascii_frame):
            if i >= max_y:
                break
            line = ''.join(row)
            try:
                stdscr.addstr(i, 0, line[:max_x])
            except curses.error:
                pass

        stdscr.refresh()
        time.sleep(0.05)

    cap.release()

if __name__ == "__main__":
    video_path = 'camel.mp4'
    curses.wrapper(run_curses, video_path)
