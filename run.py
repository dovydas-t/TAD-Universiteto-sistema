import os
from app import create_app
from app.models.auth import create_hardcoded_admin
from app.config import config

config_name = os.environ.get('FLASK_CONFIG', 'default')
app = create_app(config[config_name])


if __name__ == '__main__':
    app.run()