# -*- coding: utf-8 -*-
"""پردازشگر داده برای آماده‌سازی داده‌های ML"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class DataProcessor:
    """کلاس پردازش داده‌های املاک"""
    
    def __init__(self):
        self.feature_config = {
            'numerical': ['area', 'rooms', 'year_built', 'age'],
            'categorical': ['city', 'district', 'property_type', 'condition'],
            'target': 'price'
        }
    
    def clean_listings_data(self, listings_data: List[Dict]) -> pd.DataFrame:
        """پاکسازی و آماده‌سازی داده‌های خام"""
        
        if not listings_data:
            logger.warning("داده‌ای برای پردازش دریافت نشد")
            return pd.DataFrame()
        
        try:
            # تبدیل به DataFrame
            df = pd.DataFrame(listings_data)
            
            # حذف رکوردهای با داده‌های ضروری missing
            df = df.dropna(subset=['price', 'area', 'city'])
            
            # تبدیل انواع داده
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df['area'] = pd.to_numeric(df['area'], errors='coerce')
            df['rooms'] = pd.to_numeric(df['rooms'], errors='coerce').fillna(1)
            df['year_built'] = pd.to_numeric(df['year_built'], errors='coerce')
            
            # محاسبه ویژگی‌های جدید
            df = self._create_features(df)
            
            # حذف داده‌های نامعتبر
            df = df[
                (df['price'] > 1000000) & 
                (df['area'] > 10) &
                (df['area'] < 1000) &
                (df['rooms'] >= 0) &
                (df['rooms'] <= 10)
            ]
            
            logger.info(f"داده‌ها پاکسازی شدند: {len(df)} رکورد معتبر")
            return df
            
        except Exception as e:
            logger.error(f"خطا در پاکسازی داده‌ها: {e}")
            return pd.DataFrame()
    
    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """ایجاد ویژگی‌های مهندسی شده"""
        
        df = df.copy()
        
        # محاسبه عمر ملک
        current_year = pd.Timestamp.now().year
        df['age'] = current_year - df['year_built']
        df['age'] = df['age'].clip(lower=0, upper=100)
        
        # قیمت هر متر مربع
        df['price_per_m2'] = df['price'] / df['area']
        
        # دسته‌بندی مناطق بر اساس شهر
        df['district'] = df['district'].fillna('نامشخص')
        df['neighborhood'] = df['neighborhood'].fillna('نامشخص')
        
        # نوع ملک
        df['property_type'] = df['property_type'].fillna('apartment')
        
        # وضعیت ملک
        df['condition'] = df['condition'].fillna('normal')
        
        return df
    
    def get_market_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """استخراج بینش‌های بازار از داده‌ها"""
        
        if df.empty:
            return {}
        
        insights = {}
        
        try:
            # آمار کلی
            insights['overall'] = {
                'total_listings': len(df),
                'avg_price': int(df['price'].mean()),
                'avg_price_per_m2': int(df['price_per_m2'].mean()),
                'avg_area': float(df['area'].mean()),
                'avg_rooms': float(df['rooms'].mean())
            }
            
            # آمار به تفکیک شهر
            city_stats = df.groupby('city').agg({
                'price': ['count', 'mean', 'median', 'std'],
                'price_per_m2': ['mean', 'median'],
                'area': 'mean',
                'rooms': 'mean'
            }).round(0)
            
            city_stats.columns = ['_'.join(col).strip() for col in city_stats.columns.values]
            city_stats = city_stats.reset_index()
            
            insights['by_city'] = city_stats.to_dict('records')
            
            # آمار به تفکیک نوع ملک
            type_stats = df.groupby('property_type').agg({
                'price': ['count', 'mean'],
                'price_per_m2': 'mean',
                'area': 'mean'
            }).round(0)
            
            type_stats.columns = ['_'.join(col).strip() for col in type_stats.columns.values]
            type_stats = type_stats.reset_index()
            
            insights['by_property_type'] = type_stats.to_dict('records')
            
            # روند قیمت بر اساس عمر
            age_bins = [0, 5, 10, 20, 30, 50, 100]
            age_labels = ['0-5', '6-10', '11-20', '21-30', '31-50', '50+']
            
            df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)
            age_stats = df.groupby('age_group')['price_per_m2'].mean().reset_index()
            
            insights['by_age'] = age_stats.to_dict('records')
            
            logger.info("بینش‌های بازار استخراج شدند")
            return insights
            
        except Exception as e:
            logger.error(f"خطا در استخراج بینش‌ها: {e}")
            return {}

# نمونه global
data_processor = DataProcessor()