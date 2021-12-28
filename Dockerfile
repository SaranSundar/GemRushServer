FROM python:3.9-slim
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
# CMD ["python", "app.py"]
CMD ["gunicorn", "-w","3", "-b", "0.0.0.0:9378", "--log-level", "debug", "app", "app"]