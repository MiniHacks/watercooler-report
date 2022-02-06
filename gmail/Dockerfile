FROM python:3

WORKDIR /usr/src/app

RUN pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
RUN pip install beautifulsoup4
RUN pip install requests
RUN pip install twilio
RUN pip install lxml

COPY . .

CMD [ "python", "./Retriever.py" ]