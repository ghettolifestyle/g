#!/usr/bin/env python3
from sys import path, argv, exit as sysexit
from os import stat
from shutil import copytree
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
        meta={
            "title": "kevin mai's personal blog",
            "cool_tagline": "boomer mindset. now with more serifs",
            "links": {
                "github": "https://github.com/ghettolifestyle",
                "linkedin": "https://www.linkedin.com/in/kevin-mai-324b86171/",
                "goodreads": "https://www.goodreads.com/user/show/157784359-kevin-mai",
                "rss": "/atom.xml"
            }
        },
        base_dir=f"{HOME_DIR}/Documents/aws_blog",
        bucket="kmai-xyz-yc9qtscxpemdfxkbncjfjuxxu5q3j",
        jinja_env=Environment(
            loader=FileSystemLoader(f"{HOME_DIR}/Documents/aws_blog/templates")
        )
    )

    try:
        stat(config.base_dir)
    except FileNotFoundError:
        copytree("blog/", config.base_dir)

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
        blog.sync_state()
    elif OP == "c":
        print(blog.get_unsynced_posts())
    else:
        print_usage()

blog.sync_state()