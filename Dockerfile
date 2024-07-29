FROM python:3.12.4-alpine

WORKDIR /code

COPY requirements.txt .

# RUN apk add --no-cache gcc musl-dev linux-headers sqlite ffmpeg
RUN apk add --no-cache postgresql-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]