FROM python:3.14-alpine
WORKDIR /var/
RUN pip install --no-cache-dir bottle
ADD static/* /var/static/
ADD main.py /var/
EXPOSE 8080
CMD ["python3", "/var/main.py"]