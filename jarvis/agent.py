from google.adk.agents import Agent


# from google.adk.tools import google_search  # Import the search tool
from .tools import (

   capture_details_to_textfile,
   send_mail,
   )



root_agent = Agent(
    name="jarvis",
    #model="gemini-2.0-flash",
    # model="gemini-2.5-flash-native-audio-preview-09-2025",
    # model="gemini-2.0-flash-exp",
    # model ="gemini-3-pro-preview",
    # model="gemini-2.5-flash-native-audio-preview-09-2025",
    model="gemini-2.0-flash-live-001",
    description="Jarvis is an advanced voice agent who helps in booking a flight ticket.",
 instruction = 
    "Your name is Jarvis, an advanced voice agent that helps users book flight tickets. "
    "Conversation flow to follow precisely:\n"
    "1) Ask the user for the trip details in this order (if missing): name, origin (from), destination (to), date, class (economy/business/etc), and any notes.\n"
    "2) After collecting all required fields, repeat the collected details back to the user in a clear short summary and ask: "
    "'Do you confirm sending this booking request email? Please reply with only yes or no.'\n"
    "3) If the user replies with an explicit affirmative (yes, yep, confirmed), call the tool `capture_details_to_textfile` with a JSON/dict containing the collected fields, then call the tool `send_mail` with the user's email address as the argument.\n"
    "4) If the user replies no, ask what to change and loop back to step 1.\n"
    "5) Always be polite and confirm success after the tool returns.\n"
    "When calling tools, provide only the tool invocation; do not send the message text again. "
,

    tools=[
        send_mail,
        capture_details_to_textfile
    ],
)