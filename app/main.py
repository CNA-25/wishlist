from fastapi import FastAPI

app = FastAPI()

#load the wishlist
@app.get("/")
def read_root():
    return { "Hello": "Rahti2", "v": "0.4" }

#recieve an item id, take the Token logged user id, and add that to the wishlist
@app.post("/wishlist/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}

#recieve an item id, take the Token logged user id, and Remove that to the wishlist (if it exists)
@app.delete("/wishlist/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}