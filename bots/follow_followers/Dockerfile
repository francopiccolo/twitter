FROM python:3.7-alpine

WORKDIR /bots
COPY ../config.py .
COPY follow_followers.py ./follow_followers
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD python -m follow_followers.follow_followers