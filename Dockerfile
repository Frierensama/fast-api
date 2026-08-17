FROM python:3.12.10-alpine@sha256:4bbf5ef9ce4b273299d394de268ad6018e10a9375d7efc7c2ce9501a6e

WORKDIR /rudeusfamily

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "uvicorn","basic:app","--host","0.0.0.0","--port","8000" ]