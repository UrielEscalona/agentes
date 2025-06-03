# Manual de Instalación y Mantenimiento - Sudoku Solver

## Instalación

### Requisitos Previos
- Docker
- Docker Compose
- Git (opcional)

### Pasos de Instalación

1. Clonar el repositorio (o descargar los archivos):
```bash
git clone <url-del-repositorio>
cd sudoku
```

2. Iniciar los servicios en modo desarrollo:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

3. Acceder a la aplicación:
- Frontend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- RabbitMQ Management: http://localhost:15672 (usuario: guest, contraseña: guest)
- MySQL: localhost:3307 (usuario: root, contraseña: root)

## Mantenimiento

### Limpiar la Base de Datos

Si necesitas limpiar la base de datos, tienes dos opciones:

1. **Opción 1 - Eliminar solo los datos:**
```sql
-- Conectarse a MySQL
mysql -h localhost -P 3307 -u root -proot sudoku

-- Eliminar todos los registros
DELETE FROM tasks;
```

2. **Opción 2 - Eliminar la base de datos completa:**
```bash
# Detener los contenedores
docker-compose -f docker-compose.dev.yml down

# Eliminar el volumen de MySQL
docker volume rm sudoku_mysql_data

# Reiniciar los servicios
docker-compose -f docker-compose.dev.yml up --build
```

### Limpiar Docker

Si necesitas liberar espacio en Docker:

```bash
# Eliminar contenedores detenidos
docker container prune

# Eliminar imágenes no utilizadas
docker image prune

# Eliminar volúmenes no utilizados
docker volume prune

# Eliminar redes no utilizadas
docker network prune

# O hacer todo de una vez
docker system prune -a
```

### Verificar Logs

Para ver los logs de los diferentes servicios:

```bash
# Ver logs de todos los servicios
docker-compose -f docker-compose.dev.yml logs

# Ver logs de un servicio específico
docker-compose -f docker-compose.dev.yml logs api
docker-compose -f docker-compose.dev.yml logs worker
docker-compose -f docker-compose.dev.yml logs mysql
docker-compose -f docker-compose.dev.yml logs rabbitmq
```

### Reiniciar Servicios

Si necesitas reiniciar los servicios:

```bash
# Detener todos los servicios
docker-compose -f docker-compose.dev.yml down

# Iniciar todos los servicios
docker-compose -f docker-compose.dev.yml up --build

# Reiniciar un servicio específico
docker-compose -f docker-compose.dev.yml restart api
docker-compose -f docker-compose.dev.yml restart worker
```

## Solución de Problemas

### Problemas de Conexión

1. **MySQL no responde:**
```bash
# Verificar si el contenedor está corriendo
docker-compose -f docker-compose.dev.yml ps

# Ver logs de MySQL
docker-compose -f docker-compose.dev.yml logs mysql

# Reiniciar MySQL
docker-compose -f docker-compose.dev.yml restart mysql
```

2. **RabbitMQ no responde:**
```bash
# Verificar si el contenedor está corriendo
docker-compose -f docker-compose.dev.yml ps

# Ver logs de RabbitMQ
docker-compose -f docker-compose.dev.yml logs rabbitmq

# Reiniciar RabbitMQ
docker-compose -f docker-compose.dev.yml restart rabbitmq
```

### Problemas de Permisos

Si encuentras problemas de permisos con los volúmenes:

```bash
# Ajustar permisos en el directorio app
chmod -R 777 app/
```

## Estructura del Proyecto

```
sudoku/
├── app/
│   ├── static/          # Archivos frontend
│   │   ├── index.html
│   │   └── result.html
│   ├── config.py        # Configuración
│   ├── main.py         # API FastAPI
│   ├── sudoku.py       # Lógica del Sudoku
│   ├── worker.py       # Worker para procesar tareas
│   └── init_db.sql     # Inicialización de la base de datos
├── docker-compose.dev.yml  # Configuración de desarrollo
├── docker-compose.prod.yml # Configuración de producción
├── Dockerfile          # Imagen base
└── requirements.txt    # Dependencias Python
``` 