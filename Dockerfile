FROM python:3.6
ADD . /app
WORKDIR /app
RUN pip install -r passwordfilter/requirements.txt
EXPOSE 8000
WORKDIR /app/passwordfilter
CMD ["gunicorn", "wsgi", "--bind", "0.0.0.0:8000"]
