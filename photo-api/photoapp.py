from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Rajiv Digital Photo Studio API is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "application": "rajiv-photo-platform"}