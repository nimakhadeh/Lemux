# -*- coding: utf-8 -*-
"""روتر تحلیل بازار"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

from ...app.db import get_db
from ...app.utils.data_processor import data_processor

router = APIRouter()
logger = logging.getLogger(__name__)

class MarketAnalysisResponse(BaseModel):
    """مدل پاسخ تحلیل بازار"""
    
    overall_stats: Dict[str, Any]
    city_analysis: List[Dict[str, Any]]
    property_type_analysis: List[Dict[str, Any]]
    price_trends: Dict[str, Any]
    recommendations: List[str]

@router.get("/", response_model=MarketAnalysisResponse)
async def analyze_market(limit: int = 1000):
    """تحلیل کلی بازار املاک"""
    
    try:
        db = get_db()
        if not db.connect():
            raise HTTPException(status_code=503, detail="عدم اتصال به دیتابیس")
        
        # دریافت داده‌ها
        listings_data = db.get_listings_data(limit=limit)
        db.disconnect()
        
        if not listings_data:
            raise HTTPException(status_code=404, detail="داده‌ای برای تحلیل یافت نشد")
        
        # پردازش داده‌ها
        listings_list = [dict(item) for item in listings_data]
        df = data_processor.clean_listings_data(listings_list)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="داده‌های معتبر کافی نیست")
        
        # استخراج بینش‌ها
        insights = data_processor.get_market_insights(df)
        
        # تولید توصیه‌ها
        recommendations = generate_recommendations(insights)
        
        # تحلیل روند قیمت
        price_trends = analyze_price_trends(df)
        
        response = MarketAnalysisResponse(
            overall_stats=insights.get('overall', {}),
            city_analysis=insights.get('by_city', []),
            property_type_analysis=insights.get('by_property_type', []),
            price_trends=price_trends,
            recommendations=recommendations
        )
        
        logger.info("تحلیل بازار با موفقیت انجام شد")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطا در تحلیل بازار: {e}")
        raise HTTPException(status_code=500, detail=f"خطا در تحلیل بازار: {str(e)}")

@router.get("/city/{city_name}")
async def analyze_city(city_name: str):
    """تحلیل بازار برای یک شهر خاص"""
    
    try:
        db = get_db()
        if not db.connect():
            raise HTTPException(status_code=503, detail="عدم اتصال به دیتابیس")
        
        # دریافت داده‌های شهر خاص
        query = """
        SELECT id, title, price, area, rooms, year_built,
               city, district, property_type, condition
        FROM backend_propanalyzer_api_listing 
        WHERE city = %s AND price > 0 AND area > 0 AND is_active = true
        ORDER BY created_at DESC 
        LIMIT 1000
        """
        
        results = db.execute_query(query, (city_name,))
        db.disconnect()
        
        if not results:
            raise HTTPException(status_code=404, detail=f"داده‌ای برای شهر {city_name} یافت نشد")
        
        # پردازش داده‌ها
        listings_list = [dict(item) for item in results]
        df = data_processor.clean_listings_data(listings_list)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="داده‌های معتبر کافی نیست")
        
        insights = data_processor.get_market_insights(df)
        
        return {
            "city": city_name,
            "analysis": insights,
            "sample_size": len(df)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطا در تحلیل شهر: {e}")
        raise HTTPException(status_code=500, detail=f"خطا در تحلیل شهر: {str(e)}")

def generate_recommendations(insights: Dict[str, Any]) -> List[str]:
    """تولید توصیه‌های سرمایه‌گذاری"""
    
    recommendations = []
    
    try:
        overall = insights.get('overall', {})
        by_city = insights.get('by_city', [])
        
        if not overall or not by_city:
            return ["داده‌های کافی برای تولید توصیه موجود نیست"]
        
        # تحلیل شهرها
        city_prices = {item['city']: item['price_per_m2_mean'] for item in by_city}
        
        if city_prices:
            expensive_city = max(city_prices, key=city_prices.get)
            affordable_city = min(city_prices, key=city_prices.get)
            
            recommendations.append(f"بالاترین قیمت هر متر در {expensive_city} است")
            recommendations.append(f"مناسب‌ترین قیمت هر متر در {affordable_city} مشاهده می‌شود")
        
        # تحلیل کلی
        avg_price_m2 = overall.get('avg_price_per_m2', 0)
        
        if avg_price_m2 > 100000000:  # 100 میلیون
            recommendations.append("بازار در وضعیت گرانی قرار دارد - احتیاط در سرمایه‌گذاری")
        elif avg_price_m2 < 50000000:  # 50 میلیون
            recommendations.append("بازار در وضعیت مناسب برای خرید قرار دارد")
        else:
            recommendations.append("بازار در وضعیت متعادل قرار دارد")
        
        # توصیه بر اساس تعداد آگهی‌ها
        total_listings = overall.get('total_listings', 0)
        
        if total_listings < 100:
            recommendations.append("حجم داده‌های بازار کم است - تحلیل با احتیاط")
        elif total_listings > 1000:
            recommendations.append("حجم داده‌های بازار مناسب است - تحلیل قابل اعتماد")
        
    except Exception as e:
        logger.error(f"خطا در تولید توصیه‌ها: {e}")
        recommendations = ["خطا در تولید توصیه‌های تحلیل"]
    
    return recommendations

def analyze_price_trends(df):
    """تحلیل روند قیمت‌ها"""
    
    try:
        # تحلیل ساده - می‌تواند با داده‌های زمانی پیچیده‌تر شود
        trends = {
            "avg_price_per_m2": int(df['price_per_m2'].mean()),
            "price_range_per_m2": {
                "min": int(df['price_per_m2'].min()),
                "max": int(df['price_per_m2'].max())
            },
            "price_distribution": {
                "under_50M": len(df[df['price_per_m2'] < 50000000]),
                "50M_100M": len(df[(df['price_per_m2'] >= 50000000) & (df['price_per_m2'] < 100000000)]),
                "over_100M": len(df[df['price_per_m2'] >= 100000000])
            }
        }
        
        return trends
        
    except Exception as e:
        logger.error(f"خطا در تحلیل روند قیمت: {e}")
        return {}