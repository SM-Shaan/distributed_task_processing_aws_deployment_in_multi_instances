import pika
import time
import os
from celeryconfig import task_queues

def init_queues():
    rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672//')
    
    parameters = pika.URLParameters(rabbitmq_url)
    
    # Try to connect to RabbitMQ
    max_retries = 5
    retry_interval = 5
    
    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            
            for queue in task_queues:
                channel.exchange_declare(
                    exchange=queue.exchange.name,
                    exchange_type=queue.exchange.type,
                    durable=True
                )
                
                channel.queue_declare(
                    queue=queue.name,
                    durable=True
                )
                
                channel.queue_bind(
                    exchange=queue.exchange.name,
                    queue=queue.name,
                    routing_key=queue.routing_key
                )
                
                print(f"Created queue: {queue.name}")
            
            connection.close()
            print("Successfully initialized all queues")
            return True
            
        except pika.exceptions.AMQPConnectionError as e:
            if attempt < max_retries - 1:
                print(f"Failed to connect to RabbitMQ (attempt {attempt + 1}/{max_retries}). Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                print(f"Failed to connect to RabbitMQ after {max_retries} attempts")
                raise e

if __name__ == '__main__':
    init_queues() 