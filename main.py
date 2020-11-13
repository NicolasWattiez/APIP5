from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from preprocess import clean_title_question
import joblib

app = FastAPI()
templates = Jinja2Templates(directory="templates/")



class TextArea(BaseModel):
    content: str


@app.get('/')
def form_post(request: Request):
    result = 'Type a question'
    return templates.TemplateResponse('form2.html', context={'request': request, 'result': result, 'Titre': TextArea, 'Question': TextArea})


@app.post('/')
async def form_post(request: Request, Titre: str=Form(...), Question: str=Form(...)):

    clean_text = clean_title_question(Titre, Question)
    tag_preprocess = joblib.load('data/tag_preprocess.sav')
    model = joblib.load('data/finalized_model.sav')
    y_prediction = model.predict(clean_text)
    result = tag_preprocess.inverse_transform(y_prediction)

    return templates.TemplateResponse('form2.html', context={'request': request, 'result': result, 'Titre': TextArea, 'Question': TextArea})