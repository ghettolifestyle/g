from os import listdir
from pathlib import Path
from boto3 import client
from boto3 import Session
import markdown
from yaml import load, Loader
from shutil import move

class Blog:
    def __init__(self, config):
        session = Session(profile_name='general')
        self.s3_client = session.client("s3")
        self.config = config
        self.post_dir = f"{config.base_dir}/posts"
        self.sync_post_dir = f"{config.base_dir}/out/p"
        self.bucket = self.config.bucket

    def list_posts(self):
        bucket_contents = {}
        
        try:
            bucket_contents = self.s3_client.list_objects(
                Bucket=self.bucket,
                Prefix="p/"
            )["Contents"]
        except ClientError as e:
            return e

        synced_posts = [post["Key"].split("/")[1] for post in bucket_contents]
        unsynced_posts = scandir(self.post_dir)

        # list unsynced, unpublished drafts
        print("unsynced in drafts dir:")
        for index, post in enumerate(unsynced_posts):
            print(f"\t[{index}] {post.name}")

        print()

        # list synced posts
        print("synced to s3:")
        for index, post in enumerate(synced_posts):
            print(f"\t[{index}] {post}")

    def sync_posts(self):
        posts = listdir(self.post_dir)

        for post in posts:
            try:
                self.s3_client.upload_file(
                    post,
                    self.bucket
                )
            except ClientError as e:
                return e

    def select_posts(self, prompt, dir):
        dir_contents = listdir(dir)
        selected_posts = []

        for index, post in enumerate(dir_contents):
            print(f"[{index}] {post}")

        user_selection = input(prompt)

        if len(user_selection) < 1:
            print("select at least one post")
            print()

            select_posts(prompt, dir)
        elif len(user_selection) == 1:
            selected_posts.append(dir_contents[int(user_selection)])
        else:
            selected_posts = []
            for index in user_selection.split(","):
                selected_posts.append(dir_contents[int(index)])

        return selected_posts

    def publish_posts(self):
        selected_posts = select_posts(
            "publish> ",
            self.config.post_dir
        )

        for post in selected_posts:
            abs_draft_path = f"{self.post_dir}/{post}"
            # e.g. "2.md" -> ["2", "md"] -> "2" + ".html"
            abs_post_path = f"{self.sync_post_dir}/{post.split('.')[0]}.html"

            with open(abs_post_path) as post_file:
                # index 0 == yaml header as dict
                # index 1 == post contents in markdown
                post_metadata, post_content = parse_post(abs_draft_path)
                # render content, insert html into dict for jinja to template
                post_metadata["content"] = render_markdown(post_content)

                post_file.write(render_jinja_template("post.html"))
            
    # friendly helper functions

    def render_jinja_template(self, template, vars):
        env = self.config.jinja_env
        post_template = env.get_template(template)

        # accepts dict. how convenient
        rendered_template = post_template.render(
            vars
        )

        return rendered_template

    def render_markdown(self, markdown_content):
        return markdown.markdown(markdown_content)

    def parse_post(self, file):
        yaml_header = {}
        post_content = ""

        with open(file, "r") as post_file: 
            post_file_lines = f.readlines()

            triple_dash_count = 0
            yaml_header_lines = []
            yaml_header_end_line = 0

            for line in post_file_lines:
                line = line.strip()

                if triple_dash_count % 2 == 0 and triple_dash_count > 0:
                    break

                if line == "---":
                    triple_dash_count += 1
                else:
                    yaml_header_lines.append(line)

                yaml_header_end_line += 1

            yaml_header = load("\n".join(yaml_header_lines), Loader=Loader)

            # if user left line empty after yaml header, increment
            # to avoid parsing unnecessary newline
            if lines[yaml_header_end_line] == "\n":
                yaml_header_end_line += 1

            post_content = "".join(lines[yaml_header_end_line:])

        return yaml_header, post_content
