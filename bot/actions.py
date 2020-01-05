import os
import re
import datetime
import logging
import requests
import json
import urllib
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action, Tracker, ActionExecutionRejection
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ConversationPaused, AllSlotsReset


class ActionGreetMessage(Action):
    def name(self) -> Text:
        return "action_greet_by_time"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:
        current_time = datetime.datetime.now()
        message = ""
        if current_time.hour < 12:
            message = 'Good morning'
        elif 12 >= current_time.hour < 18:
            message = 'Good afternoon'
        else:
            message = 'Good evening'
        dispatcher.utter_message(message)
        return [AllSlotsReset()]


class ActionGreetUser(Action):
    def name(self) -> Text:
        return "greet_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:
        user_name = tracker.get_slot("person")
        if user_name != None and user_name != '' and user_name != "None":
            dispatcher.utter_message(
                template='utter_welcome_user', **tracker.slots)
        else:
            dispatcher.utter_message(
                template='utter_welcome_without_name', **tracker.slots)
        return []


class ActionDepartmentContact(Action):
    def name(self) -> Text:
        return "action_department_contact"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:
        department = tracker.get_slot("departments")
        if department != None and department != '' and department != "None":

            dir = os.path.dirname(os.path.realpath(__file__))
            departments_json = os.path.join(
                dir, "data", "json", "organization.json")

            data = json.load(open(departments_json, encoding="utf-8"))
            found = search_organizations(data, department)

            if found != []:
                organization = found['organization']
                officer = found['nodal_officer']
                address = found['address']
                phone = found['phone']
                response = "Here's something I found, <br/><br/>Ministry/Department/Organisation: {}<br/><br/>Nodal Public Grievance Officer Name and Designation: {}<br/><br/>Address: {}<br/><br/>Phone No/Fax/Email: {}".format(
                    organization, officer, address, phone)
                dispatcher.utter_message(response)
        else:
            dispatcher.utter_message(
                template='utter_default', **tracker.slots)
        return []

class ActionStateContact(Action):
    def name(self) -> Text:
        return "action_state_contact"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:
        states = tracker.get_slot("states")
        if states != None and states != '' and states != "None":

            dir = os.path.dirname(os.path.realpath(__file__))
            states_json = os.path.join(
                dir, "data", "json", "state.json")

            data = json.load(open(states_json, encoding="utf-8"))
            found = search_states(data, states)

            if found != []:
                organization = found['state']
                officer = found['nodal_officer']
                address = found['address']
                phone = found['phone']
                response = "Here's something I found, <br/><br/>Ministry/Department/Organisation: {}<br/><br/>Nodal Public Grievance Officer Name and Designation: {}<br/><br/>Address: {}<br/><br/>Phone No/Fax/Email: {}".format(
                    organization, officer, address, phone)
                dispatcher.utter_message(response)
        else:
            dispatcher.utter_message(
                template='utter_default', **tracker.slots)
        return []


def search_organizations(json_object, name):
    for dict in json_object:
        if dict['organization'].lower() == name.lower():
            return dict
    return []


def search_states(json_object, name):
    for dict in json_object:
        if dict['state'].lower() == name.lower():
            return dict
    return []
