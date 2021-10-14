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

import requests
from typing import Text, Dict, Any, List
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk import Action
from rasa_sdk.events import SlotSet


class ActionSetAskedAboutWeather(Action):
    def name(self) -> Text:
        return "action_set_asked_about_weather"

    def run(self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("asked_about_weather", True)]


class ActionCheckWeather(Action):
    def name(self) -> Text:
        return "action_check_weather"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city_name = tracker.get_slot('city')
        api_key = "e2a7eb8fb47f6546ba6b8d79c8e4d9cd"
        if city_name is None or city_name == []:
            return
        else:
            api_call = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=imperial"
            response = requests.get(api_call)
            response_json = response.json()
            description = response_json["weather"][0]["description"]
            temp = response_json["main"]["temp"]
            temp_min = response_json["main"]["temp_min"]
            temp_max = response_json["main"]["temp_max"]
            humidity = response_json["main"]["humidity"]
            wind_speed = response_json["wind"]["speed"]

            return [SlotSet("weather", description if description is not None else []),
                    SlotSet("temp", temp if temp is not None else []),
                    SlotSet("temp_min", temp_min if temp_min is not None else []),
                    SlotSet("temp_max", temp_max if temp_max is not None else []),
                    SlotSet("humidity", humidity if humidity is not None else []),
                    SlotSet("wind_speed", wind_speed if wind_speed is not None else [])]
