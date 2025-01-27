from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "Hello": "Rahti2", "v": "0.4" }

#get info about one specific item
@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}

#recieve an item id, take the Token logged user id, and add that to the wishlist
@app.post("/wishlist/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}

#send an item ID to be added to the users cart
@app.post("/cart/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}