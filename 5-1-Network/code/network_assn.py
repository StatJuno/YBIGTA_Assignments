from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class Data(BaseModel):
    gi: str
    team: str
    role: str
    name: str

data_store: List[Data] = []

@app.post("/list", response_model=List[Data])
def post_list():
    student_list = [
        Data(gi='23기', team='DE팀', role='전 부대장', name='이어흥'),
        Data(gi='24기', team='DE팀', role='팀장', name='임채림'),
        Data(gi='22기', team='DS팀', role='교육부장', name='김지훈'),
        Data(gi='24기', team='DE팀', role='부회장', name='조윤영'),
        Data(gi='24기', team='DS팀', role='회장', name='이동진')
    ]
    data_store.extend(student_list)
    return student_list
    
@app.get("/list", response_model=List[Data])
def get_list():
    return data_store

@app.put("/list/{name}", response_model=Data)
def put_list(name: str, data: Data):
    for i, d in enumerate(data_store):
        if d.name == name:
            data_store[i] = data
            return data
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/list/{name}", response_model=Data)
def delete_list(name: str):
    for i, d in enumerate(data_store):
        if d.name == name:
            data_store.pop(i)
            return d
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, log_level="info")

# 접속: localhost:8000/docs