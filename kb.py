from sys import path, argv, exit as sysexit
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
path.append("pkg/")
from bloglib import Blog, Config

HOME_DIR = f"{str(Path.home())}"

def print_usage():
    """ Prints program usage information and exits """
    print("to be implemented")
    sysexit(1)

if __name__ == "__main__":
    config = Config(
        base_dir=f"{HOME_DIR}/git/kb/blog",
        bucket="kmai-xyz-yc9qtscxpemdfxkbncjfjuxxu5q3j",
        jinja_env=Environment(
            loader=FileSystemLoader(f"{HOME_DIR}/git/kb/templates")
        )
    )

    blog = Blog(
        config=config
    )

    argv.pop(0)

    try:
        OP = argv[0]
    except IndexError:
        print_usage()

    if OP == "l":
        print(
            blog.list_posts()
        )
    elif OP == "p":
        print(
            blog.select_posts(
                "publish> ",
                config.draft_dir
            )
        )
    else:
        print_usage()
