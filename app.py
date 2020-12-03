import os
import pathlib

from cryptography.fernet import Fernet
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

here = pathlib.Path(__file__)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///test.db"
app.config["SECRET_KEY"] = os.urandom(24)
app.config["CRYPTO_KEY"] = "cfIBoF86lioHkcMjzIjUDmXLqVsGrhSAA9r3vHGd3-s="

db = SQLAlchemy(app)


def encrypt_pwd(pwd: str):
    key = app.config["CRYPTO_KEY"].encode()
    fernet = Fernet(key)

    return fernet.encrypt(pwd.encode()).decode()
