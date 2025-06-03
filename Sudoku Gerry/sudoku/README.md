# Sudoku Solver

Sistema asíncrono para resolver Sudokus utilizando FastAPI, RabbitMQ y MySQL.

## Arquitectura

### Componentes

1. **API (FastAPI)**
   - Endpoint `/solve` para recibir Sudokus
   - Endpoint `/result/{task_id}` para consultar resultados
   - Servicio de archivos estáticos para el frontend
   - Manejo de CORS para desarrollo

2. **Worker**
   - Consume tareas de RabbitMQ
   - Procesa Sudokus usando backtracking
   - Actualiza resultados en MySQL
   - Manejo de errores y reintentos

3. **RabbitMQ**
   - Cola principal: `sudoku_tasks`
   - Intercambio de mensajes entre API y Worker
   - Gestión de tareas asíncronas

4. **MySQL**
   - Almacenamiento de tareas y resultados
   - Seguimiento de estado de cada Sudoku
   - Estadísticas de resolución

### Flujo de Datos

1. El usuario envía un Sudoku a través del frontend
2. La API:
   - Genera un ID único
   - Guarda el Sudoku en MySQL
   - Envía la tarea a RabbitMQ
3. El Worker:
   - Recibe la tarea de RabbitMQ
   - Actualiza el estado a "processing"
   - Resuelve el Sudoku
   - Guarda el resultado en MySQL
4. El usuario consulta el resultado
5. La API:
   - Busca el resultado en MySQL
   - Devuelve la solución al frontend

## Red

### Tipo de Red

El sistema utiliza una **red bridge** de Docker (`sudoku-network`) por las siguientes razones:

1. **Aislamiento**: 
   - Los contenedores están aislados del host y de otras redes Docker
   - Solo los servicios definidos pueden comunicarse entre sí
   - Mayor seguridad al no exponer servicios innecesariamente

2. **Comunicación Interna**:
   - Los servicios se comunican usando nombres de host (ej: `rabbitmq`, `mysql`)
   - No es necesario conocer las IPs internas
   - DNS automático entre contenedores

3. **Escalabilidad**:
   - Fácil adición de nuevos servicios
   - Posibilidad de escalar horizontalmente
   - Balanceo de carga nativo

4. **Configuración**:
   ```yaml
   networks:
     sudoku-network:
       driver: bridge
   ```

### Puertos

- **8000**: API y Frontend
- **15672**: RabbitMQ Management
- **5672**: RabbitMQ AMQP
- **3307**: MySQL

### Conexiones

```
[Frontend] <-> [API:8000] <-> [RabbitMQ:5672] <-> [Worker]
                    ^
                    |
                    v
              [MySQL:3307]
```

### Variables de Entorno

```yaml
# RabbitMQ
RABBITMQ_HOST: rabbitmq
RABBITMQ_PORT: 5672
RABBITMQ_USER: guest
RABBITMQ_PASSWORD: guest
QUEUE_NAME: sudoku_tasks

# MySQL
MYSQL_HOST: mysql
MYSQL_USER: root
MYSQL_PASSWORD: root
MYSQL_DATABASE: sudoku
```

## Características

- Resolución asíncrona de Sudokus
- Interfaz web intuitiva
- API REST documentada
- Monitoreo de tareas
- Estadísticas de resolución
- Manejo de errores robusto
- Entornos de desarrollo y producción

## Tecnologías

- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **Base de Datos**: MySQL
- **Mensajería**: RabbitMQ
- **Contenedores**: Docker, Docker Compose

## Desarrollo Local

Para ejecutar en modo desarrollo (con recarga automática de código):
```bash
docker-compose -f docker-compose.dev.yml up --build
```

## Producción

Para ejecutar en modo producción:
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## Comandos Útiles

- Detener contenedores:
  ```bash
  # Desarrollo
  docker-compose -f docker-compose.dev.yml down
  
  # Producción
  docker-compose -f docker-compose.prod.yml down
  ```

- Ver logs:
  ```bash
  # Desarrollo
  docker-compose -f docker-compose.dev.yml logs -f
  
  # Producción
  docker-compose -f docker-compose.prod.yml logs -f
  ```

## Documentación

- Documentación Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc` 