from pathlib import Path

import cv2

# * Try multi-threading/processing for reading and processing frames.


def get_frames(video_name: str):
    if not video_name:
        # Use the default camera
        cap = cv2.VideoCapture(0)
        # Warm up the camera
        for _ in range(5):
            cap.read()
        while True:
            ret, frame = cap.read()
            if ret:
                yield frame
            else:
                break
    elif video_name.endswith(("avi", "mp4")):
        # Open a video file
        cap = cv2.VideoCapture(video_name)
        while True:
            ret, frame = cap.read()
            if ret:
                yield frame
            else:
                break
    else:
        # Assuming video_name is a directory containing images
        image_dir = Path(video_name)
        images = sorted(
            image_dir.glob("*.jp*"), key=lambda x: int(x.stem.split(".")[0])
        )
        for img_path in images:
            frame = cv2.imread(str(img_path))
            yield frame
