import json
import os
import dialogflow
from flask import Flask, request, render_template
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from google.api_core.exceptions import InvalidArgument

# Twilio account info
account_sid = os.environ['TWILIO_ACCT_SID']
auth_token = os.environ['TWILIO_AUTH_TKN']
account_num = os.environ['TWILIO_ACCT_NUM']

twilio_client = Client(account_sid, auth_token)

DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']
DIALOGFLOW_LANGUAGE_CODE = 'en'

app = Flask(__name__)

@app.route('/hello')
def hello_world():
        return 'Hello from Google cloud Flask!'

@app.route('/displayuser', methods=['GET', 'POST'])
def displayuser():
    tgtUser = request.values.get("patients", None)
    print("Display ", tgtUser)
    return "1"

@app.route('/login', methods=['GET', 'POST'])
def login():
    userName = request.values.get("uname", None)
    userPasswd = request.values.get("passwd", None)
    # Place your software to authenticate the user here
    # users = [ 'James', 'Kate', 'Jim', 'Anny' ]
    users = [ {'name':'James', 'headaches':3}, {'name':'Kate', 'headaches':3}, {'name':'Jim', 'headaches':3}, {'name':'Anny', 'headaches':3} ]
    #return render_template('users.html', title='CSCI 485 Demonstration', members=users)
    return render_template('radio.html', title='CSCI 485 Demonstration', members=users)


@app.route('/index', methods=['GET', 'POST'])
def index():
    #name = 'Shahram'
    #return render_template('index.html', title='Welcome', username=name)
    return render_template('login.html')

@app.route("/twilio", methods=['GET', 'POST'])
def twilioserver():
    # get SMS metadata
    msg_from = request.values.get("From", None)
    msg = request.values.get("Body", None)
    if msg_from is None:
        return "0"

    print(msg)
    print('msg_from=',msg_from)
    SESSION_ID = msg_from

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=msg, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response_obj = session_client.detect_intent(session=session, query_input=query_input)
        print(response_obj)
        print("Response: ", response_obj.query_result.fulfillment_text)
        reply_txt = response_obj.query_result.fulfillment_text
        reply = twilio_client.messages.create(to=msg_from, from_= account_num, body=reply_txt)
    except InvalidArgument:
        raise
    return "1"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    #app.run(host='0.0.0.0', debug=True, ssl_context='adhoc')
