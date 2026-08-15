from fastapi import FastAPI, HTTPException, Path, Query
import json

app = FastAPI()

def load_data():
    with open('basic-x.json','r') as f:
        data = json.load(f)

    return data


@app.get('/')
def hello():
    return {'message':'whatever'}

# path param
@app.get('/character/{path_param}')
def character(path_param:str = Path(...,description='character name',example='rudy')):
    data = load_data()
    if path_param in data:
        return data[path_param]
    raise HTTPException(status_code=404,detail=f"no character named {path_param}")

# query param
@app.get('/view')
def viewall(sort_param:str = Query('asc',description='desc or asc - sorting param')):
    data = load_data()
    if sort_param not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='wrong sort param. use asc or desc')
    
    data = sorted( data.values(), key= lambda x : x.get('age'), reverse= True if sort_param == 'desc' else False)
    return data