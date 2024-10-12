from flask import Flask

app=Flask(__name__)
app.config['SECRET_KEY']='Dedorz'
from app import routes