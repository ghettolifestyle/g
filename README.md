# kb

this is a work in progress. very basic functionality for now

create markdown-based posts with yaml headers (title and date only) posts
locally, convert to html and template using jinja, push to s3 bucket using
boto.

if unfamiliar with s3, activate static web site hosting in bucket, add
policy for bucket and iam entity you're using to access the aws api. use
cloudfront if your dad works at nsa

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

post will be created as draft. posts become drafts when first character in
relative post file path is an underscore ("_")

type away on keyboard until post is good or, alternatively, until satisfied.
toggle post visibility, i.e. transition from draft to post uwu. html files
will be constructed in a temp dir, then synced to s3 automatically

__NOTE:__ drafts will NOT be synced

```shell
% ./kb.py t

[0] _test.md (DRAFT)
[1] groundhog_day.md
[2] the_state_of_things.md
toggle> 0
```

want to remove post from blog? easy, just toggle visibility on a non-draft
post. it will be pruned from the bucket and its markdown file will be
renamed to include a leading underscore. local directory is source of truth

## what it doesn't do and how to fix (maybe)

+ check whether the contents of a post in the s3 bucket match those of a
  local post. fix: use an obscure hashing algorithm and compare checksums
