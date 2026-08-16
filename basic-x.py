from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field, model_validator, field_validator, computed_field
from typing import List, Dict, Optional, Annotated, Type
import json
from tensei_schema import CharacterDetails


app = FastAPI()

@app.get('/')
def home():
    return {'message':'root address endpoint'}

def load_data():
    with open('basic-x.json','r') as f:
        data = json.load(f)
    return data

def write_data(data):
    with open('basic-x.json','w') as f:
        json.dump(data,f, indent=2)

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

@app.post('/create_character')
def create_character(character:Dict[str,CharacterDetails]):
    stored_data = load_data()

    if len(character)>1:
        raise HTTPException(status_code=400,detail="insert one character at once.")
    
    character_name = list(character.keys())[0]
    character_details = list(character.values())[0]

    if character_name in stored_data:
        raise HTTPException(status_code=401,detail='name exists in db')

    stored_data[character_name] = character_details.model_dump()

    write_data(stored_data)

    return JSONResponse(status_code=201,content=f'success insertion of {character_name}')