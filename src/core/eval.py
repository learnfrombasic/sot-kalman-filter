from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
from glob import glob

import cv2
import numpy as np
import torch

from common.frame_utils import get_frames
from vendors.pysot.core.config import cfg
from vendors.pysot.models.model_builder import ModelBuilder
from vendors.pysot.tracker.tracker_builder import build_tracker

torch.set_num_threads(1)

parser = argparse.ArgumentParser(description="tracking demo")
parser.add_argument("--config", type=str, help="config file")
parser.add_argument("--snapshot", type=str, help="model name")
parser.add_argument("--video_name", default="", type=str, help="videos or image files")
args = parser.parse_args()


def main():
    # load config
    cfg.merge_from_file(args.config)
    cfg.CUDA = torch.cuda.is_available() and cfg.CUDA
    device = torch.device("cuda" if cfg.CUDA else "cpu")

    # create model
    model = ModelBuilder()

    # load model
    model.load_state_dict(
        torch.load(args.snapshot, map_location=lambda storage, loc: storage.cpu())
    )
    model.eval().to(device)

    # build tracker
    tracker = build_tracker(model)

    first_frame = True
    if args.video_name:
        video_name = args.video_name.split("/")[-1].split(".")[0]
    else:
        video_name = "webcam"
    cv2.namedWindow(video_name, cv2.WND_PROP_FULLSCREEN)
    for frame in get_frames(args.video_name):
        if first_frame:
            try:
                init_rect = cv2.selectROI(video_name, frame, False, False)
            except:
                exit()
            tracker.init(frame, init_rect)
            first_frame = False
        else:
            outputs = tracker.track(frame)
            if "polygon" in outputs:
                polygon = np.array(outputs["polygon"]).astype(np.int32)
                cv2.polylines(
                    frame, [polygon.reshape((-1, 1, 2))], True, (0, 255, 0), 3
                )
                mask = (outputs["mask"] > cfg.TRACK.MASK_THERSHOLD) * 255
                mask = mask.astype(np.uint8)
                mask = np.stack([mask, mask * 255, mask]).transpose(1, 2, 0)
                frame = cv2.addWeighted(frame, 0.77, mask, 0.23, -1)
            else:
                bbox = list(map(int, outputs["bbox"]))
                cv2.rectangle(
                    frame,
                    (bbox[0], bbox[1]),
                    (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                    (0, 255, 0),
                    3,
                )
            cv2.imshow(video_name, frame)
            cv2.waitKey(40)


if __name__ == "__main__":
    main()
