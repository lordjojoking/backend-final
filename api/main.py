from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.predictor import MandiPredictor

app = FastAPI()

# ── CORS – allow mobile app & local dev to reach the API ─────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = MandiPredictor()


@app.get("/")
def home():
    return {"message": "Mandi ML API running"}


@app.get("/commodities/")
def get_commodities():
    return {"commodities": predictor.commodities}


@app.get("/predict/")
def predict(date: str, commodity: str):
    price = predictor.predict_price(date, commodity)
    return {"predicted_modal_price": price}


@app.get("/predict_range/")
def predict_range(commodity: str, start_date: str, days: int = 30):
    """Return predicted prices for `days` consecutive days starting from `start_date`."""
    predictions = predictor.predict_range(start_date, commodity, days)
    return {"commodity": commodity, "predictions": predictions}


@app.get("/best_sowing/")
def best_sowing(commodity: str, crop_duration: int = 90):
    result = predictor.best_sowing_window(commodity, crop_duration)
    return result