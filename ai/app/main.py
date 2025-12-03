# -*- coding: utf-8 -*-
"""فایل اصلی FastAPI"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import predict, analyze, undervalued, health

# ایجاد برنامه FastAPI
app = FastAPI(
    title="PropAnalyzer AI API",
    description="API هوش مصنوعی برای تحلیل و پیش‌بینی قیمت املاک",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# افزودن middlewareهای CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در تولید محدود شود
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ثبت روترها
app.include_router(health.router, prefix="/health", tags=["سلامت"])
app.include_router(predict.router, prefix="/predict", tags=["پیش‌بینی"])
app.include_router(analyze.router, prefix="/analyze", tags=["تحلیل"])
app.include_router(undervalued.router, prefix="/undervalued", tags=["سرمایه‌گذاری"])

@app.get("/")
async def root():
    """صفحه اصلی API"""
    return {
        "message": "خوش آمدید به PropAnalyzer AI API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "predict": "/predict",
            "analyze": "/analyze", 
            "undervalued": "/undervalued"
        }
    }

@app.get("/info")
async def api_info():
    """اطلاعات API"""
    return {
        "name": "PropAnalyzer AI",
        "description": "سیستم هوش مصنوعی تحلیل بازار مسکن ایران",
        "version": "1.0.0",
        "author": "PropAnalyzer Team",
        "features": [
            "پیش‌بینی قیمت املاک",
            "تحلیل روند بازار",
            "شناسایی املاک زیر قیمت",
            "تحلیل منطقه‌ای"
        ]
    }