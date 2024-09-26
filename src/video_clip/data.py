import os
from pathlib import Path
import shutil
import tkinter as tk

import cv2
from PIL import Image
from tqdm import tqdm
from tqdm.contrib import tenumerate

from .utils import get_logger, get_suffix

class Model:
    """Manage frame position, load and svae a frame.
    Hold opencv VideoCapture object, current frame index and so on.

    Args: 
        None
    """
    def __init__(self):
        self.logger = get_logger()
        self.logger.info("Init Model class")
        self.tmp_video_path = "tmp.mp4"
        self.output_tmp_video_path = "tmp2.mp4"
        self.output_tmp_frame_path = "tmp.jpg"
        self.cap = None
        self.current_frame_index = 0
        self.video_len = 0
        self.video_fps = 0
        self.frame_width = 0
        self.frame_height = 0
        self.clip_start_pos = 0
        self.clip_stop_pos = 0
        self.save_frame_num = 0

    def __del__(self):
        del self.cap
        if os.path.exists(self.tmp_video_path):
            os.remove(self.tmp_video_path)
            self.logger.info(f"'{self.tmp_video_path}' deleting...")
        self.logger.info("Model object deleting...")
    
    def set_video_info(self, cap):
        """Set video info such as...
            1. cap
            2. video fps
            3. frame width
            4. frame height
            5. video frame num
        """
        self._set_cap(cap)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        video_len = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self._set_video_fps(fps)
        self._set_video_len(video_len)
        self._set_frame_height(height)
        self._set_frame_width(width)

    # Setter 
    def _set_cap(self, cap):
        self.cap = cap

    def _set_video_len(self, video_len):
        self.video_len = video_len

    def _set_video_fps(self, fps):
        self.video_fps = fps
    
    def _set_frame_width(self, width):
        self.frame_width = width

    def _set_frame_height(self, height):
        self.frame_height = height 
    
    def set_frame(self, frame_index):
        """Set frame
            This func will be called when update a frame on an app window

        Args:
            frame_index: frame index in the video
        """
        self.current_frame_index = frame_index
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_index) 
        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.current_frame = frame
    
    def set_input_frame_num(self, input_str: str):
        """Set input num which means how many frames will be saved

        Args:
            input_str: Input str on an app window
        """
        # if input_str == "":
        #     self.logger.warning("Save Frame Num not set")
        #     return
        # if not input_str.isdecimal():
        #     self.logger.warning("Input Value not decimal")
        #     return
        if input_str == "":
            return
        if not input_str.isnumeric():
            self.logger.warning("Input Value not Numeric")
            return
        # input_str = float(input_str)
        # if not input_str.is_integer():
        #     self.logger.warning("Input Value not INT")
        #     return
        self.save_frame_num = int(input_str)

    def set_clip_pos(self, pos: int, is_start: bool =True):
        """Set frame index in the video to clip video and save frames

        Args:
            pos: frame index
            is_start: whther clip start pos or stop pos
        """
        if is_start:
            self.clip_start_pos = pos
        else:
            self.clip_stop_pos = pos

    # Getter
    def get_video_len(self):
        return self.video_len

    def get_video_fps(self):
        return self.video_fps
    
    def get_video_width(self):
        return self.frame_width

    def get_video_height(self):
        return self.frame_height
    
    def get_frame(self):
        return self.current_frame

    def get_frame_index(self):
        return self.current_frame_index
    
    def get_clip_pos(self, is_start=True):
        if is_start:
            return self.clip_start_pos
        return self.clip_stop_pos

    def clip(self, video_name: str, progbar):
        # TODO: Move video name from app_cotroller.py to data.py
        """Clip video between 'start pos' and 'stop pos'

        Args:
            video_name: Save video name
        
        Returns:
            bool
        """
        if self.clip_start_pos >= self.clip_stop_pos:
            self.logger.warning("Start pos is bigger than stop pos")
            return False

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.clip_start_pos) 
        clip_frame_num = self.clip_stop_pos - self.clip_start_pos
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out_path = get_suffix(video_name)
        video = cv2.VideoWriter(self.output_tmp_video_path, fourcc, self.video_fps, (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        progbar.config(length=400, mode="determinate", maximum=clip_frame_num+1)
        for i in tqdm(range(clip_frame_num+1)):
            ret, frame = self.cap.read()
            if not ret:
                self.logger.warning(f"Frame finished")
                break
            
            video.write(frame)
            progbar.config(value=i)
            progbar.update()
        video.release()
        shutil.move(self.output_tmp_video_path, out_path)
        return True
    
    def save_frame(self, video_name, progbar):
        # TODO: Move video name from app_cotroller.py to data.py
        """Save frames between 'start pos' and 'stop pos'
            Save 'self.save_frame_num' frames

        Args:
            video_name: Save directory name
        
        Returns:
            bool
        """

        # save_frame_num = self.view.save_frame_num.get()
        if self.save_frame_num == 0:
            self.logger.warning("Save frame num is not input or 0")
            return False
        if self.clip_start_pos >= self.clip_stop_pos:
            self.logger.warning("Start pos is equal or bigger than stop pos")
            return False

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.clip_start_pos) 
        frame_num_in_span = self.clip_stop_pos - self.clip_start_pos + 1
        if self.save_frame_num > frame_num_in_span:
            self.logger.warning(f"Input save frame num: {self.save_frame_num} is greater than frames in span: {frame_num_in_span}")
        almost_uniform = [(frame_num_in_span + i) // self.save_frame_num for i in range(self.save_frame_num)]
        tmp = 0
        index_list = []
        for i in almost_uniform:
            tmp += i
            index_list.append(tmp)
        out_dir = get_suffix(video_name, False)
        Path(out_dir).mkdir()

        # Expect over 10FPS * 20min
        if frame_num_in_span > 12000:
            tmp_cap = cv2.VideoCapture(self.tmp_video_path)
            progbar.config(length=400, mode="determinate", maximum=len(index_list))
            for i, index in tenumerate(index_list):
                tmp_cap.set(cv2.CAP_PROP_POS_FRAMES, index+self.clip_start_pos)
                ret, frame = tmp_cap.read()
                if not ret:
                    break
                cv2.imwrite(self.output_tmp_frame_path, frame)
                shutil.move(self.output_tmp_frame_path, f"{out_dir}/frame_{str(index+self.clip_start_pos).zfill(10)}.jpg")
                progbar.config(value=i+1)
                progbar.update()
            tmp_cap.release()
        else:
            # Including bug
            progbar.config(length=400, mode="determinate", maximum=frame_num_in_span+1)
            for i in tqdm(range(frame_num_in_span+1)):
                ret, frame = self.cap.read()
                if not ret:
                    self.logger.warning(f"Frame finished")
                    break
                if not i in index_list:
                    continue
                cv2.imwrite(self.output_tmp_frame_path, frame)
                shutil.move(self.output_tmp_frame_path, f"{out_dir}/frame_{str(self.clip_start_pos+i).zfill(10)}.jpg")
                progbar.config(value=i+1)
                progbar.update()
            return True
