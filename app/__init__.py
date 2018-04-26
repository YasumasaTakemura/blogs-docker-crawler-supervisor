import os
from env.settings import load_dotenv
load_dotenv()
if '.local' in os.listdir(os.getcwd()):
    os.environ['DATABASE_NAME'] = 'test'