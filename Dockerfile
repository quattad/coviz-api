# Setup OS
FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

# RUN echo sed -i 's/http\:\/\/dl-cdn.alpinelinux.org/https\:\/\/alpine.global.ssl.fastly.net/g' >> /etc/apk/repositories

RUN echo http://mirror.yandex.ru/mirrors/alpine/v3.8/main > /etc/apk/repositories; \
    echo http://mirror.yandex.ru/mirrors/alpine/v3.8/community >> /etc/apk/repositories

# Install bash and nano text editor
RUN apk --update add bash nano

# Install deps
RUN apk --update add mariadb-dev
RUN apk --update add --no-cache \ 
    lapack-dev \ 
    gcc \
    freetype-dev
RUN apk add --no-cache --virtual .build-deps \
    gfortran \
    musl-dev \
    g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip install setuptools
RUN pip install --upgrade pip setuptools wheel
RUN pip install cython
# RUN pip install scipy
# RUN pip install seaborn

# removing dependencies
RUN apk del .build-deps

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /var/www/requirements.txt

CMD python
