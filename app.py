from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import get_session
from models import Movie

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/movies")
def get_movies(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie)).all()
    return movies

@app.post("/movies")
def create_movie(movie: Movie, session: Session = Depends(get_session)):
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    session.delete(movie)
    session.commit()
    return {"message": "Movie deleted successfully"}
