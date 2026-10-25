# StroyFix — калькулятор сметы ремонта в Ташкенте

Бесплатный MVP для расчёта ориентировочного количества и стоимости базовых
стройматериалов по ценам рынков Джами и Куйлюк. Приложение не требует
регистрации и не сохраняет пользовательские запросы.

## Структура

```text
backend/
  app/
    api/routes.py          # GET /api/materials и POST /api/calculate
    core/calculator.py     # Формулы расхода материалов
    db.py                  # SQLite, схема и начальные цены
    main.py                # FastAPI, CORS и подключение API
  requirements.txt
frontend/
  src/app/                 # Next.js App Router, страница и стили
  src/components/          # Карточка результата
  src/lib/api.ts           # Типизированный клиент backend API
```

## Запуск backend

Требуется Python 3.10 или новее.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

На Windows активируйте окружение командой `.venv\Scripts\activate`. При первом
запуске база `backend/stroyfix.db` инициализируется автоматически. API и
интерактивная документация будут доступны на `http://localhost:8000` и
`http://localhost:8000/docs`.

## Запуск frontend

В другом терминале:

```bash
cd frontend
npm install
npm run dev
```

Откройте `http://localhost:3000`. По умолчанию frontend обращается к backend на
`http://localhost:8000`. Для другого адреса задайте
`NEXT_PUBLIC_API_URL`, а разрешённые frontend origins задаются переменной
`STROYFIX_CORS_ORIGINS` в backend (список через запятую).

## API

`POST /api/calculate` принимает JSON:

```json
{
  "area_sqm": 60,
  "repair_type": "Косметический"
}
```

Поддерживаемые типы ремонта: `Косметический` и `Капитальный`. Ответ содержит
общую стоимость по средней цене двух рынков, итог для каждого рынка и
детализацию количества и стоимости по материалам. `GET /api/materials`
возвращает текущий каталог и цены. Начальные значения в базе — демонстрационные
средние цены в сумах; перед публичным запуском замените их на актуальные.

Расход зависит от типа ремонта и задаётся в `backend/app/core/calculator.py`.
Для MVP это ориентировочная оценка, а не коммерческое предложение или точная
ведомость материалов.
