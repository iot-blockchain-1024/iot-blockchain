from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import db
from app.application import create_app

app = create_app('development')

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
