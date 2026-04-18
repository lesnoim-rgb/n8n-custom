from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import time
import random
import json

app = FastAPI()

class ParseRequest(BaseModel):
    keywords: List[str]
    regions: List[str]
    max_results: int = 50

class TenderInfo(BaseModel):
    id: str
    name: str
    price: Optional[float]
    publish_date: str
    docs_links: List[str]
    region: str

# Заглушка — реальный парсинг zakupki.gov.ru будет здесь
# Пока что имитируем данные для теста
async def parse_zakupki(keywords: List[str], regions: List[str], max_results: int) -> List[Dict]:
    # Здесь будет реальный код парсинга с Playwright
    # Пока возвращаем тестовые данные
    await asyncio.sleep(2)  # Имитируем задержку
    
    test_tenders = []
    for i in range(min(max_results, 10)):
        test_tenders.append({
            "id": f"TEST-{i:05d}",
            "name": f"Тестовый тендер {i} по ключевым словам {', '.join(keywords)}",
            "price": random.uniform(100000, 10000000),
            "publish_date": "2026-04-18",
            "docs_links": [f"https://zakupki.gov.ru/epz/order/notice/download/{i}"],
            "region": regions[0] if regions else "Москва"
        })
    return test_tenders

@app.post("/parse", response_model=List[TenderInfo])
async def parse(request: ParseRequest):
    """Основной эндпоинт для парсинга тендеров"""
    try:
        tenders = await parse_zakupki(
            keywords=request.keywords,
            regions=request.regions,
            max_results=request.max_results
        )
        return tenders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
