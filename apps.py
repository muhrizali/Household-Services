from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# initializing flask and related apps
app = Flask(__name__)
app.config["SECRET_KEY"] = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"

# # initializing sqlalchemy with flask
# class Base(DeclarativeBase):
#     pass
# db = SQLAlchemy(model_class=Base)

# # configure the database, initialize app with the extension
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# db.init_app(app)

# post-init:
# for including views
# import models
# import views, forms

# # create schemas
# with app.app_context():
#     db.create_all()
