FROM python:3.6
ADD . /app
WORKDIR /app
RUN pip install -r PasswordFilter/requirements.txt
EXPOSE 8000
CMD ["gunicorn", "PasswordFilter.app:app"]
