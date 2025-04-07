import unittest
import json
import urllib.error
import urllib.request
from io import StringIO
from unittest.mock import patch, Mock, MagicMock
from github_activity import fetch_user_events, parse_events, print_events

class TestGithubActivityFunctions(unittest.TestCase):
    @patch("urllib.request.urlopen")  # Patch correctly
    def test_fetch_user_events(self, mock_urlopen):
        # Create a mock HTTP response
        mock_response = MagicMock()

        # Successful response
        events_list = [
            {
                "type": "PushEvent",
                "repo": {"name": "demo-repo"},
                "payload": {}
            }
        ]
        mock_response.__enter__.return_value.status = 200
        mock_response.__enter__.return_value.read.return_value = json.dumps(events_list).encode("utf-8")
        mock_urlopen.return_value = mock_response
        events = fetch_user_events("testuser")
        self.assertIsInstance(events, list)
        self.assertEqual(events[0]["type"], "PushEvent")

        # Missing username
        with self.assertRaises(ValueError) as context:
            fetch_user_events("")
        
        self.assertEqual(str(context.exception), "Username is a required argument.")

        # HTTP error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url=None, code=404, msg="Not Found", hdrs=None, fp=None
            )
        
        with self.assertRaises(ValueError) as context:
            fetch_user_events("invaliduser")
        
        self.assertIn("GitHub API error: 404", str(context.exception))

        # Network error
        mock_urlopen.side_effect = urllib.error.URLError("Network unreachable")

        with self.assertRaises(ValueError) as context:
            fetch_user_events("anyuser")

        self.assertIn("Network error: Network unreachable", str(context.exception))

    def test_parse_events(self):
        # Invalid events list
        events_list = {}
        with self.assertRaises(ValueError) as context:
            parse_events(events_list)
        
        self.assertEqual(str(context.exception), "Parse_Events expected a list, but got a different object.")

        # Emtpy events list
        events_list = []
        parsed_events = parse_events(events_list)
        self.assertEqual(parsed_events, [])

        # Valid list
        events_list = [
            {
                "type": "PushEvent",
                "repo": {
                    "name": "demorepo"
                },
                "payload": {}
            },
            {
                "type": "ActionEvent",
                "repo": {
                    "name": "demorepo"
                },
                "payload": {
                    "action": "created"
                }
            }
        ]

        expected_output = [
            {
                "type": "PushEvent",
                "repo-name": "demorepo",
                "action": "Unknown",
                "count": 1
            },
            {
                "type": "ActionEvent",
                "repo-name": "demorepo",
                "action": "created",
                "count": 1
            }
        ]

        parsed_events = parse_events(events_list)
        self.assertEqual(parsed_events, expected_output)

        # Malformed event list
        events_list = [{}]
        expected_output = [
            {
                "type": "Unknown",
                "repo-name": "Unknown",
                "action": "Unknown",
                "count": 1
            }
        ]

        parsed_events = parse_events(events_list)
        self.assertEqual(parsed_events, expected_output)

    def test_prints_push_event(self):
        # Empty list
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            print_events([])
            self.assertEqual(mock_stdout.getvalue(), "\nNo events to display.\n\n")

        # Full event list
        events = [
            {"type": "PushEvent", "repo-name": "some/repo", "action": "Unknown", "count": 3},
            {"type": "PullRequestEvent", "repo-name": "some/repo", "action": "created", "count": 99},
            {"type": "Unknown", "repo-name": "Unknown", "action": "Unknown", "count": 1}
            ]
        expected_output = "\nPushed 3 commits to some/repo.\n" \
        "Created 99 pull requests in some/repo.\n" \
        "Unhandled Event: Unknown - Unknown\n\n"

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            print_events(events)
            self.assertEqual(mock_stdout.getvalue(), expected_output)