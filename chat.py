import os
import dialogflow
from google.api_core.exceptions import InvalidArgument

DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = '+13106997821'

text_to_be_analyzed = "Hello"

session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.types.QueryInput(text=text_input)
try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        print("Response:", response.query_result.fulfillment_text)
except InvalidArgument:
        raise

#print(response)

