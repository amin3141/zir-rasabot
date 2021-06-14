<!--lint disable no-literal-urls-->
<p align="center">
  <a href="https://zir-ai.com/">
    <img
      alt="Zir AI"
      src="https://zir-ai.com/static/media/logo-light.637c616a.svg"
      width="400"
    />
  </a>
</p>

The source code in this repository shows a simple Rasa chatbot fallback
mechanism, which gets relevant information from ZIR Semantic Search.

# Table of contents

* [Rasa Bot & Zir](#rasa-bot--zir)
* [Setup & Play](#setup--play)
  + [Set-up Rasa](#set-up-rasa)
  + [Set-up repo](#set-up-repo)
  + [Running the demo](#running-the-demo)
* [Customizing the bot](#customizing-the-bot)
  + [Data](#data)
* [Rasa Custom Action](#rasa-custom-action)

## Rasa Bot & Zir

[Rasa](https://rasa.com/) is the leading conversational AI platform, for
personalized conversations at scale. Developers provide the questsions they
expect the end customer to ask and Rasa bot, using AI, predicts and matches the
what the customer intended to ask. With this information at hand, developers can
easily match what the bot should respond.

This is all well unless when the customer asks a valid question the developer
did not expect, for such a scenario Rasa provides a
[fallback mechanism](https://rasa.com/docs/rasa/fallback-handoff#fallbacks).

> Although Rasa will generalize to unseen messages, some messages might receive
> a low classification confidence. Using Fallbacks will help ensure that these
> low confidence messages are handled gracefully, giving your assistant the
> option to either respond with a default message or attempt to disambiguate the
> user input.

Using the mechanism the bot can ask fallback and search through the reviews
uploaded in [Zir-AI](https://zir-ai.com) with the help of
[custom actions](https://rasa.com/docs/rasa/custom-actions). If the reviews have
the relavent information, it is shown as a result otherwise if the confidence of
the question to review matching is low, we fallback to a generic statement.

The end results sums up to be this:

## Setup & Play

You'll need to have Rasa installed and this repository. You might want to create
a [virtual environment](#https://docs.python.org/3/library/venv.html) to isolate
the dependencies rasa requires.

### Set-up Rasa

Follow the
[rasa installation instrcutions](#https://rasa.com/docs/rasa/installation) or
copy paste the following commands in terminal

```bash
pip3 install -U pip
pip3 install rasa
rasa --version
```

This should print the rasa version similar to follow

```bash
Rasa Version      :         2.7.0
Minimum Compatible Version: 2.6.0
Rasa SDK Version  :         2.7.0
Rasa X Version    :         None
Python Version    :         3.8.5
Operating System  :         Linux
Python Path       :         /bin/python3
```

> Windows & WSL works too

### Set-up repo

To install dependecies for this repository to work install python dependencies
from requirements.txt

```bash
pip install -r requirements.txt
python3 -m spacy download en_core_web_md
```

This will install the spacy model `en_core_web_md` this bot is configured with.
Now you'll need to train the rasa bot

```bash
rasa train
```

### Running the demo

While running the model, you are require to run the rasa action server along
with the rasa bot. So in one terminal run

```bash
rasa run actions
```

In another terminal you can either play with the bot in your `shell` or on the
browser.

To talk to the bot in shell run

```bash
rasa shell
```

Or to talk to the bot in the browser run

```bash
rasa run --credentials ./credentials.yml  --enable-api --auth-token XYZ123 --model ./models --endpoints ./endpoints.yml --cors "*"
```

Now, open the `index.html` in your browser to talk to the bot.

## Customizing the bot

Use the following information to customize the bot and the source of data.

### Data

Data for the bot is sourced from [OpinRank](https://github.com/kavgan/OpinRank/)
and reviews for Hotel Jumeirah is specifically used for this bot. Reviews are
parsed from https://github.com/amin3141/zir-souffle. Use `hotels.py` to generate
the output `json` and the `reviews.db`.

Create a corpus on [Zir AI](http://zir-ai.com) and upload all the `json` files.
Create an api key for access and note down the following information

- Api key
- corpus id
- customer id

## Rasa Custom Action

Use the above collected information and replace the information in
`actions/actions.py` and you're good to go.

```python
customer_id = "1835841754"
corpus_id = 1
header = {
    "customer-id": customer_id,
    "x-api-key": "zqt_WvU_2atFHgqYxxT2sQswwIUgogI8K3QeWs0oqA"
}
```
