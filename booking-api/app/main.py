from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Photography Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://snehaldigitalphoto.com",
        "https://www.snehaldigitalphoto.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Booking(BaseModel):
    name: str
    email: EmailStr
    mobile: str

bookings = []

@app.get("/")
def home():
    return {"message": "Photography Booking API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/bookings")
def get_bookings():
    return bookings

@app.post("/bookings")
def create_booking(booking: Booking):
    booking_data = booking.dict()
    bookings.append(booking_data)
    return {
        "message": "Booking created successfully",
        "booking": booking_data
    }
