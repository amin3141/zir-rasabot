# Rasa-bot with ZIR-AI fallback

# Run:
#
#     docker container run --publish 5005:5005 --name zir-ai-rasa zir-ai:rasa
#
# Build:
#     docker build . -t zir-ai:rasa

FROM rasa/rasa:2.7.1-spacy-en

WORKDIR /opt/zir/hotel-bot
COPY . /opt/zir/hotel-bot

RUN rasa train

ENV RASA_REST_PORT=5005

EXPOSE $RASA_REST_PORT
ENTRYPOINT [ "/bin/sh", "start.sh"]
