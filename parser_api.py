from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import time
import random
import json
from playwright.async_api import async_playwright

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

async def parse_zakupki_real(keywords: List[str], regions: List[str], max_results: int) -> List[Dict]:
    """
    Реальный парсинг zakupki.gov.ru с использованием Playwright
    """
    results = []
    
    async with async_playwright() as p:
        # Запускаем браузер (без GUI, в режиме headless)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Формируем URL поиска
        search_url = "https://zakupki.gov.ru/epz/orderquicksearch/search/results.html"
        
        # Переходим на страницу поиска
        await page.goto(search_url)
        
        # Вводим ключевые слова
        await page.fill('input[name="searchString"]', ' '.join(keywords))
        
        # Выбираем регион (упрощённо)
        # В реальности нужно разбираться с селекторами zakupki.gov.ru
        
        # Нажимаем поиск
        await page.click('button[type="submit"]')
        
        # Ждём загрузки результатов
        await page.wait_for_selector('.registry-entry', timeout=30000)
        
        # Парсим результаты
        tenders = await page.query_selector_all('.registry-entry')
        
        for i, tender in enumerate(tenders[:max_results]):
            try:
                # Извлекаем номер закупки
                tender_id = await tender.query_selector('.purchase-number a')
                tender_id_text = await tender_id.inner_text() if tender_id else "N/A"
                
                # Извлекаем название
                name_elem = await tender.query_selector('.row .registry-entry__header-title')
                name_text = await name_elem.inner_text() if name_elem else "Без названия"
                
                # Извлекаем НМЦК (цену)
                price_elem = await tender.query_selector('.price-cell')
                price_text = await price_elem.inner_text() if price_elem else "0"
                
                # Извлекаем ссылки на документацию
                docs_links = []
                doc_links = await tender.query_selector_all('.attachment-link')
                for link in doc_links:
                    href = await link.get_attribute('href')
                    if href:
                        docs_links.append(f"https://zakupki.gov.ru{href}")
                
                results.append({
                    "id": tender_id_text.strip(),
                    "name": name_text.strip(),
                    "price": float(price_text.replace(' ', '').replace('₽', '').replace(',', '.')),
                    "publish_date": "2026-04-18",  # реальную дату нужно парсить отдельно
                    "docs_links": docs_links,
                    "region": regions[0] if regions else "Не указан"
                })
                
            except Exception as e:
                print(f"Ошибка парсинга тендера: {e}")
                continue
            
            # Задержка между тендерами
            await asyncio.sleep(random.uniform(1, 3))
        
        await browser.close()
    
    return results

@app.post("/parse", response_model=List[TenderInfo])
async def parse(request: ParseRequest):
    """Основной эндпоинт для парсинга тендеров"""
    try:
        # Используем реальный парсинг
        tenders = await parse_zakupki_real(
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
