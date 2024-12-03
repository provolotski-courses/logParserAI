from environs import Env
env = Env()
env.read_env()

#logger settings
LOG_DIR = env('LOG_DIR')
LOG_FILE = env('LOG_FILE')
LOG_LEVEL = env('LOG_LEVEL')


