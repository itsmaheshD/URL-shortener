from fastapi import FastAPI
from url_designer.api.routes.urls import router


app=FastAPI(
    title= "URL Designer",
    version="1.0",
    description="A URL designer which shortens the URL using base62 encoding",
)

@app.get("/")
def hello_word():
    return "hello word"

app.include_router(router)

