# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from datetime import date
from typing import Any, Text, Dict, List
from urllib.parse import quote
import sqlite3
import webbrowser
import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
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


class ValidateCredentialsAndDisplayMarks(Action):

    def name(self) -> Text:
        return "validate_credentials_and_display_marks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        messages = []
        #print("tracker : ", tracker)
        for event in (list(tracker.events)):
            #print("Event : ",event)
            if event.get("event") == "user":
                messages.append(event.get("text"))
        print("Messages : ", messages)

        reg_no = messages[-2]
        password = str((tracker.latest_message)['text'])
        conn = sqlite3.connect('students_database.db')
        query = "select * from Student_details where regno = '{0}' and password = '{1}'".format(reg_no,
                                                                                                password)
        print("Final query : ", query)
        df = pd.read_sql(query, conn)
        if df.shape[0] == 1:
            values = list(df.values)[0]
            name = values[0]
            subjects_col = ['S1', 'S2', 'S3', 'S4', 'S5', 'Lab1', 'Lab2']
            marks_df = df[subjects_col]
            val_dict = (marks_df.to_dict('r'))[0]
            failed_subjects = ''
            total_marks = sum(list(val_dict.values()))
            content = "Below are the details " + name + "\n\n\n"

            for k, v in val_dict.items():
                if v < 25:
                    failed_subjects = failed_subjects + k + ', '
                content = content + k + "  : " + str(v) + "\n"

            content = content + "Total : " + " : " + str(total_marks) + "\n"
        else:
            content = "Sorry your credentials are incorrect. Please enter valid credentials next time"
        dispatcher.utter_message(text=content)
        return []


class ActionAskUsn(Action):

    def name(self) -> Text:
        return "action_ask_usn"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        str((tracker.latest_message)['text'])
        dispatcher.utter_message(template="utter_ask_usn")

        return []

class ActionAskPassword(Action):

    def name(self) -> Text:
        return "action_ask_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        str((tracker.latest_message)['text'])
        dispatcher.utter_message(template="utter_ask_password")

        return []


class ValidateCredentialsAndDisplayAttendance(Action):

    def name(self) -> Text:
        return "validate_credentials_and_display_attendance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        messages = []
        #print("tracker : ", tracker)
        for event in (list(tracker.events)):
            #print("Event : ",event)
            if event.get("event") == "user":
                messages.append(event.get("text"))
        print("Messages : ", messages)

        reg_no = messages[-2]
        password = str((tracker.latest_message)['text'])
        conn = sqlite3.connect('students_database.db')
        query = "select * from Student_details where regno = '{0}' and password = '{1}'".format(reg_no,
                                                                                                password)
        print("Final query : ", query)
        df = pd.read_sql(query, conn)
        if df.shape[0] == 1:
            values = list(df.values)[0]
            name = values[0]
            #marks = values[2:8]
            days_col = ['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7',
                        'Day8', 'Day9', 'Day10', 'Day11', 'Day12', 'Day13', 'Day14', 'Day15',
                        'Day16', 'Day17', 'Day18', 'Day19', 'Day20', 'Day21', 'Day22', 'Day23',
                        'Day24', 'Day25', 'Day26', 'Day27', 'Day28', 'Day29', 'Day30']

            attendance_df = df[days_col]
            attendance_data = list(list(attendance_df.values)[0])
            present_no_of_days = attendance_data.count(1)
            absent_no_of_days = attendance_data.count(0)

            content = "Below are the details " + name + "\n\n\n"
            content = content+'No of days present : ' + str(present_no_of_days) + '\nNo of days absent  : ' + str(
                absent_no_of_days)

        else:
            content = "Sorry your credentials are incorrect. Please enter valid credentials next time"
        dispatcher.utter_message(text=content)
        return []


class ActionAdmissionInfo(Action):

    def name(self) -> Text:
        return "action_admission_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        str((tracker.latest_message)['text'])
        dispatcher.utter_message(template="utter_admission_info")

        return []


class DisplayUpcomingHolidays(Action):

    def name(self) -> Text:
        return "display_upcoming_holidays"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        today = date.today()
        print("Today's date:", today)
        this_month = today.strftime("%m")
        df2 = pd.read_excel('2021_calendar.xlsx')
        df2['Date'] = pd.to_datetime(df2['Date'])
        current_month_df = df2[df2['Date'].dt.month == int(this_month)]
        content = 'Total of ' + \
            str(current_month_df.shape[0]) + ' this month\n'+"--\n"
        for i in range(current_month_df.shape[0]):
            content = content + str(current_month_df['Date'].values[i])[:10] + '  -  ' + str(
                current_month_df['Holiday Description'].values[i]) + '\n'

        dispatcher.utter_message(text=content)

        return []


#################################

# class ActionAskUsn(Action):

#     def name(self) -> Text:
#         return "show_query_results"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         to_search = str((tracker.latest_message)['entity'])
#         if not to_search == "":
#             webbrowser.open("https://www.google.com/search?q={}".format(quote(to_search)))
#         return []
#################################
class DisplayUpcomingExams(Action):

    def name(self) -> Text:
        return "display_upcoming_exams"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        today = date.today()
        print("Today's date:", today)
        this_month = today.strftime("%m")
        df2 = pd.read_excel('Exams.xlsx')
        df2['StartDate'] = pd.to_datetime(df2['StartDate'])
        current_month_df = df2[df2['StartDate'].dt.month >= int(this_month)]
        content = 'The upcoming Exam dates are\n' + "--\n" + \
            "Start-Date | Exam-Name | End-Date\n" + "______\n"
        for i in range(current_month_df.shape[0]):
            content = content + str(current_month_df['StartDate'].values[i])[:10] + '  |  ' + str(
                current_month_df['Exam'].values[i])+' | ' + str(current_month_df['EndDate'].values[i])[:10] + '\n'

        dispatcher.utter_message(text=content)

        return []
