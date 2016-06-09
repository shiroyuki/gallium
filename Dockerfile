FROM python:3

ENV path /opt/gallium

ADD . ${path}
#RUN pip install -U pip
RUN pip install -q ${path}

WORKDIR ${path}

ENTRYPOINT ["gallium"]
