from slackclient import SlackClient
import time
import urllib

BOT_ID = '<bot_id>'
SLACK_BOT_TOKEN = '<slack_bot_token>'

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = ""
    if command.startswith(EXAMPLE_COMMAND):
            command = str(command).split("do")[1]

            if urllib.urlopen(command).getcode() == 200:
                response = str(command) + " is up.!"
            else:
                response = "Sorry, No information regarding your search...we are working on it to improve"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                # print output['text'].split(AT_BOT)[1].strip().lower(), output['channel']

                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None
    

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
