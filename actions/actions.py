# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
import json
import requests
import sqlite3
import textwrap


from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    con = None

    def name(self) -> Text:
        con = sqlite3.connect("./reviews.db")
        self.cur = con.cursor()
        return "zir_action_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        number_results = 3
        data_dict = {
            "query": [
                {
                    "query": tracker.latest_message["text"],
                    "num_results": number_results,
                    "corpus_key": [
                        {
                            "customer_id": "1526022105",
                            "corpus_id": 40
                        }
                    ]
                }
            ]
        }
        header = {
            "customer-id": "1526022105",
            "x-api-key": "zqt_WvU_2atFHgqYxxT2sQswwIUgogI8K3QeWs0oqA"
        }
        payload = json.dumps(data_dict)
        response = requests.post(f"https://h.serving.zir-ai.io:443/v1/query",
                                 data=payload,
                                 verify=True,
                                 headers=header,
                                 timeout=10)
        parsed = json.loads(response.text)
        first_resp = parsed["responseSet"][0]["response"][0]
        last_resp = parsed["responseSet"][0]["response"][-1]
        textQuery = []
        print(last_resp["score"])
        print(first_resp["score"])
        if last_resp["score"] < 0.3 or first_resp["score"] < 0.3:
            textQuery.append("I'm sorry, I can't help you.")
        else:
            textQuery = print_responses(parsed["responseSet"][0], self.cur)
            # items = [d['text'] for d in parsed["responseSet"][0]["response"]]
            textQuery.insert(0, "\n" )
            textQuery.insert(0, "This is what i found in the reviews:" )
        textQuery = "\n".join(textQuery)
        dispatcher.utter_message(text=textQuery)
        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]


def print_responses(response_set, sqlite_cursor):
    """Print responses to the console."""
    textList = []
    for result in response_set["response"]:
        doc = response_set["document"][result["documentIndex"]]
        query = f"""
            SELECT title, date, hotel, review FROM reviews
                WHERE doc_id="{doc["id"]}"
        """
        for row in sqlite_cursor.execute(query):
            title, date, hotel, fulltext = row
            textList.append("**" + title + "**")
            if is_title(result):
                textList.append(f"{head(fulltext)}")
            else:
                t = result["text"]
                textList.append(f"{highlight(fulltext, t)}")
            textList.append("*" + f"{hotel_name(hotel)} reviewed on {date}" + "*")
            textList.append("\n")
            break
    return textList

def hotel_name(hotel):
    """Returns a human-readable name for a hotel."""
    if hotel == "sheraton_fisherman_s_wharf_hotel":
        return "Sheraton Fisherman's Wharf Hotel"
    if hotel == "the_westin_st_francis":
        return "The Westin St. Francis San Francisco on Union Square"
    if hotel == "best_western_tuscan_inn_fisherman_s_wharf_a_kimpton_hotel":
        return "Best Western Fishermans Wharf"
    return hotel


def highlight(fulltext, snippet):
    """Return a result snippet with context, suitable for terminal display."""
    if snippet in fulltext:
        start = fulltext.index(snippet)
        end = start + len(snippet)

        lines = textwrap.wrap(fulltext)
        start_line = 0
        end_line = len(lines)
        pos = 0

        # Figure out which lines to display, and insert ANSI
        # code to highlight the actual snippet.
        for x, line in enumerate(lines):
            next_pos = pos + len(line)

            color_start = pos <= start < next_pos
            color_end = pos <= end < next_pos

            if color_start and color_end:
                start_line = end_line = x
                ips = start - pos - x   # insertion point
                ipe = end - pos - x     # insertion point
                lines[x] = line[:ips] + "**" + line[ips:ipe] + \
                    "**" + line[ipe:]
            elif color_start:
                start_line = x
                ip = start - pos - x    # insertion point
                lines[x] = line[:ip] + "**" + line[ip:]
            elif color_end:
                end_line = x
                ip = end - pos - x    # insertion point
                lines[x] = line[:ip] + "**" + line[ip:]

            pos = next_pos

        # Widen the line selection to include a bit of context.
        if start_line > 0:
            start_line -= 1
        end_line += 2
        return prettify('\n'.join(lines[start_line:end_line]))
    return prettify(snippet)


def head(fulltext):
    """Returns the first three lines of the review."""
    lines = textwrap.wrap(fulltext)
    return prettify('\n'.join(lines[0:3]) + '...')


def is_title(result):
    """Returns true if the result is a title match."""
    for metadatum in result["metadata"]:
        if metadatum["name"] == "is_title":
            return metadatum["value"] == "true"
    return False


def prettify(text):
    """Clean up the text to make it more suitable for display."""
    return text.replace("&amp;", "&").replace("&quot;", "\"")
