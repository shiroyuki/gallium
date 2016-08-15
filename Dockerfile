FROM python:3

ENV path /opt/gallium

RUN pip install -q https://github.com/shiroyuki/Imagination/releases/download/2.0.0a1/imagination-2.0.0a0.tar.gz

ADD . ${path}
RUN pip install -q ${path}

WORKDIR ${path}

ENTRYPOINT ["gallium"]
