import json
import time
from abc import abstractmethod

from app.ingest.application.mq.mq_connection_params import MqConnectionParams
from test.integration.ingest.application.mq.stomp_integration_test_base import StompIntegrationTestBase


class StompListenerIntegrationTestBase(StompIntegrationTestBase):

    def _send_test_message(self, mq_queue_name: str) -> None:
        test_message_json = {}
        test_message_json_str = json.dumps(test_message_json)

        connection = self._create_mq_connection(self._get_mq_connection_params())
        connection.send(mq_queue_name, test_message_json_str)
        connection.disconnect()

    @abstractmethod
    def _get_mq_connection_params(self) -> MqConnectionParams:
        pass

    def _await_until_on_message_has_calls_or_timeout(self, on_message_mock) -> None:
        timeout = self._get_message_await_timeout()
        while not on_message_mock.call_count and time.time() < timeout:
            time.sleep(1)

    def _assert_on_message_has_calls(self, on_message_mock) -> None:
        if on_message_mock.call_count == 0:
            self.fail(msg="The listener did not receive the published message")
