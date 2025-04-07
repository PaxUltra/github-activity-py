import sys
import json
import urllib.error
import urllib.request
from collections import defaultdict

def fetch_user_events(username):
    if not username:
        raise ValueError("Username is a required argument.")

    # Make a request to the GitHub API
    events_url = f'https://api.github.com/users/{username}/events'

    try:
        with urllib.request.urlopen(events_url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except urllib.error.HTTPError as e:
        raise ValueError(f"GitHub API error: {e.code}")
    except urllib.error.URLError as e:
        raise ValueError(f"Network error: {e.reason}")

def parse_events(events_list):
    if not isinstance(events_list, list):
        raise ValueError("Parse_Events expected a list, but got a different object.")

    # A GitHub user may not have any events associated with them, in which case the API will return an empty list
    event_counts = defaultdict(int)

    # Count the number of occurrences for each type/repo pairing
    # Example, if the user pushed to demo-repo 7 times, the result will be {('PushEvent', 'demo-repo', 'Unknown'): 7}
    for event in events_list:
        event_type = event.get("type", "Unknown")
        repo_name = event.get("repo", {}).get("name", "Unknown")
        action = event.get("payload", {}).get("action", "Unknown")

        combo_key = (event_type, repo_name, action)
        event_counts[combo_key] += 1

    # Convert back into a list of dictionaries
    parsed_events = [
        {"type": event_type, "repo-name": repo_name, "action": action, "count": count} for (event_type, repo_name, action), count in event_counts.items()
    ]

    return parsed_events

def print_events(events_list):
    if not events_list:
        print("\nNo events to display.\n")
        return

    # Messages for events that do not have an action associated with them
    event_messages = {
        "CommitCommentEvent": "Commented on commits {count} times in {repo-name}.",
        "PushEvent": "Pushed {count} commits to {repo-name}.",
        "CreateEvent": "Created {repo-name}.",
        "ForkEvent": "Forked {repo-name}.",
        "GollumEvent": "Created/updated wiki pages {count} times in {repo-name}.",
        "PublicEvent": "Made {repo-name} public.",
        "WatchEvent": "Started watching {repo-name}.",
        "DeleteEvent": "Deleted {repo-name}.",
        "MemberEvent": "Accepted invitation to {repo-name}."
    }

    # Messages for events that will have an action in their payload
    action_event_messages = {
        "PullRequestEvent": "pull requests",
        "IssueCommentEvent": "issue comments",
        "IssueEvents": "issues",
        "PullRequestReviewEvent": "pull request reviews",
        "PullRequestReviewCommentEvent": "pull request review comments",
        "PullRequestReviewThreadEvent": "pull request comment threads",
        "ReleaseEvent": "releases",
        "SponsorshipEvent": "sponsorship listings"
    }

    print() # Just formatting

    for event in events_list:
        message_template = event_messages.get(event["type"])
        if message_template:
            print(message_template.format(**event))
        elif event["type"] in action_event_messages.keys():
            action = event.get("action", "Unknown")
            noun = action_event_messages.get(event["type"], "Unknown")
            print(f'{action.capitalize()} {event["count"]} {noun} in {event["repo-name"]}.')
        else:
            print(f'Unhandled Event: {event["type"]} - {event.get("action", "N/A")}')

    print() # Just formatting

if __name__ == "__main__":
    # Get username from commandline arguments
    username = sys.argv[1] if len(sys.argv) > 1 else None # The username will be the second argument

    try:
        # Get user events
        events_list = fetch_user_events(username)

        # Transform event data into the form we want
        parsed_events = parse_events(events_list)

        # Display data to the user in a readable format
        print_events(parsed_events)
    except ValueError as e:
        print(f"\n{e}\n")
    except Exception as e:
        print(f"\nUnexpected error: {e}\n")