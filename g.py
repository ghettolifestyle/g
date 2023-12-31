#!/usr/bin/env python3
from sys import path, argv, exit as sysexit
from os import stat, makedirs
from shutil import copytree
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
path.append("pkg/")
from bloglib import Blog, Config

HOME_DIR = f"{str(Path.home())}"

def print_usage():
    """ Prints program usage information and exits """

    print("""./g.py {
        \tn [title]\t-> create new draft
        \tt\t\t-> toggle post visibility (draft/undraft)
        \ts\t\t-> manually sync state (incl. pruning)\n}""")

    sysexit(1)

if __name__ == "__main__":
    config = Config(
        meta={
            "title": "kevin mai's personal blog",
            "author": "kevin mai",
            "url": "https://kmai.xyz",
            "cool_tagline": "hypnotically ugly",
            "quote_under_posts": {
                "body": "Devenir immortel, et puis mourir.",
                "source": "Parvulesco"
            },
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
        makedirs(f"{config.base_dir}/posts", exist_ok=True)

        copytree("res/templates", config.base_dir)

    blog = Blog(
        config=config
    )

    # just gonna pretend this is bash for now
    argv.pop(0)

    try:
        OP = argv[0]
    except IndexError:
        print_usage()

    if OP == "l":
        print(
            blog.list_posts()
        )
    elif OP == "n":
        argv.pop(0)

        try:
            blog.create_post(argv[0])
        except IndexError:
            blog.create_post()
    elif OP == "t":
        blog.toggle_post_visibility()
    elif OP == "s":
        blog.sync_state()
    else:
        print_usage()

blog.sync_state()
