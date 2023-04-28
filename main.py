"""FastAPIs to book a movie. User can get all movies, get more details about a specific movie 
and book tickets to a movie. 

Uses FireO for Movie and Ticket ORM and Pydantic for Validating  MovieListRequest, MovieRequest, 
TicketRequest and TicketResponse. See models module for more info.
"""

import random
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from models import Movie, Ticket, MovieListRequest, MovieRequest, TicketRequest, TicketResponse


app = FastAPI(
    title = "FastAPIs to book a movie",
    description = "APIs to see avaiable movies, get more details about a movie and book tickets to a movie. This implemetation uses Firebase as the database, FireO as the ORM and Pydantic for custom validation.",
    version = "0.0.1",
    contact={
        "name": "Manish Bhagat",
    }
)

db: List[Movie] = [
    Movie(
        id = "cQD8u3JvVUbDuAByNzNY",
        movie_title = "Spider-Man: No Way Home",
        start_time = "28 Apr 2023 03:35 PM",
        end_time = "28 Apr 2023 04:45 PM",
        seats_booked = [],
        ticket_price = 215,
        isles = ["A", "B", "C", "D","E"],
        seats_per_isle = 10,
        booked_out = False
    ),
    Movie(
        id = "TTGCgiDFiPm1y2ei8QqT",
        movie_title = "Avatar: The Way of Water",
        start_time = "28 Apr 2023 07:35 PM",
        end_time = "28 Apr 2023 09:45 PM",
        seats_booked = [],
        ticket_price = 350,
        isles = ["A", "B", "C", "D","E"],
        seats_per_isle = 10,
        booked_out = False
    )
]

for d in db:
    d.save()

@app.get("/api/v1/movies", response_model=Dict[str, MovieListRequest])
def get_all_movies():
    """Returns all movies avaiables in a trucated form."""
    all_movies = Movie.collection.fetch()
    movies = {}
    for mov in all_movies:
        movies[mov.id] = {}
        movies[mov.id]["movie_title"] = mov.movie_title
        movies[mov.id]["id"] = mov.id
        movies[mov.id]["start_time"] = mov.start_time
        movies[mov.id]["end_time"] = mov.end_time
        movies[mov.id]["seats_booked"] = mov.seats_booked
    return movies

@app.get("/api/v1/movies/{movie_id}", response_model=MovieRequest)
def specific_movie(movie_id: str):
    """Returns details about a single movie."""
    movie = Movie.collection.get(movie_id)
    if movie:
        requested_movie = MovieRequest(
            movie_title = movie.movie_title,
            id = movie.id,
            start_time = movie.start_time,
            end_time = movie.end_time,
            seats_booked = movie.seats_booked,
            ticket_price = movie.ticket_price,
            isles = movie.isles,
            seats_per_isle = movie.seats_per_isle
        )
        return requested_movie
    raise HTTPException(
        status_code=404,
        detail="Movie with the given id was not found"
    )

@app.post("/api/v1/book", response_model=TicketResponse)
def book_ticket(ticket_request: TicketRequest):
    """Books tickets and returns ticket with details."""
    movie = Movie.collection.get(ticket_request.movie_id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given id was not found"
        )
    if movie.booked_out:
        raise HTTPException(
            status_code=406,
            detail=f"Movie {movie.movie_title} for time slot [{movie.start_time} - {movie.end_time}] is completely booked"
        )

    number_of_tickets = ticket_request.number_of_tickets
    if number_of_tickets <= 0:
        raise HTTPException(
            status_code=400,
            detail="Bad request. Can't buy zero or negative tickets"
        )


    isles, seats_per_isle, already_booked = movie.isles, movie.seats_per_isle, movie.seats_booked
    if number_of_tickets + len(movie.seats_booked) > (len(isles) * seats_per_isle):
        raise HTTPException(
            status_code=400,
            detail="Not enough tickets. Reduce number of tickets to book or Try another movie"
        )
    
    booking_seats = []
    for i in range(ticket_request.number_of_tickets):
        while True:
            tic = isles[random.randint(0, len(isles) - 1)]
            tic += str(random.randint(1, seats_per_isle))

            if tic not in set(already_booked):
                booking_seats.append(tic)
                break


    already_booked = already_booked + booking_seats
   
    movie.seats_booked = already_booked
    if len(movie.seats_booked) == len(movie.isles) * movie.seats_per_isle:
        movie.booked_out = True
    movie.update()

    tic = Ticket(
        movie_id = movie.id,
        seats_booked = booking_seats,
        amount = movie.ticket_price * len(booking_seats)
    )
    tic.save()

    return TicketResponse(
        id = tic.id,
        timestamp = str(tic.timestamp),
        movie_id = tic.movie_id,
        seats_booked = tic.seats_booked,
        amount = tic.amount,
        movie_title = movie.movie_title,
        start_time = movie.start_time,
        end_time = movie.end_time
    )
