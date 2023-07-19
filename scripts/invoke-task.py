from celery import Celery
import os

app1 = Celery('tasks')
app1.config_from_object('celeryconfig')

s3_bucket = os.getenv("S3_BUCKET_NAME", "dataverse-export-dev")
s3_path = "doi-12-3456-transfer-service-test"

        
arguments = {
            'testing': "true",
            'package_id': "12345",
            's3_path': s3_path,
            's3_bucket_name': s3_bucket,
            'destination_path': os.path.join(os.getenv('BASE_DROPBOX_PATH'), os.getenv('DATAVERSE_DROPBOX_NAME'), "incoming"),
            'application_name': "Dataverse",
            'transfer_status': "successful",
            "admin_metadata": {"original_queue": os.getenv("TRANSFER_CONSUME_QUEUE_NAME"), "retry_count": 0}}

res = app1.send_task('dims.tasks.handle_transfer_status',
                     args=[arguments], kwargs={},
                     queue=os.getenv("TRANSFER_CONSUME_QUEUE_NAME"))
