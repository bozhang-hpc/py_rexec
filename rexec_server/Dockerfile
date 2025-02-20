FROM python:3.13.1-slim

WORKDIR /server

COPY ./rexec_server.py /server

RUN pip install dill pyzmq

EXPOSE 5560

CMD ["python", "rexec_server.py"]