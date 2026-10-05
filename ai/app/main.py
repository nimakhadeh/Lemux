# -*- coding: utf-8 -*-
"""فایل اصلی FastAPI"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import predict, analyze, undervalued, health

app = FastAPI(
    title="PropAnalyzer AI API",
    description="API هوش مصنوعی برای تحلیل و پیش‌بینی قیمت املاک",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

allowed_origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(health.router, prefix="/health", tags=["سلامت"])
app.include_router(predict.router, prefix="/predict", tags=["پیش‌بینی"])
app.include_router(analyze.router, prefix="/analyze", tags=["تحلیل"])
app.include_router(undervalued.router, prefix="/undervalued", tags=["سرمایه‌گذاری"])

@app.get("/")
async def root():
    return {
        "message": "خوش آمدید به PropAnalyzer AI API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "predict": "/predict",
            "analyze": "/analyze",
            "undervalued": "/undervalued",
        },
    }

@app.get("/info")
async def api_info():
    return {
        "name": "PropAnalyzer AI",
        "description": "سیستم هوش مصنوعی تحلیل بازار مسکن ایران",
        "version": "1.0.0",
        "author": "PropAnalyzer Team",
        "features": [
            "پیش‌بینی قیمت املاک",
            "تحلیل روند بازار",
            "شناسایی املاک زیر قیمت",
            "تحلیل منطقه‌ای",
        ],
    }
