ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

RUN mkdir /webserver

WORKDIR /webserver

COPY . /webserver

# Install python 3
RUN apk add --no-cache python3 && \
	python3 -m ensurepip && \
	pip3 install --no-cache --upgrade pip setuptools wheel && \
	pip3 install -r requirements.txt

CMD [ "/run.sh" ]