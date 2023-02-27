from pathlib import Path


def get_project_root():
    root_dir = Path(__file__).absolute().parent.parent.parent
    return root_dir
