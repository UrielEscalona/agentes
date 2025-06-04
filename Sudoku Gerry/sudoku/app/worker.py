import json
import pika
import mysql.connector
import time
from sudoku import Sudoku, Solver
from config import (
    RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD,
    MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE,
    QUEUE_NAME, DLX_NAME, DLQ_NAME
)

def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def update_task_status(task_id, status, solution=None, steps=None, nodes_explored=None, error=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if status == 'completed':
        query = """
            UPDATE tasks 
            SET status = %s, 
                solution = %s, 
                steps = %s, 
                nodes_explored = %s,
                completed_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (status, json.dumps(solution), steps, nodes_explored, task_id))
    elif status == 'failed':
        query = """
            UPDATE tasks 
            SET status = %s, 
                error_message = %s,
                completed_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (status, error, task_id))
    else:
        query = "UPDATE tasks SET status = %s WHERE id = %s"
        cursor.execute(query, (status, task_id))
    
    conn.commit()
    cursor.close()
    conn.close()

def process_sudoku(ch, method, properties, body):
    try:
        # Decodificar el mensaje
        message = json.loads(body)
        task_id = message['task_id']
        grid = message['grid']
        
        # Actualizar estado a processing
        update_task_status(task_id, 'processing')
        
        # Resolver el Sudoku
        sudoku = Sudoku(grid)
        solver = Solver(sudoku)
        is_solved = solver.solve()
        
        if is_solved:
            # Obtener estadísticas
            stats = solver.get_statistics()
            
            # Actualizar con la solución
            update_task_status(
                task_id=task_id,
                status='completed',
                solution=solver.get_solution().tolist(),
                steps=stats['steps_taken'],
                nodes_explored=stats['nodes_explored']
            )
        else:
            update_task_status(
                task_id=task_id,
                status='failed',
                error='No se pudo resolver el Sudoku'
            )
        
        # Confirmar el mensaje
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        # En caso de error, actualizar estado y rechazar el mensaje
        update_task_status(
            task_id=task_id,
            status='failed',
            error=str(e)
        )
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def get_rabbitmq_connection():
    while True:
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT,
                    credentials=credentials
                )
            )
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("No se pudo conectar a RabbitMQ. Reintentando en 5 segundos...")
            time.sleep(5)

def main():
    # Conectar a RabbitMQ con reintentos
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    
    # Declarar el exchange y las colas
    channel.exchange_declare(exchange=DLX_NAME, exchange_type='direct')
    channel.queue_declare(queue=DLQ_NAME)
    channel.queue_bind(exchange=DLX_NAME, queue=DLQ_NAME, routing_key=DLQ_NAME)
    
    # Declarar la cola principal con DLX
    channel.queue_declare(
        queue=QUEUE_NAME,
        arguments={
            'x-dead-letter-exchange': DLX_NAME,
            'x-dead-letter-routing-key': DLQ_NAME
        }
    )
    
    # Configurar el consumidor
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=process_sudoku
    )
    
    print(' [*] Esperando mensajes. Para salir presiona CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main() 