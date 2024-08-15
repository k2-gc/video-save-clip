import os
import shutil
import tkinter as tk
import tkinter.filedialog

import cv2

from .data import Model
from .utils import get_logger
from .window_creater import View


class Controller:
    """App controller
    This class manage view class which treats tkinter window and data class which treats data.

    Args:
        root (tkinter.Tk): tkinter.Tk object.
    """
    def __init__(self, root):
        self.logger = get_logger()
        self.logger.info("Init Controller class")
        self.root = root
        self.view = View(root)
        self.model = Model()
        self.video_name = ""
        self.next_key = ["Right"]
        self.prev_key = ["Left"]
        self.quit_key = ["q"]
        self._bind_callback()

    def __del__(self):
        self.logger.info("Controller object deleting...")
    

    def _bind_callback(self):
        """Bind callback function to the button etc. in View

        """
        # Bind callback function to buttons in View class
        self.view.file_dialog.config(command=self.open_video)
        self.view.video_clip_start.config(command=lambda: self.get_value(True))
        self.view.video_clip_stop.config(command=lambda: self.get_value(False))
        self.view.slider.config(command=self.update_frame)
        self.view.help_label.config(command=self.help)
        self.view.video_clip.config(command=self.clip_video)
        self.view.frame_clip.config(command=self.clip_frame)
        self.view.save_frame_num.trace_add("write", callback=lambda *args: self.get_input_num(*args))
        self.view.save_num_input.config()

        # Bind callback function to key pressing
        self.root.bind("<KeyPress>", self.key_event)

    
    def get_input_num(self, *args):
        """Get expected save frame num

        """
        input_string = self.view.save_frame_num.get()
        if "q" in input_string:
            self.logger.warning("[q] was pressed!")
        self.model.set_input_frame_num(input_string)
        

    def clip_video(self):
        """Clip and save frames in the span as a video.
        
        """
        self.logger.info("Clip videos")
        if not self.model.clip(self.video_name):
            self.logger.warning("Clip video failed")

    def clip_frame(self):
        """Clip and save frames in the span as images.
        
        """
        
        self.logger.info("Clip frames")
        if not self.model.save_frame(self.video_name):
            self.logger.warning("Clip frames failed")
        

    def help(self):
        """Open help window.
        
        """

        self.logger.info("Open help")
        fps = self.model.get_video_fps()
        video_len = self.model.get_video_len()
        width = self.model.get_video_width()
        height = self.model.get_video_height()
        self.view.create_help_window(fps, video_len, width, height)
    

    def get_value(self, is_start=True):
        """Get and set frame pos
           If 'is_start' is True, start frame pos will be set.
           Otherwise, stop frame pos will be set.
        
        Args:
            is_start (bool): start pos or stop pos
        """

        current_value = self.view.slider.get()
        if is_start:
            self.view.video_clip_start_label["text"] = f"{str(current_value).zfill(5)}"
            self.model.set_clip_pos(current_value)
            self.logger.info(f"Set start pos: {current_value}")
        else:
            self.view.video_clip_stop_label["text"] = f"{str(current_value).zfill(5)}"
            self.model.set_clip_pos(current_value, False)
            self.logger.info(f"Set stop pos: {current_value}")

    def open_video(self):
        """Using filedialog, open mp4 video file
        
        """
        fTyp = [("", "*mp4")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file_path = tk.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if file_path == "":
            return
        self.logger.info(f"Video path: {file_path}")
        if os.path.exists(file_path):
            shutil.copyfile(file_path, self.model.tmp_video_path)
            cap = cv2.VideoCapture(self.model.tmp_video_path)
            self.model.set_video_info(cap)
            self.view.recreate_window(self.model.get_video_width(), self.model.get_video_height())
            self._bind_callback()
            self.update_frame()
            self.view.slider.config(to=self.model.get_video_len()-1)
            self.logger.info(f"Loaded: {file_path}")
            self.video_name = os.path.basename(file_path)
        else:
            self.logger.warning(f"Video not found: {file_path}")
    

    def update_frame(self, *args):
        """Update shown frame on display
            This function is called under the conditions below.
                1. Slider is changed
                2. 'left' or 'right' key on keybord is pressed.

        Args:
            *args
        """
        frame_index = self.view.slider.get()
        self.model.set_frame(frame_index)
        self.view.display_image(self.model.get_frame())

    def key_event(self, event):
        """Key pressing operation.
            This function is called and run a function corresponding to key when pressing a key.

        Args:
            event (tkinter.Event): tkinter.Event object.
        """
        if event.keysym in self.next_key:
            frame_index = self.model.get_frame_index() + 1
            self.view.slider.set(frame_index)
            self.update_frame()
            return
        elif event.keysym in self.prev_key:
            frame_index = self.model.get_frame_index() - 1
            self.view.slider.set(frame_index)
            self.update_frame()
            return
        elif event.keysym in self.quit_key:
            del self.model
            del self.view
            self.root.destroy()
            self.root.quit()
            del self
        else:
            pass
        #     self.logger.info(f"No functions is assigned to key '{event.keysym}'")
