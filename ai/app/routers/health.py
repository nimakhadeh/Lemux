# -*- coding: utf-8 -*-
"""روتر بررسی سلامت سرویس"""

from fastapi import APIRouter, HTTPException
from ...app.db import get_db
from ...app.models.price_predictor import price_predictor
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def health_check():
    """بررسی سلامت کلی سرویس"""
    
    health_status = {
        "status": "healthy",
        "service": "PropAnalyzer AI API",
        "version": "1.0.0"
    }
    
    # بررسی اتصال به دیتابیس
    try:
        db = get_db()
        if db.connect():
            health_status["database"] = "connected"
            db.disconnect()
        else:
            health_status["database"] = "disconnected"
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["database"] = "error"
        health_status["status"] = "unhealthy"
        logger.error(f"خطا در اتصال به دیتابیس: {e}")
    
    # بررسی وضعیت مدل
    if price_predictor.is_trained:
        health_status["model"] = "trained"
    else:
        health_status["model"] = "not_trained"
        health_status["status"] = "degraded"
    
    return health_status

@router.get("/database")
async def database_health():
    """بررسی سلامت دیتابیس"""
    
    try:
        db = get_db()
        if db.connect():
            # تست کوئری ساده
            result = db.execute_query("SELECT 1 as test")
            db.disconnect()
            
            return {
                "status": "healthy",
                "message": "اتصال به دیتابیس موفقیت‌آمیز بود",
                "test_query": "passed"
            }
        else:
            raise HTTPException(status_code=503, detail="عدم اتصال به دیتابیس")
            
    except Exception as e:
        logger.error(f"خطا در بررسی سلامت دیتابیس: {e}")
        raise HTTPException(status_code=503, detail=f"خطا در دیتابیس: {str(e)}")

@router.get("/model")
async def model_health():
    """بررسی سلامت مدل ML"""
    
    model_status = {
        "is_trained": price_predictor.is_trained,
        "model_type": "RandomForestRegressor" if price_predictor.model else "None"
    }
    
    if price_predictor.is_trained:
        model_status["status"] = "healthy"
        model_status["message"] = "مدل آموزش دیده آماده استفاده است"
    else:
        model_status["status"] = "not_trained"
        model_status["message"] = "مدل نیاز به آموزش دارد"
    
    return model_status

@router.post("/train")
async def train_model():
    """آموزش مدل با داده‌های فعلی"""
    
    try:
        db = get_db()
        if not db.connect():
            raise HTTPException(status_code=503, detail="عدم اتصال به دیتابیس")
        
        # دریافت داده‌ها از دیتابیس
        listings_data = db.get_listings_data(limit=5000)
        
        if not listings_data:
            raise HTTPException(status_code=404, detail="داده‌ای برای آموزش یافت نشد")
        
        # تبدیل به لیست دیکت
        listings_list = [dict(item) for item in listings_data]
        
        # پردازش داده‌ها
        from ...app.utils.data_processor import data_processor
        df = data_processor.clean_listings_data(listings_list)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="داده‌های معتبر کافی نیست")
        
        # آموزش مدل
        success = price_predictor.train(df)
        
        db.disconnect()
        
        if success:
            return {
                "status": "success",
                "message": "مدل با موفقیت آموزش داده شد",
                "training_samples": len(df),
                "model_type": "RandomForestRegressor"
            }
        else:
            raise HTTPException(status_code=500, detail="خطا در آموزش مدل")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطا در آموزش مدل: {e}")
        raise HTTPException(status_code=500, detail=f"خطا در آموزش مدل: {str(e)}")