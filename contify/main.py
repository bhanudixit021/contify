from fastapi import FastAPI
from helpers import load_from_disk
from apps.transducers.controllers import router as search_index_routers
import os

app = FastAPI()
app.include_router(search_index_routers)



#load exisiting data from disk
load_from_disk()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)