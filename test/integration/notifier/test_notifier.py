import json, sys
from celery.result import AsyncResult
from test.integration.integration_test_base import IntegrationTestBase
sys.path.append('app')
import app.notifier.notifier as notifier 

class TestNotifier(IntegrationTestBase):
    def test_notifier(self):
        result = notifier.send_error_notification("Test Subject from DIMS", "Test Body from DIMS", "dts@hu.onmicrosoft.com")
        assert isinstance(result, AsyncResult)
