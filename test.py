import os
from slackclient import SlackClient

BOT_NAME = 'testbot'

slack_client = SlackClient('xoxb-273399944180-VnvdaI0HEdShlDzpetgSk99y')

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        print "got!"
        users = api_call.get('members')
        print users
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)

