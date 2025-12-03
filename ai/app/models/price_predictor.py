# -*- coding: utf-8 -*-
"""مدل پیش‌بینی قیمت املاک"""

import pandas as pd
import numpy as np
import joblib
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import os

logger = logging.getLogger(__name__)

class PricePredictor:
    """کلاس اصلی پیش‌بینی قیمت املاک"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        self.model_path = "app/models/price_predictor.pkl"
        
        # ویژگی‌های مدل
        self.numerical_features = ['area', 'rooms', 'year_built', 'age']
        self.categorical_features = ['city', 'district', 'property_type', 'condition']
        self.target_feature = 'price'
    
    def prepare_features(self, df):
        """آماده‌سازی ویژگی‌ها برای آموزش مدل"""
        
        # کپی داده‌ها
        data = df.copy()
        
        # محاسبه عمر ملک
        current_year = pd.Timestamp.now().year
        data['age'] = current_year - data['year_built']
        data['age'] = data['age'].clip(lower=0, upper=100)  # محدود کردن عمر
        
        # محاسبه قیمت هر متر
        data['price_per_m2'] = data['price'] / data['area']
        
        # حذف داده‌های پرت
        data = self._remove_outliers(data)
        
        return data
    
    def _remove_outliers(self, df):
        """حذف داده‌های پرت"""
        
        # محدودیت‌های منطقی
        df = df[
            (df['area'] >= 10) & (df['area'] <= 1000) &  # متراژ معقول
            (df['price'] >= 1000000) & (df['price'] <= 100000000000) &  # قیمت معقول
            (df['rooms'] >= 0) & (df['rooms'] <= 10) &  # تعداد اتاق معقول
            (df['age'] >= 0) & (df['age'] <= 100)  # عمر معقول
        ]
        
        # حذف بر اساس قیمت هر متر
        Q1 = df['price_per_m2'].quantile(0.05)
        Q3 = df['price_per_m2'].quantile(0.95)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df = df[
            (df['price_per_m2'] >= lower_bound) & 
            (df['price_per_m2'] <= upper_bound)
        ]
        
        return df
    
    def encode_categorical_features(self, df, training=True):
        """کدگذاری ویژگی‌های دسته‌ای"""
        
        encoded_df = df.copy()
        
        for feature in self.categorical_features:
            if feature not in df.columns:
                continue
                
            if training:
                # ایجاد encoder جدید
                self.label_encoders[feature] = LabelEncoder()
                encoded_df[feature] = self.label_encoders[feature].fit_transform(df[feature])
            else:
                # استفاده از encoder موجود
                if feature in self.label_encoders:
                    # مدیریت مقادیر جدید
                    known_categories = set(self.label_encoders[feature].classes_)
                    current_categories = set(df[feature].unique())
                    
                    # اختصاص کد -1 به مقادیر جدید
                    encoded_df[feature] = df[feature].apply(
                        lambda x: self.label_encoders[feature].transform([x])[0] 
                        if x in known_categories else -1
                    )
                else:
                    encoded_df[feature] = -1
        
        return encoded_df
    
    def train(self, data):
        """آموزش مدل"""
        
        try:
            logger.info("شروع آموزش مدل...")
            
            # آماده‌سازی داده‌ها
            prepared_data = self.prepare_features(data)
            
            if len(prepared_data) < 10:
                logger.warning("داده‌های کافی برای آموزش موجود نیست")
                return False
            
            # کدگذاری ویژگی‌های دسته‌ای
            encoded_data = self.encode_categorical_features(prepared_data, training=True)
            
            # تعریف ویژگی‌ها و هدف
            features = self.numerical_features + self.categorical_features
            X = encoded_data[features]
            y = encoded_data[self.target_feature]
            
            # تقسیم داده
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # نرمال‌سازی ویژگی‌های عددی
            X_train[self.numerical_features] = self.scaler.fit_transform(X_train[self.numerical_features])
            X_test[self.numerical_features] = self.scaler.transform(X_test[self.numerical_features])
            
            # ایجاد و آموزش مدل
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_train, y_train)
            
            # ارزیابی مدل
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
            
            y_pred = self.model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            logger.info(f"مدل آموزش داده شد - Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")
            logger.info(f"MAE: {mae:,.0f}, R²: {r2:.3f}")
            
            self.is_trained = True
            
            # ذخیره مدل
            self.save_model()
            
            return True
            
        except Exception as e:
            logger.error(f"خطا در آموزش مدل: {e}")
            return False
    
    def predict(self, input_data):
        """پیش‌بینی قیمت برای داده جدید"""
        
        if not self.is_trained or self.model is None:
            logger.error("مدل آموزش ندیده است")
            return None
        
        try:
            # تبدیل به DataFrame
            if isinstance(input_data, dict):
                df = pd.DataFrame([input_data])
            else:
                df = input_data.copy()
            
            # آماده‌سازی ویژگی‌ها
            prepared_data = self.prepare_features(df)
            encoded_data = self.encode_categorical_features(prepared_data, training=False)
            
            # اطمینان از وجود تمام ویژگی‌ها
            for feature in self.numerical_features + self.categorical_features:
                if feature not in encoded_data.columns:
                    encoded_data[feature] = 0
            
            # نرمال‌سازی
            encoded_data[self.numerical_features] = self.scaler.transform(encoded_data[self.numerical_features])
            
            # پیش‌بینی
            features = self.numerical_features + self.categorical_features
            X = encoded_data[features]
            
            prediction = self.model.predict(X)
            
            return float(prediction[0]) if len(prediction) == 1 else prediction.tolist()
            
        except Exception as e:
            logger.error(f"خطا در پیش‌بینی: {e}")
            return None
    
    def save_model(self):
        """ذخیره مدل آموزش دیده"""
        try:
            # ایجاد پوشه اگر وجود ندارد
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            # ذخیره مدل و preprocessors
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'label_encoders': self.label_encoders,
                'is_trained': self.is_trained
            }
            
            joblib.dump(model_data, self.model_path)
            logger.info(f"مدل در {self.model_path} ذخیره شد")
            
        except Exception as e:
            logger.error(f"خطا در ذخیره مدل: {e}")
    
    def load_model(self):
        """بارگذاری مدل آموزش دیده"""
        try:
            if os.path.exists(self.model_path):
                model_data = joblib.load(self.model_path)
                
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.label_encoders = model_data['label_encoders']
                self.is_trained = model_data['is_trained']
                
                logger.info("مدل با موفقیت بارگذاری شد")
                return True
            else:
                logger.warning("فایل مدل یافت نشد")
                return False
                
        except Exception as e:
            logger.error(f"خطا در بارگذاری مدل: {e}")
            return False

# نمونه global از مدل
price_predictor = PricePredictor()