"""Contains FireO ORMs for Movie and Ticket and Pydantic Models for MovieListRequest, MovieRequest, 
TicketRequest and TicketResponse"""

from typing import List
from fireo.models import Model
from fireo.fields import IDField, TextField, NumberField, ListField, BooleanField, DateTime
from pydantic import BaseModel

class Movie(Model):
    """Movie class for FireO ORM"""
    id =  IDField()
    movie_title = TextField()
    start_time = TextField()
    end_time = TextField()
    seats_booked = ListField()
    ticket_price = NumberField()
    isles = ListField()
    seats_per_isle = NumberField()
    booked_out = BooleanField()

class Ticket(Model):
    """Ticket class for FireO ORM"""
    id = IDField()
    timestamp = DateTime(auto=True)
    movie_id = TextField()
    seats_booked = ListField()
    amount = NumberField()

class MovieListRequest(BaseModel):
    """Pydantic Model to validate MovieListRequest"""
    movie_title: str
    id: str
    start_time: str
    end_time: str
    seats_booked: List[str]

class MovieRequest(BaseModel):
    """Pydantic Model to validate MovieRequest"""
    movie_title: str
    id: str
    start_time: str
    end_time: str
    seats_booked: List[str]
    ticket_price: float
    isles: List[str]
    seats_per_isle: int

class TicketRequest(BaseModel):
    """Pydantic Model to validate TicketRequest"""
    movie_id: str
    number_of_tickets: int

class TicketResponse(BaseModel):
    """Pydantic Model to validate TicketResponse"""
    id: str
    timestamp: str
    movie_id: str
    seats_booked: List[str]
    amount: float
    movie_title: str
    start_time: str
    end_time: str
