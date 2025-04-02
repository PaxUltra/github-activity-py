import unittest
import json
import urllib.request
from unittest.mock import patch, Mock, MagicMock
from github_activity import fetch_user_events, parse_events

class TestGithubActivityFunctions(unittest.TestCase):
    def setUp(self):
        self.sample_events_list = [
            {
                "type": "PushEvent",
                "repo": {"name": "demo-repo"},
                "payload": {}
            }
        ]

    @patch("urllib.request.urlopen")  # Patch correctly
    def test_fetch_user_events(self, mock_urlopen):
        # Create a mock HTTP response
        mock_response = MagicMock()
        mock_response.__enter__.return_value.status = 200
        mock_response.__enter__.return_value.read.return_value = json.dumps(self.sample_events_list).encode("utf-8")

        # Assign mock response to urlopen mock
        mock_urlopen.return_value = mock_response

        # Call function
        events = fetch_user_events("testuser")

        # Assertions
        self.assertIsInstance(events, list)
        self.assertEqual(events[0]["type"], "PushEvent")
