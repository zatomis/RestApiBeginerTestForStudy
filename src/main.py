import logging

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn

import sys
from pathlib import Path

# это для того, чтобы питон верно нашел и запустил основной файл !!!
# добавить эту папку в пути-чтобы интерпритатор работал
sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.DEBUG)

from src.api.tables import router as router_tables
from src.api.reservations import router as router_reservations


app = FastAPI(docs_url=None)
app.include_router(router_tables)
app.include_router(router_reservations)


@app.get("/")
def func():
    return "Hello World!!!!!!!!!!"


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    #это для запуска только локально
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    #это для запуска в докер
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
