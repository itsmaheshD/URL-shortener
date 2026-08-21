from fastapi import FastAPI

app=FastAPI(
    title= "URL Designer",
    version="1.0",
    description="A URL designer which shortens the URL using base62 encoding",
)

@app.get("/")
def hello_word():
    return "hello word"

