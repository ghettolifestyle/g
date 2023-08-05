class Config:
  def __init__(self, meta, base_dir, bucket, jinja_env):
    self.meta = meta
    self.base_dir = base_dir
    self.bucket = bucket
    self.jinja_env = jinja_env
