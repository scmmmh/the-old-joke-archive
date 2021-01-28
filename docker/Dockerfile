FROM python:3.8

ARG SQLALCHEMY_URL=
ARG ELASTICSEARCH_HOSTS=
ARG BROKER_URL=
ARG SESSION_SECRET=
ARG EMAIL_SMTP_HOST=
ARG EMAIL_SMTP_SSL=
ARG EMAIL_SMTP_USERNAME=
ARG EMAIL_SMTP_PASSWORD=
ARG EMAIL_SENDER=

# Install base dependencies
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y tini libtesseract-dev libleptonica-dev tesseract-ocr

# Copy the application and configuration file
COPY toja-0.1.0-py3-none-any.whl /tmp/
COPY production.ini /etc/toja/production.ini
RUN sed -i -e "s#SQLALCHEMY_URL#${SQLALCHEMY_URL}#g" \
           -e "s#SESSION_SECRET#${SESSION_SECRET}#g" \
           -e "s#ELASTICSEARCH_HOSTS#${ELASTICSEARCH_HOSTS}#g" \
           -e "s#BROKER_URL#${BROKER_URL}#g" \
           -e "s#EMAIL_SMTP_HOST#${EMAIL_SMTP_HOST}#g" \
           -e "s#EMAIL_SMTP_SSL#${EMAIL_SMTP_SSL}#g" \
           -e "s#EMAIL_SMTP_USERNAME#${EMAIL_SMTP_USERNAME}#g" \
           -e "s#EMAIL_SMTP_PASSWORD#${EMAIL_SMTP_PASSWORD}#g" \
           -e "s#EMAIL_SENDER#${EMAIL_SENDER}#g" /etc/toja/production.ini

# Install the application
RUN python -m pip install /tmp/toja-0.1.0-py3-none-any.whl[postgresql]
COPY start_toja.sh /usr/bin/
RUN chmod a+x /usr/bin/start_toja.sh && \
    mkdir /var/lib/toja && \
    chmod 0666 /var/lib/toja

# Setup the running environment
VOLUME [ "/var/lib/toja" ]
ENV LC_ALL=C
WORKDIR /var/lib/toja
EXPOSE 8080
ENTRYPOINT [ "tini", "--" ]
CMD [ "/usr/bin/start_toja.sh" ]
