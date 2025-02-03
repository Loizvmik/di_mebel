from fastapi import FastAPI


app = FastAPI()

@app.get("/furniture")
def read_furniture():
    furniture = 