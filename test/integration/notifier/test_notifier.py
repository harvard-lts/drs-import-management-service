from unittest import TestCase
import json, sys
from test.integration.integration_test_base import IntegrationTestBase
sys.path.append('app')
import app.notifier.notifier as notifier 

class TestNotifier(TestCase):
    def test_notifier(self):
        message = notifier.send_error_notification("Test Subject from DIMS", "Test Body from DIMS", "dts@hu.onmicrosoft.com")
        json_message = json.loads(message)
        self.assertTrue(type(json_message) is dict)
