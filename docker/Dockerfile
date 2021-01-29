FROM python:3.8

ARG TOJA_USER="toja"
ARG TOJA_UID="10000"
ARG TOJA_GID="10000"

# Create the user
RUN groupadd --gid $TOJA_GID $TOJA_USER && \
    useradd --gid $TOJA_GID --no-log-init --shell /bin/bash --uid $TOJA_UID $TOJA_USER

# Install base dependencies
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y tini libtesseract-dev libleptonica-dev tesseract-ocr

# Copy the application and configuration file
COPY toja-0.1.2-py3-none-any.whl /tmp/
COPY production.ini /etc/toja/production.ini

# Install the application
RUN python -m pip install /tmp/toja-0.1.2-py3-none-any.whl[postgresql]
COPY start_toja.sh /usr/bin/
RUN chmod a+x /usr/bin/start_toja.sh && \
    mkdir /var/lib/toja && \
    chmod 0755 /var/lib/toja && \
    chown -R ${TOJA_USER}:${TOJA_USER} /etc/toja && \
    chown -R ${TOJA_USER}:${TOJA_USER} /var/lib/toja

# Setup the running environment
USER ${TOJA_UID}:${TOJA_GID}
VOLUME [ "/var/lib/toja" ]
ENV LC_ALL=C
WORKDIR /var/lib/toja
EXPOSE 8080
ENTRYPOINT [ "tini", "--" ]
CMD [ "/usr/bin/start_toja.sh" ]
