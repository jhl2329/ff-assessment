FROM python:3
WORKDIR /code
ENV FLASK_APP=api/api.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .

CMD ["python", "./main.py"]