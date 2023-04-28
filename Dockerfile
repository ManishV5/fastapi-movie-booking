FROM python:3.9-bullseye
ADD fastapi-movie-booking/ /fastapi-app
WORKDIR /fastapi-app
RUN pip install -r requirements.txt
RUN pytest
ENTRYPOINT uvicorn main:app
