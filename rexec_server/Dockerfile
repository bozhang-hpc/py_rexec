FROM python:3.13.1

WORKDIR /server

COPY rexec_server/rexec_server.py /server
COPY rexec /server/rexec

RUN pip install dill pyzmq dxspaces

ENV broker_addr=127.0.0.1
ENV broker_port=5560

CMD ["sh", "-c", "python rexec_server.py \
                  ${broker_addr} --broker_port ${broker_port}"]