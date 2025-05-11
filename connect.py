import configparser
from mongoengine import connect


config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
domain = config.get('DB', 'domain')
db_name = config.get('DB', 'db_name')

# connect to cluster on AtlasDB with connection string

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority&appName=Cluster0""", ssl=True)
