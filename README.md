# Sistema de Gestión de Inventario de Productos Perecederos

Este sistema permite gestionar un inventario de productos perecederos, controlando sus fechas de caducidad y estado actual. Está construido con Flask para el backend y React para el frontend, utilizando PostgreSQL como base de datos.

## Requisitos Previos

- Docker
- Docker Compose
- Git

## Estructura del Proyecto

```
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    ├── public/
    ├── Dockerfile
    └── .env.example
```

## Configuración Inicial

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd sistema-inventario
```

### 2. Configurar el Backend

```bash
# Navegar al directorio del backend
cd backend

# Copiar el archivo de variables de entorno
cp .env.example .env

# Editar .env con tus configuraciones
# Ejemplo de configuración mínima:
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=inventory_db
DB_HOST=db
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:5432/${DB_NAME}
```

### 3. Iniciar los Servicios

```bash
# Construir e iniciar los contenedores
docker-compose up -d --build

# Verificar que los contenedores estén corriendo
docker-compose ps

# Ejecutar las migraciones de la base de datos
docker-compose exec web flask db init
docker-compose exec web flask db migrate
docker-compose exec web flask db upgrade
```

### 4. Verificar la Instalación

- Backend API: http://localhost:5000
- Documentación Swagger: http://localhost:5000/swagger-ui
- Base de datos PostgreSQL: localhost:5432

## Uso de la API

### Documentación de la API

La documentación completa de la API está disponible en:
- Swagger UI: http://localhost:5000/swagger-ui
- OpenAPI JSON: http://localhost:5000/openapi.json

### Endpoints Principales

1. **Productos**
   - `POST /api/products` - Crear nuevo producto
   - `GET /api/products` - Listar productos

2. **Inventario**
   - `POST /api/inventory/entry` - Registrar entrada
   - `POST /api/inventory/exit` - Registrar salida
   - `GET /api/inventory/status` - Ver estado del inventario
   - `GET /api/products/<id>/inventory` - Ver inventario por producto

### Ejemplos de Uso

#### Crear un Producto

```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Leche",
    "description": "Leche entera"
  }'
```

#### Registrar Entrada de Inventario

```bash
curl -X POST http://localhost:5000/api/inventory/entry \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 100,
    "expiration_date": "2024-12-31T00:00:00"
  }'
```

## Mantenimiento y Solución de Problemas

### Logs

Ver logs de los contenedores:
```bash
# Todos los servicios
docker-compose logs

# Servicio específico
docker-compose logs web
docker-compose logs db
```

### Reiniciar Servicios

```bash
# Reiniciar todos los servicios
docker-compose restart

# Reiniciar un servicio específico
docker-compose restart web
```

### Limpiar y Reconstruir

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar también volúmenes (borra la base de datos)
docker-compose down -v

# Reconstruir desde cero
docker-compose up -d --build
```

## Estados del Producto

El sistema maneja tres estados para los productos:

- **Vigente**: El producto no ha vencido
- **Por vencer**: El producto vencerá en los próximos 3 días
- **Vencido**: El producto ya pasó su fecha de caducidad

## Seguridad

- Las variables sensibles deben configurarse en el archivo `.env`
- No compartir las credenciales de la base de datos
- Mantener los contenedores actualizados
- Revisar regularmente los logs en busca de actividad sospechosa

## Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para detalles
