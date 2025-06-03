import os

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')

# MySQL Configuration
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'sudoku')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'sudoku')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'sudoku')

# Queue Configuration
QUEUE_NAME = 'sudoku_tasks'
DLX_NAME = 'sudoku_dlx'
DLQ_NAME = 'sudoku_dead_letters'

# Environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development') 