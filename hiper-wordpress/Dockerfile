FROM python:3.7
WORKDIR /hiper-wordpress

COPY requirements.txt  ./

ENV TZ=America/Sao_Paulo

RUN groupadd -r user_hiper_wp && useradd -r -s /bin/false -g user_hiper_wp user_hiper_wp && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    apt-get update  && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /hiper-wordpress

RUN chown -R user_hiper_wp:user_hiper_wp /hiper-wordpress

USER user_hiper_wp

EXPOSE 5000

CMD ["uwsgi", "--ini", "/hiper-wordpress/wsgi.ini"]
