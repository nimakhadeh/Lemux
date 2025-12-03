# -*- coding: utf-8 -*-
"""روتر پیش‌بینی قیمت"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging

from ...app.models.price_predictor import price_predictor

router = APIRouter()
logger = logging.getLogger(__name__)

class PredictionRequest(BaseModel):
    """مدل درخواست پیش‌بینی"""
    
    area: float = Field(..., gt=0, description="متراژ ملک (متر مربع)")
    rooms: int = Field(1, ge=0, le=10, description="تعداد اتاق")
    year_built: int = Field(..., ge=1300, le=1500, description="سال ساخت")
    city: str = Field(..., description="شهر")
    district: str = Field(..., description="منطقه یا محله")
    property_type: str = Field("apartment", description="نوع ملک")
    condition: str = Field("normal", description="وضعیت ملک")
    
    class Config:
        schema_extra = {
            "example": {
                "area": 85,
                "rooms": 2,
                "year_built": 1400,
                "city": "تهران",
                "district": "الهیه",
                "property_type": "apartment",
                "condition": "new"
            }
        }

class PredictionResponse(BaseModel):
    """مدل پاسخ پیش‌بینی"""
    
    predicted_price: int
    confidence: float
    price_per_m2: int
    input_features: dict
    model_info: dict

@router.post("/", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    """پیش‌بینی قیمت ملک بر اساس ویژگی‌های ورودی"""
    
    if not price_predictor.is_trained:
        raise HTTPException(
            status_code=503, 
            detail="مدل آموزش ندیده است. لطفاً اول مدل را آموزش دهید."
        )
    
    try:
        # تبدیل درخواست به دیکشنری
        input_data = request.dict()
        
        # پیش‌بینی قیمت
        predicted_price = price_predictor.predict(input_data)
        
        if predicted_price is None:
            raise HTTPException(status_code=500, detail="خطا در پیش‌بینی قیمت")
        
        # محاسبه قیمت هر متر
        price_per_m2 = int(predicted_price / request.area)
        
        # اعتماد به پیش‌بینی (بر اساس تجربه - می‌تواند بهبود یابد)
        confidence = 0.85  # این می‌تواند بر اساس معیارهای مدل محاسبه شود
        
        response = PredictionResponse(
            predicted_price=int(predicted_price),
            confidence=confidence,
            price_per_m2=price_per_m2,
            input_features=input_data,
            model_info={
                "model_type": "RandomForestRegressor",
                "is_trained": True,
                "features_used": price_predictor.numerical_features + price_predictor.categorical_features
            }
        )
        
        logger.info(f"پیش‌بینی انجام شد: {predicted_price:,.0f} تومان برای ملک {request.area} متری")
        
        return response
        
    except Exception as e:
        logger.error(f"خطا در پیش‌بینی: {e}")
        raise HTTPException(status_code=500, detail=f"خطا در پیش‌بینی: {str(e)}")

@router.get("/sample")
async def get_sample_prediction():
    """دریافت یک پیش‌بینی نمونه"""
    
    sample_request = PredictionRequest(
        area=85,
        rooms=2,
        year_built=1400,
        city="تهران",
        district="الهیه", 
        property_type="apartment",
        condition="new"
    )
    
    return await predict_price(sample_request)

@router.get("/features")
async def get_model_features():
    """دریافت ویژگی‌های مورد استفاده مدل"""
    
    features_info = {
        "numerical_features": price_predictor.numerical_features,
        "categorical_features": price_predictor.categorical_features,
        "target_feature": price_predictor.target_feature,
        "is_trained": price_predictor.is_trained
    }
    
    return features_info