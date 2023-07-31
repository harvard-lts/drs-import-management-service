import os

broker_url = os.getenv('BROKER_URL')
broker_connection_retry_on_startup=True
task_serializer = 'json'
accept_content = ['application/json']
result_serializer = 'json'
timezone = 'US/Eastern'
enable_utc = True
worker_enable_remote_control = False

task_routes = {
    'dims.tasks.handle_process_status':
        {'queue': os.getenv("PROCESS_CONSUME_QUEUE_NAME")},
    'dims.tasks.handle_transfer_status' :
        {'queue': os.getenv("TRANSFER_CONSUME_QUEUE_NAME")}
}
