FROM python:latest


COPY . .



RUN pip install --no-cache-dir --upgrade -r /requirements.txt



CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
#CMD ["fastapi", "run", "main.py", "--port", "80"]