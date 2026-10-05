# -*- coding: utf-8 -*-
"""روتر پیش‌بینی قیمت"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import logging

from app.models.price_predictor import price_predictor

router = APIRouter()
logger = logging.getLogger(__name__)

class PredictionRequest(BaseModel):
    area: float = Field(..., gt=0, le=1000, description="متراژ ملک (متر مربع)")
    rooms: int = Field(1, ge=0, le=10, description="تعداد اتاق")
    year_built: int = Field(..., ge=1300, le=1500, description="سال ساخت")
    city: str = Field(..., min_length=1, max_length=100, description="شهر")
    district: str = Field(..., min_length=1, max_length=100, description="منطقه یا محله")
    property_type: str = Field("apartment", min_length=1, max_length=20)
    condition: str = Field("normal", min_length=1, max_length=20)

    class Config:
        schema_extra = {"example": {
            "area": 85, "rooms": 2, "year_built": 1400,
            "city": "تهران", "district": "الهیه",
            "property_type": "apartment", "condition": "new"
        }}

class PredictionResponse(BaseModel):
    predicted_price: int
    confidence: float | None
    price_per_m2: int
    input_features: dict
    model_info: dict

@router.post("/", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    if not price_predictor.is_trained:
        raise HTTPException(status_code=503, detail="مدل آموزش ندیده است. لطفاً اول مدل را آموزش دهید.")

    try:
        input_data = request.dict()
        predicted_price = price_predictor.predict(input_data)
        if predicted_price is None:
            raise HTTPException(status_code=500, detail="خطا در پیش‌بینی قیمت")

        price_per_m2 = int(predicted_price / request.area)

        return PredictionResponse(
            predicted_price=int(predicted_price),
            confidence=None,
            price_per_m2=price_per_m2,
            input_features=input_data,
            model_info={
                "model_type": "RandomForestRegressor",
                "is_trained": True,
                "features_used": price_predictor.numerical_features + price_predictor.categorical_features,
            },
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("خطا در پیش‌بینی")
        raise HTTPException(status_code=500, detail="خطا در پیش‌بینی")

@router.get("/sample")
async def get_sample_prediction():
    sample_request = PredictionRequest(
        area=85, rooms=2, year_built=1400, city="تهران",
        district="الهیه", property_type="apartment", condition="new",
    )
    return await predict_price(sample_request)

@router.get("/features")
async def get_model_features():
    return {
        "numerical_features": price_predictor.numerical_features,
        "categorical_features": price_predictor.categorical_features,
        "target_feature": price_predictor.target_feature,
        "is_trained": price_predictor.is_trained,
    }
