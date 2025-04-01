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
            if response.status != 200:
                raise ValueError(f"GitHub API error: {response.status}")

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

    for event in events_list:
        match event.get("type"):
            case "CommitCommentEvent":
                print(f'Commented on commits {event.get("count")} times in {event.get("repo-name")}.')
            case "PushEvent":
                print(f'Pushed {event.get("count")} commits to {event.get("repo-name")}.')
            case "CreateEvent":
                print(f'Created {event.get("repo-name")}.')
            case "PullRequestReviewEvent":
                match event.get("action"):
                    case "created":
                        print(f'Created {event.get("count")} pull request reviews for {event.get("repo-name")}.')
            case "PullRequestReviewCommentEvent":
                match event.get("action"):
                    case "created":
                        print(f'Commented {event.get("count")} times on pull request reviews for {event.get("repo-name")}.')
            case "IssueCommentEvent":
                match event.get("action"):
                    case "created":
                        print(f'Commented {event.get("count")} times on issues for {event.get("repo-name")}.')
                    case "edited":
                        print(f'Edited {event.get("count")} issue comments in {event.get("repo-name")}.')
                    case "deleted":
                        print(f'Deleted {event.get("count")} issue comments in {event.get("repo-name")}.')
            case "PullRequestEvent":
                match event.get("action"):
                    case "opened":
                        print(f'Opened {event.get("count")} pull requests for {event.get("repo-name")}.')
                    case "edited":
                        print(f'Edited {event.get("count")} pull requests for {event.get("repo-name")}.')
                    case "closed":
                        print(f'Closed {event.get("count")} pull requests for {event.get("repo-name")}.')
                    case "reopened":
                        print(f'Reopened {event.get("count")} pull requests for {event.get("repo-name")}.')
                    case "assigned":
                        print(f'Assigned pull requests {event.get("count")} times in {event.get("repo-name")}.')
                    case "unassigned":
                        print(f'Unassigned pull requests {event.get("count")} times in {event.get("repo-name")}.')
                    case "review_requested":
                        print(f'Requested reviews for {event.get("count")} pull requests in {event.get("repo-name")}.')
                    case "review_request_removed":
                        print(f'Removed review requests {event.get("count")} times in {event.get("repo-name")}.')
                    case "labeled":
                        print(f'Labeled pull requests {event.get("count")} times in {event.get("repo-name")}.')
                    case "unlabeled":
                        print(f'Unlabeled pull requests {event.get("count")} times in {event.get("repo-name")}.')
                    case "synchronize":
                        print(f'Synchronized pull requests {event.get("count")} times in {event.get("repo-name")}.')
            case "DeleteEvent":
                print(f'Deleted {event.get("count")} branches/tags in {event.get("repo-name")}.')
            case "ForkEvent":
                print(f'Forked {event.get("repo-name")}.')
            case "GollumEvent":
                print(f'Created/updated wiki pages {event.get("count")} times in {event.get("repo-name")}.')
            case "DeleteEvent":
                print(f'Deleted {event.get("count")} branches/tags in {event.get("repo-name")}.')
            case "IssuesEvent":
                match event.get("action"):
                    case "opened":
                        print(f'Opened {event.get("count")} issues in {event.get("repo-name")}.')
                    case "edited":
                        print(f'Edited {event.get("count")} issues in {event.get("repo-name")}.')
                    case "closed":
                        print(f'Closed {event.get("count")} issues in {event.get("repo-name")}.')
                    case "reopened":
                        print(f'Reopened {event.get("count")} issues in {event.get("repo-name")}.')
                    case "assigned":
                        print(f'Assigned issues {event.get("count")} times in {event.get("repo-name")}.')
                    case "unassigned":
                        print(f'Unassigned issues {event.get("count")} times in {event.get("repo-name")}.')
                    case "labeled":
                        print(f'Labeled issues {event.get("count")} times in {event.get("repo-name")}.')
                    case "unlabeled":
                        print(f'Unlabeled issues {event.get("count")} times in {event.get("repo-name")}.')
            case "MemberEvent":
                print(f'Accepted invitation to {event.get("repo-name")}.')
            case "PublicEvent":
                print(f'Made {event.get("repo-name")} public.')
            case "PullRequestReviewThreadEvent":
                match event.get("action"):
                    case "resolved":
                        print(f'Resolved {event.get("count")} pull request comment threads in {event.get("repo-name")}.')
                    case "unresolved":
                        print(f'Unresolved {event.get("count")} pull request comment threads in {event.get("repo-name")}.')
            case "ReleaseEvent":
                match event.get("action"):
                    case "published":
                        print(f'Published {event.get("count")} releases in {event.get("repo-name")}.')
            case "SponsorshipEvent":
                match event.get("action"):
                    case "created":
                        print(f'Created {event.get("count")} sponsorship listings for {event.get("repo-name")}.')
            case "WatchEvent":
                print(f'Started watching {event.get("repo-name")}.')
            case _:
                print(f'Unhandled Event: {event.get("type")} - {event.get("action")}')

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