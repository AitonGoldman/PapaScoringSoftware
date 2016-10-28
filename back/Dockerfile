FROM python
ENV DB_TYPE sqlite
ENV FLASK_SECRET_KEY poop
ADD . /td
RUN /td/get_pyenv.sh
WORKDIR /td
ENTRYPOINT utils/gunicorn.docker.cmd 