import tkinter as tk
from tkinter import ttk

import numpy as np
from PIL import Image, ImageTk


from .utils import get_logger

class View(tk.Frame):
    """Manage app window.

    Args:
        parent (tkinter.Tk): tkinter.Tk object
    """
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Video Clip")
        self.logger = get_logger()
        self.logger.info("Init View class")

        # Create tkinter widgets
        self.width = 0
        self.height = 0
        self.tool_bar = None
        self.image_frame = None
        self.slider_bar = None
        self.command_bar = None
        self.canvas = None
        self.file_dialog = None
        self.help_label = None
        # TODO: Combbox
        # self.comb = ttk.Combobox(self.tool_bar, values=["a", "b"], textvariable=tk.StringVar(), state="readonly")
        self.video_clip_start = None
        self.video_clip_start_label = None
        self.video_clip_stop = None
        self.video_clip_stop_label = None
        self.video_clip = None
        self.save_frame = None
        self.fps_label1 = None
        self.fps_label2 = None
        self.save_frame_num = None
        self.save_num_input = None
        self.video_clip = None
        self.frame_clip = None
        self.slider = None
        self._create_window(640, 480)

    def __del__(self):
        self.logger.info("View object deleting...")
    
    def recreate_window(self, width: int, height: int):
        """Recreate an app window
            This function will be called when opning mp4 video file

        Args:
            width: Frame width
            height: Frame height
        """
        self._create_window(width, height)
    
    def _create_window(self, width: int = 640, height: int = 480):
        """Create an app window

        Args:
            width: Frame width
            height: Frame height
        """
        if width > 1900:
            width //= 2
            height //= 2
        self.width = int(width)
        self.height = int(height)
        self.tool_bar = tk.Frame(self.parent, width=self.width)
        self.image_frame = tk.Frame(self.parent)
        self.slider_bar = tk.Frame(self.parent, width=100)
        self.command_bar = tk.Frame(self.parent, width=self.width, borderwidth=1, relief="solid")
        self.tool_bar.grid(column=0, row=0, padx=2, pady=2, sticky="NEWS")
        self.image_frame.grid(column=0, row=1, padx=2, pady=2)
        self.slider_bar.grid(row=2, sticky="NEWS")
        self.command_bar.grid(row=3, sticky="NEWS")
        for i in range(6):
            self.command_bar.grid_columnconfigure(i, weight=1)
        self.canvas = tk.Canvas(self.image_frame, width=self.width-4, height=self.height)
        self.file_dialog = tk.Button(self.tool_bar, text="File", width=10, height=1, bg="white")
        self.help_label = tk.Button(self.tool_bar, text="Help", width=10, height=1, bg="white")
        # TODO: Combbox
        # self.comb = ttk.Combobox(self.tool_bar, values=["a", "b"], textvariable=tk.StringVar(), state="readonly")
        self.video_clip_start = tk.Button(self.command_bar, text="Start pos", height=1, bg="white", default="active")
        self.video_clip_start_label = tk.Label(self.command_bar, text="00000", height=1, bg="white")
        self.video_clip_stop = tk.Button(self.command_bar, text="Stop pos", height=1, bg="white", default="active")
        self.video_clip_stop_label = tk.Label(self.command_bar, text="00000", height=1, bg="white")
        self.video_clip = tk.Button(self.command_bar, text="clip", height=1, bg="white", default="active")
        self.save_frame = tk.Frame(self.command_bar)
        self.fps_label1 = tk.Label(self.command_bar, text="Save", height=1, bg="white")
        self.fps_label2 = tk.Label(self.command_bar, text="Frames", height=1, bg="white")
        self.save_frame_num = tk.StringVar()
        self.save_frame_num.set("")
        self.save_num_input = tk.Entry(self.command_bar, width=2, textvariable=self.save_frame_num, bg="#bfdfff")
        self.video_clip = tk.Button(self.command_bar, text="Video clip", height=1, bg="white", default="active")
        self.frame_clip = tk.Button(self.command_bar, text="Frame save", height=1, bg="white", default="active")
        command_button = [
            self.video_clip_start,
            self.video_clip_start_label,
            self.video_clip_stop,
            self.video_clip_stop_label,
            self.video_clip,
            self.fps_label1,
            self.save_num_input,
            self.fps_label2,
            self.frame_clip,
        ]
        for i, command in enumerate(command_button):
            command.grid(column=i, row=0)
            command.grid_columnconfigure(1, weight=1)
        self.file_dialog.grid(column=0, row=0, padx=(2, 2), pady=2)
        self.help_label.grid(column=1, row=0, padx=(2, 2), pady=2)
        # self.comb.grid(column=2, row=0, padx=(2, 2), pady=2)
        self.canvas.grid(column=0, row=0)
        # self.canvas.create_image(0, 0, image=self.image_tk, anchor=tk.NW)
        self.slider = tk.Scale(self.slider_bar, from_=0, to=0, orient='horizontal', length=self.width)
        self.slider.grid(sticky="NEWS")
    
    def display_image(self, frame: np.ndarray):
        """Display a frame on an app window
            This will be called when 
                1. Opened video file
                2. slidar bar changed
                3. left key or right key was pressed
        
        Args:
            frame: image frame
        """
        img = Image.fromarray(frame)
        img = img.resize((self.width, self.height))
        self.image_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self.image_tk, anchor=tk.NW)

    def create_help_window(self, fps, video_len, width, height):
        def show_video_info(window, fps, video_len, width, height):
            info_window = tk.Toplevel(window)
            info_window.title("Property")
            info_window.grab_set()
            fps_label = tk.Label(info_window, text=f"FRAME RATE\t: {fps:10}")
            frame_num_label = tk.Label(info_window, text=f"FRAME NUM\t: {video_len:10}")
            # TODO: Add video len
            # if fps != 0:
            #     video_len_label = tk.Label(info_window, text=f"VIDEO LEN\t: {video_len:10}")
            width_label = tk.Label(info_window, text=f"FRAME WIDTH\t: {width:10}")
            height_label = tk.Label(info_window, text=f"FRAME HEIGHT\t: {height:10}")
            label_list = [
                fps_label, 
                frame_num_label,
                width_label,
                height_label,
            ]
            for label in label_list:
                label.grid(sticky=tk.NW, padx=10, pady=3)

        def show_contributor_info(window):
            info_window = tk.Toplevel(window)
            info_window.title("Contributor")
            info_window.grab_set()
            greeting_label = tk.Label(info_window, text="Hello!")
            contributor_label = tk.Label(info_window)
            contributor_name_list = [
                "Contributor to this app:",
                "k2-gc",
            ]
            contributor_label.config(text="\n".join(contributor_name_list))
            greeting_label.grid(sticky=tk.NW, padx=20, pady=10)
            contributor_label.grid(sticky=tk.NW, padx=20, pady=10)
            
        help_window = tk.Toplevel(self.parent)
        help_window.grab_set()
        video_info = tk.Button(help_window, text="Video Info")
        # help_frame = tk.Frame(help_window, borderwidth=1, relief="solid")
        contributor_label = tk.Button(help_window, text="Contributor")
        video_info.grid(sticky=tk.NSEW, padx=20, pady=10)
        contributor_label.grid(sticky=tk.NSEW, padx=20, pady=10)
        video_info.config(command=lambda: show_video_info(help_window, fps, video_len, width, height))
        contributor_label.config(command=lambda: show_contributor_info(help_window))

    
    
    