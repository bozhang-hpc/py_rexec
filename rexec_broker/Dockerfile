FROM python:3.13.1-slim

WORKDIR /broker

COPY rexec_broker/rexec_broker.py /broker

RUN pip install pyzmq

ENV client_port=5559
ENV server_port=5560
ENV control_port=5561

EXPOSE ${client_port} ${server_port} ${control_port}

CMD ["sh", "-c", "python rexec_broker.py                \
                  --client_port ${client_port}          \
                  --server_port ${server_port}          \
                  --control_port ${control_port}"]