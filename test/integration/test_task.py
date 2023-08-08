from celery import Celery
from kombu import Queue
import os

app1 = Celery('tasks')
app1.config_from_object('celeryconfig')

def test_publish_queue_task():
    '''Verifies that tasks can be published to a queue
    that this celery worker does not consume'''
    package_id = "12345"
    process_ready_task = os.getenv('PROCESS_READY_TASK_NAME', 'dts.tasks.prepare_and_send_to_drs')
    msg_json = {
        "dlq_testing": True, # So it doesn't get consumed by the external service
        "package_id": package_id,
        "application_name": "ePADD",
        'destination_path': "/dest/path",
        "admin_metadata": {
            "original_queue": os.getenv("PROCESS_PUBLISH_QUEUE_NAME"),
            "task_name": process_ready_task,
            "retry_count": 0
        }
    }
    myqueue = Queue(
        os.getenv("PROCESS_PUBLISH_QUEUE_NAME"), no_declare=True)
    try:
        app1.send_task(process_ready_task, args=[msg_json], kwargs={},
            queue=myqueue)
        assert True
    except:
        assert False
