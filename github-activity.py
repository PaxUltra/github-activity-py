import sys
import json
import urllib.request

def fetch_user_events(username):
    if not username:
        print("Username is a required argument.")
        return None
    else:
        # Make a request to the GitHub API
        events_url = f'https://api.github.com/users/{username}/events'

        with urllib.request.urlopen(events_url) as response:
            data = response.read().decode('utf-8')
            events_list = json.loads(data)

    return events_list


if __name__ == "__main__":
    # Get username from commandline arguments
    username = sys.argv[1] if sys.argv[1] else None # The username will be the second argument

    # Get user events
    events_list = fetch_user_events(username)

    print(len(events_list))

    # Parse user events
    event_types = {}
    for event in events_list:
        event_type = event.get("type")
        if event.get("type") in event_types:
            event_types[event_type] = event_types[event_type] + 1
        else:
            event_types[event_type] = 1

    print(event_types)