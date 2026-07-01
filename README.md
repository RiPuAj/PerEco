# Ecosistema Personal

Aplicación Django modular para la gestión de finanzas personales y control de salud. Preparada para ejecutarse en **Raspberry Pi** con Docker.

## Servicios

### Salud
- Registro de peso corporal con evolución gráfica
- Registro de comidas con calorías por momento del día (desayuno, almuerzo, cena, snack)
- Dashboard con gráficos de peso y calorías agrupados por día/semana/mes
- Cálculo de **TMB** (Tasa Metabólica Basal) y **calorías de mantenimiento** mediante la fórmula Mifflin-St Jeor
- Perfil de usuario con altura, sexo, fecha de nacimiento y nivel de actividad

### Finanzas
- **Dashboard** con KPIs: ingresos/gastos/balance del mes, gasto máximo recomendado, objetivo de ahorro
- **Ingresos** y **Gastos** con categorías personalizables
- **Inversiones** con control de rentabilidad (valor invertido vs actual, % de ganancia/pérdida)
- **Gastos futuros** planificados con prioridades (baja, media, alta)
- **Categorías** personalizables con color para cada tipo (ingreso/gasto)
- Gráfico circular de gastos por categoría
- Cálculo de gasto máximo permitido (ingresos - 20% ahorro)

## Requisitos

- Python 3.13+ (desarrollo) o Docker (producción)
- Django 5.0+

## Puesta en marcha

### Desarrollo (local)

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux:   source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Producción (Docker)

Construir la imagen para ARM (Raspberry Pi) o x86_64:

```bash
docker compose build
docker compose up -d
```

Variables de entorno disponibles:

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `DJANGO_SECRET_KEY` | *(auto-generada)* | Clave secreta de Django |
| `DJANGO_DEBUG` | `False` | Modo depuración |
| `DJANGO_ALLOWED_HOSTS` | `*` | Hosts permitidos (separados por coma) |

### Portainer

1. Añadir el stack desde el repositorio Git
2. Usar `docker-compose.yml` como plantilla
3. Configurar las variables de entorno necesarias
4. Desplegar

La aplicación quedará accesible en el puerto **8000**.

## Estructura

```
BodyLog/
├── core/                  # App núcleo (landing page)
├── salud/                 # App de salud
├── finanzas/              # App de finanzas
├── Ecosistema_Personal/   # Configuración Django
├── templates/             # Plantillas HTML
├── static/                # Archivos estáticos
├── Dockerfile             # Imagen multi-stage (~130 MB)
├── docker-compose.yml     # Orquestación para Portainer
└── entrypoint.sh          # Script de arranque
```

## Tecnologías

- **Backend**: Django 5.1, Gunicorn, Whitenoise
- **Frontend**: Tailwind CSS (CDN), Chart.js
- **Base de datos**: SQLite (volumen persistente)
- **Contenedor**: python:3.13-slim (multi-arch: amd64, arm64, arm/v7)
