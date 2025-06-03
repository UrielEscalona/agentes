from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import uuid
import pika
import mysql.connector
from config import (
    RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD,
    MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE,
    QUEUE_NAME
)

app = FastAPI(
    title="Sudoku API",
    description="API para resolver Sudokus de forma asíncrona",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

class SudokuRequest(BaseModel):
    grid: List[List[int]] = Field(
        example=[
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ],
        description="Matriz 9x9 que representa el tablero de Sudoku. Use 0 para celdas vacías."
    )

class SudokuResponse(BaseModel):
    task_id: str = Field(description="ID único de la tarea")
    status: str = Field(description="Estado actual de la tarea")

class SudokuResult(BaseModel):
    task_id: str
    status: str
    solution: Optional[List[List[int]]] = None
    steps: Optional[int] = None
    nodes_explored: Optional[int] = None
    error_message: Optional[str] = None

def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def get_rabbitmq_channel():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
    )
    return connection.channel()

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/result")
async def result_page():
    return FileResponse("static/result.html")

@app.post("/solve", response_model=SudokuResponse)
async def solve_sudoku(request: SudokuRequest):
    try:
        # Generar ID único
        task_id = str(uuid.uuid4())
        
        # Guardar en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (id, grid, status) VALUES (%s, %s, %s)",
            (task_id, json.dumps(request.grid), 'pending')
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        # Enviar a RabbitMQ
        channel = get_rabbitmq_channel()
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=json.dumps({
                'task_id': task_id,
                'grid': request.grid
            })
        )
        
        return SudokuResponse(
            task_id=task_id,
            status='pending'
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/result/{task_id}", response_model=SudokuResult)
async def get_result(task_id: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM tasks WHERE id = %s",
            (task_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        return SudokuResult(
            task_id=result['id'],
            status=result['status'],
            solution=json.loads(result['solution']) if result['solution'] else None,
            steps=result['steps'],
            nodes_explored=result['nodes_explored'],
            error_message=result['error_message']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 