from fastapi import FastAPI
from application.routes.RAuth import router as auth_router
from application.routes.RUser import router as user_router
from application.routes.RBooking import router as book_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="MontainAPI")

app.include_router(auth_router) 
app.include_router(user_router)
app.include_router(book_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensaje": "API Montain funcionando"}
