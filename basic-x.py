from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel,Field, model_validator, field_validator, computed_field, TypeAdapter
from typing import List, Dict, Optional, Annotated, Type
import json
from tensei_schema import CharacterDetails


app = FastAPI()

char_details = {
        "aisa":{
            "title" :"imouto",
            "type" : ["maid","chloe"],
            "class_":"beyond god",
            "age":18,
            "married":["ars"]
        },
        "paul":{
            "title":"father",
            "type":["swordsman","sacrifice"],
            "class_":"king",
            "age":38,
            "married":["zenith","lilia"]
        }
}


@app.get('/')
def home():
    return {'message':'root address endpoint'}

def load_data():
    with open('basic-x.json','r') as f:
        data = json.load(f)
    return data

@app.get('/character/{path_param}')
def view_character(path_param:str = Path(...,description='name of a character',examples=['rudy','sylphy'])):
    data = load_data()
    if path_param not in data:
        raise HTTPException(status_code=404,detail='no such name endpoint')
    return data[path_param]

@app.get('/viewdata')
def view_data(wannasort:str = Query('asc',description='an element to sort')):
    data = load_data()

    if wannasort not in ['asc','desc']:
        raise HTTPException(status_code=400)

    sorted_data = sorted(data.values(), key=lambda x: x.get('age'),reverse =True if wannasort == 'desc' else False)
    return sorted_data