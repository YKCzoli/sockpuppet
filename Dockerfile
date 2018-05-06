FROM python

RUN apt-get update -y && apt-get -y upgrade

ADD ./requirements.txt /requirements.txt
WORKDIR /
RUN pip install --upgrade -r requirements.txt
RUN rm requirements.txt

RUN mkdir app
ADD . /app
WORKDIR /app

CMD [ "python", "tpl_puppet.py" ]