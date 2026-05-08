from fastapi import APIRouter, HTTPException
from api.models.todo import Todo
from api.schemas.todo import GetTodo, PostTodo, PutTodo

todo_router = APIRouter(prefix="/api", tags=["Todo"])

@todo_router.get("/")
async def all_todos():
    data = Todo.all()
    todos = await GetTodo.from_queryset(data)
    return {"todos": todos}


@todo_router.post("/")
async def post_todo(todo: PostTodo):
    row = await Todo.create(**todo.dict(exclude_unset=True))
    return await GetTodo.from_tortoise_orm(row)


@todo_router.put("/{todo_id}")
async def update_todo(todo_id: int, todo: PutTodo):
    data = todo.dict(exclude_unset=True)
    exists = await Todo.filter(id=todo_id).exists()
    if not exists:
        raise HTTPException(status_code=404, detail="Todo not found")
    await Todo.filter(id=todo_id).update(**data)
    return {"message": "Todo updated successfully"}


@todo_router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    exists = await Todo.filter(id=todo_id).exists()
    if not exists:
        raise HTTPException(status_code=404, detail="Todo not found")
    await Todo.filter(id=todo_id).delete()
    return {"message": "Todo deleted successfully"}
