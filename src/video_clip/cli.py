import fire

from .app_sample import run_app

def help():
    print("Usage: ")
    print("Run comand 'video-clip run' on terminal or comannd prompt.")

video_clip_app = {
    "run": run_app,
    "help": help,
}

def app() -> None:
    """Cli app
    """
    fire.Fire(video_clip_app)

if __name__ == "__main__":
    app()