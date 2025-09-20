from jinja_utils import load_jinja_env

# 使用默认路径
env = load_jinja_env()
template = env.get_template("autofunc/default.jinja")