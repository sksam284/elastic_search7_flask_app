FROM python:3.8-slim-buster

RUN useradd user

COPY requirements.txt /

RUN pip install -r /requirements.txt

WORKDIR /opt

COPY . /opt/

RUN chown -R user:user ./
USER user

EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]