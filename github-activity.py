import sys
import json
import urllib.request
from collections import defaultdict

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

def parse_events(events_list):
    event_counts = defaultdict(int)

    # Count the number of occurrences for each type/repo pairing
    # Example, if the user pushed to demo-repo 7 times, the result will be {('PushEvent', 'demo-repo'): 7}
    for event in events_list:
        combo_key = (event.get("type"), event.get("repo").get("name"))
        event_counts[combo_key] += 1

    # Convert back into a list of dictionaries
    parsed_events = [
        {"type": event_type, "repo-name": repo_name, "count": count} for (event_type, repo_name), count in event_counts.items()
    ]

    return parsed_events

if __name__ == "__main__":
    # Get username from commandline arguments
    username = sys.argv[1] if sys.argv[1] else None # The username will be the second argument

    # Get user events
    events_list = fetch_user_events(username)

    # Parse user events
    # event_types = {}
    # for event in events_list:
    #     event_type = event.get("type")
    #     if event.get("type") in event_types:
    #         event_types[event_type] = event_types[event_type] + 1
    #     else:
    #         event_types[event_type] = 1

    # print(event_types)

    parse_events(events_list)