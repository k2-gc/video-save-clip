import logging
from pathlib import Path

def get_logger():
    """Get logger.
        Get same name logger and set format and so on.

    """
    logger = logging.getLogger("logger")
    if logger.hasHandlers():
        return logger
    st_handler = logging.StreamHandler()
    format = "[%(levelname)s] %(message)s"
    st_handler.setFormatter(logging.Formatter(format))
    logger.setLevel(logging.INFO)
    logger.addHandler(st_handler)
    return logger

def get_suffix(file_name, with_ext=True):
    """Get suffix
        Example:
            Args: 
                file_name = "tmp.mp4"
                with_ext = True

            Case1: "tmp_1.mp4" does not exist
                Returns:
                    "tmp_1.mp4"
            Case2: "tmp_1.mp4" exists
                Returns:
                    "tmp_2.mp4"

        Args:
            file_name: file name to get unique suffix
            with_ext: If True, file_name with ext will be returned
                      Only file_name will be returned otherwise
        
        Returns:
            str: file name with unique suffix
    """
    file_name = Path(file_name)
    ext = file_name.suffix
    basename = file_name.stem
    i = 1
    while True:
        if with_ext:
            outpath = Path(f"{basename}_{i}{ext}")
        else:
            outpath = Path(f"{basename}_{i}")

        if not outpath.exists():
            return str(outpath)
        i += 1