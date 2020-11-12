from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates/")



class TextArea(BaseModel):
    content: str


@app.get('/')
def form_post(request: Request):
    result = 'Type a question'
    return templates.TemplateResponse('form2.html', context={'request': request, 'result': result, 'Titre': TextArea, 'Question': TextArea})


@app.post('/')
def form_post(request: Request, Titre: str=Form(...), Question: str=Form(...)):
    result = 'ça marche' 
    return templates.TemplateResponse('form2.html', context={'request': request, 'result': result, 'Titre': TextArea, 'Question': TextArea})