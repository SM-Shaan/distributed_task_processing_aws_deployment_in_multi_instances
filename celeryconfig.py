from kombu import Exchange, Queue
import os

broker_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
result_backend = os.getenv('REDIS_URL', 'redis://redis:6379/0')

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

worker_prefetch_multiplier = 1 # Number of tasks to prefetch
worker_max_tasks_per_child = 1000 # Number of tasks a worker can process before being replaced
worker_max_memory_per_child = 200000 # Maximum memory a worker can use before being replaced
worker_pool = 'solo' # Use solo pool for debugging
worker_concurrency = 1 # Number of concurrent tasks a worker can process
worker_send_task_events = True # Send task events to the broker
task_send_sent_event = True # Send task sent events to the broker

task_queues = (
    Queue('default', Exchange('default', type='direct'), routing_key='default'),
    Queue('high_priority', Exchange('high_priority', type='direct'), routing_key='high_priority'),
    Queue('low_priority', Exchange('low_priority', type='direct'), routing_key='low_priority'),
    Queue('data_processing', Exchange('data_processing', type='direct'), routing_key='data_processing'),
    Queue('email_sending', Exchange('email_sending', type='direct'), routing_key='email_sending'),
    Queue('file_processing', Exchange('file_processing', type='direct'), routing_key='file_processing'),
)

task_queues = tuple(
    Queue(
        queue.name,
        Exchange(queue.exchange.name, type=queue.exchange.type, durable=True),
        routing_key=queue.routing_key,
        durable=True
    )
    for queue in task_queues
)

task_routes = {
    'tasks.process_task': {
        'queue': 'default',
        'routing_key': 'default'
    }
}

# Add task-specific routing
task_routes.update({
    'tasks.process_data_task': {'queue': 'data_processing', 'routing_key': 'data_processing'},
    'tasks.send_email_task': {'queue': 'email_sending', 'routing_key': 'email_sending'},
    'tasks.process_file_task': {'queue': 'file_processing', 'routing_key': 'file_processing'},
})

# Configure task retry policy
task_annotations = {
    'tasks.process_task': {
        'rate_limit': '10/s',
        'retry_backoff': True,
        'retry_backoff_max': 600,  # Maximum retry delay in seconds
        'max_retries': 3,  # Maximum number of retries
        'retry_jitter': True  # Add jitter to prevent thundering herd
    }
}

task_acks_late = True
task_reject_on_worker_lost = True
task_track_started = True
task_time_limit = 3600
task_soft_time_limit = 3300
task_create_missing_queues = True

broker_connection_retry = True
broker_connection_retry_on_startup = True
broker_connection_max_retries = 5
broker_heartbeat = 10
broker_connection_timeout = 30

task_track_started = True
task_ignore_result = False
task_store_errors_even_if_ignored = True 