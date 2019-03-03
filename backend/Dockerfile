FROM simiprambos/pychrome:latest

LABEL maintainer="simi.prambos@gmail.com"

ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

COPY . $APP_HOME/

RUN pip3 install -r requirements.txt

RUN python3 manage.py makemigrations numbers_app messages_app contacts_app users_auth media_app
RUN python3 manage.py migrate

CMD tail -f /dev/null