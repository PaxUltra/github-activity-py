import unittest
import json
import urllib.error
import urllib.request
from unittest.mock import patch, Mock, MagicMock
from github_activity import fetch_user_events, parse_events

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