# kb

this is a work in progress. very basic functionality for now

create markdown-based posts with yaml headers (title and date only) posts
locally, convert to html and template using jinja, push to s3 bucket using
boto

## requirements

you need

+ an s3 bucket
+ an aws profile
+ a python interpreter
+ some packages (Jinja2, boto3, markdown, pyyaml)
+ computer

## usage

adjust metadata, base_dir, bucket_name, literally everything in config object instantiation in `kb.py`

```python
config = Config(
    meta={
        "title": "kevin mai's personal blog",
        "author": "kevin mai",
        "url": "https://kmai.xyz",
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
```

make file executable, execute file

```shell
% chmod u+x ./kb.py
% ./kb.py n "<optional_title_you_will_be_prompted>"
% vim "<base_dir>/posts/"   # find post and press enter, add metadata and body
```

type away on keyboard until post is good or, alternatively, until satisfied.
construct html files in temp dir and sync

```shell
% ./kb.py p
```

want to remove post? easy, just delete from `self.post_dir`, then resync
("automatic" in future). script will compare state and remove accordingly.
local directory is source of truth

```
% rm "<base_dir>/posts/<rel_path_to_post>"
% ./kb.py p
```

## what it doesn't do and how to fix (maybe)

+ check whether the contents of a post in the s3 bucket match those of a
  local post. fix: use an obscure hashing algorithm and compare checksums
