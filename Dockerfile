FROM python:3

ENV path /opt/gallium

RUN pip install -q imagination

ADD . ${path}
RUN pip install -q ${path}

WORKDIR ${path}

ENTRYPOINT ["gallium"]
