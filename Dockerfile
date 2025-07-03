FROM python:3.11
WORKDIR /web-app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/web-app
EXPOSE 5000
CMD ["python", "app/app.py"]