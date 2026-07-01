# Ecosistema Personal

Aplicación Django modular para la gestión de finanzas personales y control de salud.

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

- Python 3.13+
- Django 6.0+

## Puesta en marcha

```bash
# 1. Clonar el repositorio
git clone <repo-url> bodylog
cd bodylog

# 2. Crear y activar entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install django

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Crear superusuario (opcional, para acceder al admin)
python manage.py createsuperuser

# 6. Iniciar servidor de desarrollo
python manage.py runserver
```

Acceder a [http://localhost:8000](http://localhost:8000) e iniciar sesión.

## Estructura del proyecto

```
BodyLog/
├── core/                  # App núcleo (landing page con servicios)
├── salud/                 # App de salud (peso, comidas, perfil TMB)
├── finanzas/              # App de finanzas (ingresos, gastos, inversiones)
├── Ecosistema_Personal/   # Configuración del proyecto Django
├── templates/             # Plantillas HTML
│   ├── base/              # Base, navbar, paginación
│   ├── salud/             # Templates de salud
│   ├── finanzas/          # Templates de finanzas
│   └── components/        # Componentes reutilizables
├── static/                # Archivos estáticos (CSS, JS)
└── manage.py              # Script de gestión de Django
```

## Tecnologías

- **Backend**: Django 6.0
- **Frontend**: Tailwind CSS (CDN), Chart.js
- **Base de datos**: SQLite (por defecto)
