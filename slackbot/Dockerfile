FROM python:3

WORKDIR /usr/src/app

RUN pip install flask
RUN pip install requests
RUN pip install slackclient
RUN pip install slackeventsapi
RUN pip install twilio

COPY . .

CMD [ "python", "./main.py" ]