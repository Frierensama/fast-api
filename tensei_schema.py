from pydantic import BaseModel,Field, model_validator, field_validator, computed_field, TypeAdapter
from typing import List, Dict, Optional, Annotated, Type

# character details schema
class CharacterDetails(BaseModel):
    title:str
    type:List[str]
    class_:str
    age:int
    married:List[str]

    @field_validator('age')
    @classmethod
    def age_field_validator(cls,value):
        if value<0:
            raise ValueError('invalid age')
        return value

    @computed_field
    @property
    def spouse_count(self)->int:
        return len(self.married)


few_char_details = {
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

adaptor = TypeAdapter(Dict[str,CharacterDetails])
validated_char_details = adaptor.validate_python(few_char_details)

print(validated_char_details)
