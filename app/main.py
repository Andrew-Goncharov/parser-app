from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .total_parse import get_parsed_data


from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from database import actions

from .form import LoginForm
from .helpers import get_urls, map_img_url, calculate_interval, calculate_pagination

import starlette.status as status
import uvicorn
import os
import sys

sys.path.append("..")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")

LOGGED_IN = False

database_path = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database/main_database.db"

engine = create_engine(database_path,
                       connect_args={"check_same_thread": False})


def test_uuids_uniqueness() -> None:
    all_values = []
    connection = engine.connect()
    list_data = actions.get_all(connection)

    for row in list_data:
        all_values.append(row["id_uuid"])

    unique_values = set(all_values)

    print("Total: ", len(all_values))
    print("Unique: ", len(unique_values))

    assert len(all_values) == len(unique_values)


def get_connection() -> Connection:
    with engine.connect() as connection:
        with connection.begin():
            yield connection


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    global LOGGED_IN

    LOGGED_IN = False

    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=JSONResponse)
async def login(request: Request, connection: Connection = Depends(get_connection)):
    global LOGGED_IN

    form = LoginForm(request)

    form_data = await form.load_data()
    is_valid = await form.is_valid()

    if not is_valid:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Validation failed"})

    user_data = actions.get_user(form_data["username"], connection)

    if not user_data or form_data["password"] != user_data[0]["password"]:
        return templates.TemplateResponse("login.html",
                                          {"request": request, "message": "Incorrect username or password"})

    LOGGED_IN = True

    return RedirectResponse(app.url_path_for(name="main"), status_code=status.HTTP_302_FOUND)


@app.get("/parse_data")
async def parse(request: Request, count_pages: int = 5, connection: Connection = Depends(get_connection)):
    parsed_images = get_parsed_data(count_pages=count_pages)
    processed_images = map_img_url(parsed_images)

    if processed_images:
        actions.insert(processed_images, connection)

    return RedirectResponse(app.url_path_for(name="main"), status_code=status.HTTP_302_FOUND)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request, id: int = 1, connection: Connection = Depends(get_connection)):
    global LOGGED_IN

    if not LOGGED_IN:
        return RedirectResponse(app.url_path_for(name="login"))

    total_number = actions.get_info(connection)

    max_id = total_number // 12 if total_number % 12 == 0 else (total_number // 12) + 1

    start_id, end_id = calculate_interval(id, max_id)
    all_data = actions.get_many(start_id, end_id, connection)
    images = get_urls(all_data=all_data)
    pagination_list = calculate_pagination(id, max_id)

    print(f"Start id: {start_id}; End id: {end_id}")
    print(f"Number: {len(images)}")
    print(f"Final images: {images}")

    return templates.TemplateResponse("index.html", {"request": request,
                                                     "images": images,
                                                     "id": id,
                                                     "max_id": max_id,
                                                     "pagination_list": pagination_list,
                                                     "logged_in": True})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)

