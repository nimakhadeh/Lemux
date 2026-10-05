# -*- coding: utf-8 -*-
"""Identify potentially undervalued listings from market data."""

from fastapi import APIRouter, HTTPException, Query

from app.db import get_db

router = APIRouter()


@router.get("/")
async def undervalued_listings(
    city: str | None = Query(default=None, min_length=1, max_length=100),
    limit: int = Query(default=20, ge=1, le=100),
):
    """Return active listings priced below their city's average price per m²."""

    db = get_db()
    if not db.connect():
        raise HTTPException(status_code=503, detail="عدم اتصال به دیتابیس")

    try:
        query = """
            WITH city_market AS (
                SELECT
                    city,
                    AVG(price / NULLIF(area, 0)) AS avg_price_per_m2
                FROM backend_propanalyzer_api_listing
                WHERE is_active = true AND price > 0 AND area > 0
                GROUP BY city
            )
            SELECT
                l.id,
                l.title,
                l.city,
                l.district,
                l.price,
                l.area,
                ROUND((l.price / NULLIF(l.area, 0))::numeric, 0) AS price_per_m2,
                ROUND((
                    (1 - (l.price / NULLIF(l.area, 0)) /
                    NULLIF(cm.avg_price_per_m2, 0)) * 100
                )::numeric, 2) AS discount_percent
            FROM backend_propanalyzer_api_listing l
            JOIN city_market cm ON cm.city = l.city
            WHERE l.is_active = true
              AND l.price > 0
              AND l.area > 0
              AND l.price / NULLIF(l.area, 0) < cm.avg_price_per_m2
        """
        params = []

        if city:
            query += " AND l.city = %s"
            params.append(city.strip())

        query += " ORDER BY discount_percent DESC LIMIT %s"
        params.append(limit)

        rows = db.execute_query(query, params)
        return {
            "city": city,
            "count": len(rows),
            "listings": [dict(row) for row in rows],
        }
    finally:
        db.disconnect()
