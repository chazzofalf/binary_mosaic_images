FROM debian:sid
COPY venv-setup.sh /etc/venv-setup.sh
COPY docker-start.sh /etc/docker-start.sh
COPY binary_mosaic_images /src/binary_mosaic_images
COPY setup.py /src/setup.py
COPY pydo.py /etc/pydo.py
RUN chmod +x /etc/venv-setup.sh
RUN /etc/venv-setup.sh
VOLUME /input
VOLUME /output
ENTRYPOINT /etc/docker-start.sh


