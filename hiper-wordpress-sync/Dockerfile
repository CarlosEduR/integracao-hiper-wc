FROM python:3.7
WORKDIR /hiper-wordpress-sycn

COPY requirements.txt  ./

ENV TZ=America/Sao_Paulo

RUN groupadd -r user_hiper_wp && useradd -r -s /bin/false -g user_hiper_wp user_hiper_wp && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    apt-get update  && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /hiper-wordpress-sycn

RUN chown -R user_hiper_wp:user_hiper_wp /hiper-wordpress-sycn

USER user_hiper_wp

EXPOSE 5001

CMD ["uwsgi", "--ini", "/hiper-wordpress-sycn/wsgi.ini"]
