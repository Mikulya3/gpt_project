from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml

def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        return config

config = load_config()
database_url = config['database_url']


engine = create_engine(database_url, echo=True)
Base = declarative_base()
Session = sessionmaker()