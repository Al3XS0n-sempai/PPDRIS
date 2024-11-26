FROM alpine:latest

RUN apk add --no-cache openssh-client ansible git sshpass bash
COPY ./ansible /ansible

WORKDIR /ansible

ENV ANSIBLE_HOST_KEY_CHECKING=False

CMD [ "" ]
