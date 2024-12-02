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

# type: ignore
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet  

class ActionSetUserType(Action):
    def name(self):
        return "action_set_user_type"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "").lower()

        # Determine user type based on message content
        if "owner" in user_message:
            return [SlotSet("type_user", "owner")]
        elif "rent" in user_message or "tenant" in user_message or "lease" in user_message:
            return [SlotSet("type_user", "tenant")]
        else:
            dispatcher.utter_message(text="I couldn't identify your role. Are you an owner or a tenant?")
            return []


class ActionAcknowledgeUser(Action):
    def name(self) -> Text:
        return "action_acknowledge_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_type = tracker.get_slot("type_user")
        
        if user_type == "owner":
            dispatcher.utter_message(text="Thank you! You are identified as an owner.")
        elif user_type == "tenant":
            dispatcher.utter_message(text="Thank you! You are identified as a tenant.")
        else:
            dispatcher.utter_message(text="I'm not sure of your role. Could you clarify?")
        
        return []
