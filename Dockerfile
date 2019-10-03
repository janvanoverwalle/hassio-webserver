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
RUN apk add --no-cache python3

# Install any dependencies
#RUN pip3 install -r requirements.txt

CMD [ "/run.sh" ]