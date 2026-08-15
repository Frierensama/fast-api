from fastapi import FastAPI, HTTPException, Path
import json

app = FastAPI()

def load_data():
    with open('basic-x.json','r') as f:
        data = json.load(f)

    return data


@app.get('/')
def hello():
    return {'message':'whatever'}


@app.get('/character/{path_param}')
def character(path_param:str = Path(...,description='character name',example='rudy')):
    data = load_data()
    if path_param in data:
        return data[path_param]
    raise HTTPException(status_code=404,detail=f"no character named {path_param}")