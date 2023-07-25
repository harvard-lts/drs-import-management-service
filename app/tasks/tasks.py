from celery import Celery
import os
import traceback
from app.ingest.domain.services.exceptions.process_service_exception import ProcessServiceException
from app.ingest.domain.services.exceptions.transfer_service_exception import TransferServiceException
from app.containers import Services
import app.notifier.notifier as notifier
from celery.exceptions import Reject

app = Celery()
app.config_from_object('celeryconfig')

process_task = os.getenv('PROCESS_TASK_NAME', 'dims.tasks.handle_process_status')
transfer_task = os.getenv('TRANSFER_TASK_NAME', 'dims.tasks.handle_transfer_status')
retries = os.getenv('MESSAGE_MAX_RETRIES', 3)

@app.task(bind=True, serializer='json', name=process_task, max_retries=retries, acks_late=True)
def handle_process_status(self, message_body):
    if "dlq_testing" in message_body:
        raise Reject("reject", requeue=False)
    try:
        process_service = Services.process_service()
        process_service.handle_process_status_message(message_body, self.request.id)
    except ProcessServiceException as e:
        exception_msg = traceback.format_exc()
        send_error_notifications(message_body, e, exception_msg)
        
@app.task(bind=True, serializer='json', name=transfer_task, max_retries=retries, acks_late=True)
def handle_transfer_status(self, message_body):
    if "dlq_testing" in message_body:
        raise Reject("reject", requeue=False)
    try:
        transfer_service = Services.transfer_service()
        transfer_service.handle_transfer_status_message(message_body, self.request.id)
        if 'testing' in message_body:
            app.send_task("dims.tasks.do_task", args=[message_body], kwargs={},
                    queue=(os.getenv("PROCESS_PUBLISH_QUEUE_NAME") +'-dryrun')) 
    except TransferServiceException as e:
        exception_msg = traceback.format_exc()
        send_error_notifications(message_body, e, exception_msg)

def send_error_notifications(message_body, exception, exception_msg):
    msg = "Could not process export for DRSIngest for {}.  Error {}.".format(message_body.get("package_id"), str(exception))
    body = msg + "\n" + exception_msg
    notifier.send_error_notification(str(exception), body)