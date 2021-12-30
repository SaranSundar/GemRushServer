FROM python:3.9-slim
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
# CMD ["python", "app.py"]
CMD ["gunicorn", "--log-level", "debug", "app"]