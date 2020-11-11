from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from src.model import spell_number

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

@app.get('/')
def read_form():
    return 'hello world'