from environs import Env

env = Env()
env.read_env()

ENVIRONMENT = env.str("ENVIRONMENT")
DEBUG = env.bool("DEBUG", False)
DATABASE_URL = env.str("DATABASE_URL")
