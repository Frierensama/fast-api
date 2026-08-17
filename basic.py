from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field, model_validator, field_validator, computed_field
from typing import List, Dict, Optional, Annotated, Type
import json
from tensei_schema import CharacterDetails, CharacterDetailsUpdate


app = FastAPI()

def load_data():
    with open('basic-x.json','r') as f:
        data = json.load(f)
    return data

def write_data(data):
    with open('basic-x.json','w') as f:
        json.dump(data,f, indent=2)

@app.get('/')
def home():
    return {'message':'root address endpoint'}

@app.get('/character/{character_name}')
def view_character(character_name:str = Path(...,description='name of a character',examples=['rudy','sylphy'])):
    data = load_data()
    if character_name not in data:
        raise HTTPException(status_code=404,detail='no such name endpoint')
    return data[character_name]

@app.get('/viewdata')
def view_data(wannasort:str = Query('asc',description='an element to sort')):
    data = load_data()

    if wannasort not in ['asc','desc']:
        raise HTTPException(status_code=400)

    return data

@app.post('/create_character')
def create_character(character:Dict[str,CharacterDetails]):
    stored_data = load_data()

    if len(character)>1:
        raise HTTPException(status_code=400,detail="insert one character at once.")
    
    character_name = list(character.keys())[0]
    character_details = list(character.values())[0]

    if character_name in stored_data:
        raise HTTPException(status_code=400,detail='name exists in db')

    stored_data[character_name] = character_details.model_dump()

    write_data(stored_data)

    return JSONResponse(status_code=201,content=f'success insertion of {character_name}')


@app.put('/update_character/{character_name}')
def update_details(character_name:str, character_details_update:CharacterDetailsUpdate):
    stored_data = load_data()

    if character_name not in stored_data:
        raise HTTPException(status_code=404,detail='no such character')

    stored_char_details = stored_data[character_name]

    details_to_update = character_details_update.model_dump(exclude_unset=True)

    for key,value in details_to_update.items():
        stored_char_details[key] = value

    character_updated = CharacterDetails(**stored_char_details)

    stored_data[character_name] = character_updated.model_dump()
    write_data(stored_data)

    return JSONResponse(status_code=200, content=f'success modified {character_name}')


@app.delete('/delete_character/{character_name}')
def delete_character(character_name:str):
    stored_data = load_data()

    if character_name not in stored_data:
        raise HTTPException(status_code=404,detail='no character with name')

    del stored_data[character_name]

    write_data(stored_data)

    return JSONResponse(status_code=204)