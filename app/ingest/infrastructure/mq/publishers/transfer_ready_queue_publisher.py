"""
This module defines a TransferReadyQueuePublisher, an implementation of ITransferReadyQueuePublisher
which includes the necessary logic to connect to the remote MQ and publish a transfer ready message.
"""

import os

from app.common.infrastructure.mq.mq_connection_params import MqConnectionParams
from app.common.infrastructure.mq.publishers.stomp_publisher_base import StompPublisherBase
from app.ingest.domain.models.ingest.ingest import Ingest
from app.ingest.domain.mq.transfer_ready_queue_publisher import ITransferReadyQueuePublisher


class TransferReadyQueuePublisher(ITransferReadyQueuePublisher, StompPublisherBase):

    def publish_message(self, ingest: Ingest) -> None:
        message = self.__create_transfer_ready_message(ingest)
        self._logger.info("Publishing transfer ready message... Message body: " + str(message))
        self._publish_message(message)

    def _get_queue_name(self) -> str:
        return os.getenv('MQ_TRANSFER_QUEUE_TRANSFER_READY')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('MQ_TRANSFER_HOST'),
            mq_port=os.getenv('MQ_TRANSFER_PORT'),
            mq_ssl_enabled=os.getenv('MQ_TRANSFER_SSL_ENABLED'),
            mq_user=os.getenv('MQ_TRANSFER_USER'),
            mq_password=os.getenv('MQ_TRANSFER_PASSWORD')
        )

    def __create_transfer_ready_message(self, ingest: Ingest) -> dict:
        # Set destination path based on application
        base_dropbox_path = os.getenv('BASE_DROPBOX_PATH')
        destination_path = ""

        if ingest.depositing_application == "Dataverse":
            destination_path = os.path.join(base_dropbox_path, os.getenv('DATAVERSE_DROPBOX_NAME'), "incoming")
        elif ingest.depositing_application == "ePADD":
            destination_path = os.path.join(base_dropbox_path, os.getenv('EPADD_DROPBOX_NAME'), "incoming")

        return {
            'package_id': ingest.package_id,
            's3_path': ingest.s3_path,
            's3_bucket_name': ingest.s3_bucket_name,
            'destination_path': destination_path,
            'application_name': ingest.depositing_application
        }
