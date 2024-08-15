import tkinter as tk

from .utils import get_logger
from .app_controller import Controller

def run_app():
    logger = get_logger()
    logger.info("Start App")
    root = tk.Tk()
    controller = Controller(root)
    root.mainloop()
    logger.info("Stop App")


if __name__ == "__main__":
    run_app()
