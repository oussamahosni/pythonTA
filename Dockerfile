FROM python:3.9
# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Updating apt to see and install Google Chrome
RUN apt-get -y update
# Magic happens
RUN apt-get install -y google-chrome-stable
# Installing Unzip
RUN apt-get install -yqq unzip

# Install necessary dependencies
WORKDIR /project
COPY ./requirements.txt /project/requirements.txt 
RUN pip install -r /project/requirements.txt

COPY ./app /project/app

CMD [ "uvicorn", "app.main:app","--reload" ,"--host", "0.0.0.0", "--port", "8000" ]

