FROM python:3.13.1-slim

WORKDIR /broker

COPY ./rexec_broker.py /broker

RUN pip install pyzmq

EXPOSE 5559 5560 5561

CMD ["python", "rexec_broker.py"]