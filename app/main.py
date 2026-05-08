from fastapi import FastAPI
from api.routes.todo import todo_router
from tortoise.contrib.fastapi import register_tortoise  

app = FastAPI()
app.include_router(todo_router)
register_tortoise(
    app, 
    db_url="sqlite://db.sqlite3", 
    add_exception_handlers=True,
    generate_schemas=True,
    modules={"models": ["api.models.todo"]})

@app.get("/")
def index():
    return {"status": "todo api is running"}