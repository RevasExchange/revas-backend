from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.core.config import settings
from app.routers import auth, profile, waitlist, location, products, populators
from app.models import models
from app.core.database import engine


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
models.Base.metadata.create_all(bind=engine)


origins = [settings.CLIENT_ORIGIN]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=["Auth"], prefix="/api/auths")
app.include_router(profile.router, tags=["Profile"], prefix="/api/profiles")
app.include_router(waitlist.router, tags=["Waitlist"], prefix="/api/waitlists")
app.include_router(location.router, tags=["Location"], prefix="/api/locations")
# app.include_router(products.router, tags=["Products"], prefix="/api/products")

app.include_router(populators.router, tags=["Populators"], prefix="/api/populators")


@app.get("/api/check")
async def check():
    return {"status": "ok"}
