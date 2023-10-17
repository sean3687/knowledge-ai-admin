from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating : Optional[int] = None
    
my_posts = [{"title": "title of post1", "content": "content pf post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return p


@app.get("/") #decorator
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post): #... means Body will be store in payload which is dictionary type in python
    #after we use class from pydantic, we can use new_post.title, new_post.content
    print(post.title)
    print("this is .dict", post.dict())
    print("this is post",post)
    return {"data":post}

@app.get("/posts/{id}")
def get_post(id):
    post = find_post()
    return { "post_detail": f"Here is post {id}" }


