FROM rasa/rasa:2.7.1-spacy-en AS trained

WORKDIR /hotel-bot
COPY . /hotel-bot

RUN rasa train

FROM rasa/rasa:2.7.1-spacy-en

WORKDIR /hotel-bot
COPY --from=trained /hotel-bot .

ENV RASA_REST_PORT=5005

EXPOSE $RASA_REST_PORT
ENTRYPOINT [ "/bin/sh", "start.sh"]