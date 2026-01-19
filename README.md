# ⚽ Sistema de Gestión de Fútbol

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![React](https://img.shields.io/badge/React-18-cyan.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Sistema completo de gestión de fútbol con autenticación avanzada, scraping de La Liga, búsqueda de jugadores y visualización de estadísticas. Disponible en versión **consola (CLI)** y **web (React + FastAPI)**.

## 📋 Características Principales

- 🔐 **Sistema de autenticación completo**
  - Registro con verificación por email (códigos de 6 dígitos)
  - Login seguro con contraseñas hasheadas
  - Recuperación de contraseña
  - Validaciones robustas con expresiones regulares
  
- 📊 **Web scraping automático**
  - Extracción de clasificación de La Liga desde Wikipedia
  - Actualización manual de datos en tiempo real
  - Limpieza automática de datos
  
- 🔍 **Ojeador de jugadores**
  - Búsqueda en base de datos global (TheSportsDB API)
  - Descarga automática de fotos de jugadores
  - Información completa: equipo, nacionalidad, posición, edad
  
- 📈 **Visualización avanzada**
  - Gráficos interactivos con Chart.js (web)
  - Gráficos estáticos con Matplotlib (consola)
  - Métricas avanzadas calculadas automáticamente
  
- 💻 **Dual Interface**
  - Aplicación web moderna con React y Tailwind CSS
  - Aplicación de consola para usuarios técnicos
  
- 🎨 **Diseño moderno**
  - UI con efecto glassmorphism
  - Responsive design (móvil, tablet, desktop)
  - Animaciones fluidas
  - Modo oscuro integrado

## 🚀 Instalación Rápida

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Gmail con contraseña de aplicación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/sistema-gestion-futbol.git
cd sistema-gestion-futbol
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install fastapi uvicorn pydantic python-multipart pandas requests matplotlib
```

### 3. Configurar Email (Verificación de Cuentas)

Edita `run_app.bat` o crea variables de entorno:

```bash
set EMAIL_USER=tu_email@gmail.com
set EMAIL_PASS=tu_contraseña_de_aplicacion
```

> **💡 Cómo obtener contraseña de aplicación de Gmail:**
> 1. Accede a [myaccount.google.com](https://myaccount.google.com)
> 2. Seguridad → Verificación en 2 pasos (activar)
> 3. Contraseñas de aplicaciones → Generar nueva
> 4. Copia la contraseña de 16 caracteres

## 🎮 Uso

### Opción 1: Aplicación Web (Recomendado)

**Windows:**
```bash
run_app.bat
```

**Linux/Mac:**
```bash
python server.py
```

El navegador se abrirá automáticamente en `http://localhost:8000`

### Opción 2: Aplicación de Consola

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
DAVID_SANTIAGO_PROYECTO/
│
├── data/
│   ├── csvs/
│   │   └── clasificacion_laliga_24_25.csv   # Datos scrapeados
│   ├── graficos/                             # Gráficos generados (PNG)
│   ├── photos/                               # Fotos de jugadores descargadas
│   ├── pending_users.json                    # Usuarios pendientes de verificar
│   └── users.json                            # Base de datos de usuarios
│
├── docs/
│   └── README_FRONTEND.md                    # Documentación del frontend
│
├── frontend_static/
│   ├── images/
│   │   └── logo.png                          # Logo de la aplicación
│   └── index.html                            # Single Page Application (React)
│
├── scripts/
│   ├── debug_load.py                         # Script de depuración
│   └── test_api.py                           # Tests de la API
│
├── src/
│   ├── api_logic.py                          # Lógica de negocio para API
│   ├── auth.py                               # Sistema de autenticación CLI
│   ├── cargar_ai.py                          # Ojeador de jugadores
│   ├── database.py                           # Gestión de usuarios y verificación
│   ├── email_utils.py                        # Envío de correos SMTP
│   ├── scrape_laliga.py                      # Web scraping de Wikipedia
│   ├── validators.py                         # Validaciones con regex
│   └── ver_laliga.py                         # Visualización y análisis de datos
│
├── main.py                                   # Aplicación de consola
├── server.py                                 # Servidor FastAPI
├── run_app.bat                               # Script de inicio automático
├── requirements.txt                          # Dependencias del proyecto
└── README.md                                 # Este archivo
```

## 🔧 Funcionalidades Detalladas

### 1. Sistema de Autenticación

#### Registro de Usuarios
- Validación de username (3-20 caracteres, alfanumérico + guiones bajos)
- Validación de email con regex
- Validación de contraseña (8+ caracteres, mayúsculas, minúsculas, números, especiales)
- Confirmación de contraseña
- Envío automático de código de verificación por email

#### Verificación por Email
- Código de 6 dígitos
- Expiración en 10 minutos
- Opción de reenvío de código
- Sistema de usuarios pendientes separado

#### Recuperación de Contraseña
- Solicitud de código por username o email
- Validación de código temporal
- Actualización segura de contraseña

### 2. Clasificación de La Liga

#### Scraping Automático
- Extrae datos desde Wikipedia en tiempo real
- Identifica automáticamente la tabla correcta
- Limpia nombres de equipos (elimina referencias y anotaciones)
- Guarda en formato CSV

#### Visualización de Datos
- Tabla interactiva con selección de equipos
- Ordenamiento por posición
- Responsive design (oculta columnas en móviles)

#### Estadísticas por Equipo
- **Básicas**: Posición, Puntos, Partidos Jugados
- **Resultados**: Victorias, Empates, Derrotas
- **Goles**: A favor, en contra, diferencia
- **Métricas Avanzadas**:
  - Puntos por partido
  - Tasa de victorias/empates/derrotas
  - Eficiencia ofensiva/defensiva
  - Balance ofensivo/defensivo

### 3. Ojeador de Jugadores

#### Búsqueda
- Base de datos global de TheSportsDB
- Búsqueda por nombre (parcial o completo)
- Información completa del jugador:
  - Nombre completo
  - Equipo actual
  - Nacionalidad
  - Posición
  - Edad (calculada desde fecha de nacimiento)
  - Estado (activo/retirado)
  - Deporte y género

#### Gestión de Fotos
- Descarga automática desde la API
- Guarda en carpeta `data/photos/`
- Soporta PNG y JPG
- Sanitización de nombres de archivo

### 4. Visualización de Datos

#### Gráficos Web (Chart.js)
1. **Top 10 Clasificación**
   - Barras horizontales
   - Colores graduales según puntos
   
2. **Análisis Radar de Equipos**
   - 5 métricas: Victorias%, Empates%, Derrotas%, Potencia Ofensiva, Fragilidad Defensiva
   - Selector de equipo
   - Interactivo

#### Gráficos Consola (Matplotlib)
1. **Pie Chart**: Distribución de resultados
2. **Bar Chart**: Goles a favor vs contra
3. **Horizontal Bars**: Promedios por partido
4. **Bar Chart**: Tasas porcentuales
5. **Top 10**: Clasificación con colores graduales

Todos los gráficos se guardan en alta calidad (300 DPI) en `data/graficos/`

## 📡 Documentación de la API

### Autenticación

| Endpoint | Método | Body | Respuesta |
|----------|--------|------|-----------|
| `/api/register` | POST | `{username, email, password}` | Código de verificación enviado |
| `/api/verify` | POST | `{username, code}` | Cuenta verificada |
| `/api/resend-code` | POST | `{username}` o `{email}` | Código reenviado |
| `/api/login` | POST | `{username, password}` | Token de sesión |
| `/api/forgot-password` | POST | `{username}` o `{email}` | Código de reset enviado |
| `/api/reset-password` | POST | `{username, code, new_password}` | Contraseña actualizada |

### La Liga

| Endpoint | Método | Parámetros | Respuesta |
|----------|--------|------------|-----------|
| `/api/laliga` | GET | - | Array con clasificación completa |
| `/api/laliga/update` | POST | - | Datos actualizados desde Wikipedia |
| `/api/laliga/{team_name}` | GET | `team_name` | Estadísticas detalladas del equipo |

### Ojeador

| Endpoint | Método | Body | Respuesta |
|----------|--------|------|-----------|
| `/api/scout` | POST | `{name}` | Información del jugador + foto |

## 🎨 Tecnologías Utilizadas

### Backend
- **Python 3.8+** - Lenguaje principal
- **FastAPI** - Framework web moderno y rápido
- **Pandas** - Manipulación y análisis de datos
- **Matplotlib** - Generación de gráficos estáticos
- **Requests** - Peticiones HTTP
- **BeautifulSoup/lxml** - Parsing HTML (vía pandas)
- **smtplib** - Envío de emails
- **hashlib** - Hashing de contraseñas

### Frontend
- **React 18** - Framework de UI
- **Tailwind CSS** - Framework de estilos
- **Chart.js** - Gráficos interactivos
- **Font Awesome** - Biblioteca de iconos
- **Babel Standalone** - Transpilación JSX en navegador

### APIs Externas
- **Wikipedia** - Datos de La Liga
- **TheSportsDB** - Información de jugadores
- **Gmail SMTP** - Verificación por email

## 🔒 Seguridad Implementada

- ✅ Contraseñas hasheadas con SHA256
- ✅ Validaciones estrictas con expresiones regulares
- ✅ Verificación obligatoria de email
- ✅ Códigos temporales con expiración (10 minutos)
- ✅ Separación de usuarios verificados y pendientes
- ✅ CORS configurado para desarrollo seguro
- ✅ Sanitización de inputs
- ✅ Manejo seguro de errores sin exponer información sensible

## 📝 Ejemplos de Uso

### Ejemplo 1: Registrar Usuario y Verificar

```python
import requests

# 1. Registro
response = requests.post("http://localhost:8000/api/register", json={
    "username": "david_santiago",
    "email": "david@example.com",
    "password": "MiPass123!"
})
print(response.json())
# Output: {"status": "pending", "message": "Se ha enviado un código..."}

# 2. Verificación (con código recibido por email)
response = requests.post("http://localhost:8000/api/verify", json={
    "username": "david_santiago",
    "code": "123456"
})
print(response.json())
# Output: {"status": "success", "message": "Cuenta verificada correctamente"}

# 3. Login
response = requests.post("http://localhost:8000/api/login", json={
    "username": "david_santiago",
    "password": "MiPass123!"
})
print(response.json())
# Output: {"status": "success", "username": "david_santiago", ...}
```

### Ejemplo 2: Obtener Clasificación

```python
import requests

response = requests.get("http://localhost:8000/api/laliga")
data = response.json()

print("Top 5 La Liga:")
for team in data[:5]:
    print(f"{team['Pos']}. {team['Equipo']} - {team['Pts']} pts")

# Output:
# Top 5 La Liga:
# 1. Real Madrid - 46 pts
# 2. Barcelona - 41 pts
# 3. Atlético Madrid - 38 pts
# ...
```

### Ejemplo 3: Buscar Jugador

```python
import requests

response = requests.post("http://localhost:8000/api/scout", json={
    "name": "Messi"
})
jugador = response.json()

print(f"Jugador: {jugador['nombre']}")
print(f"Equipo: {jugador['equipo']}")
print(f"Nacionalidad: {jugador['nacionalidad']}")
print(f"Edad: {jugador['edad']} años")
print(f"Foto: {jugador['foto_url']}")
```

### Ejemplo 4: Actualizar Datos (CLI)

```python
from src.scrape_laliga import extraer_clasificacion_laliga

# Ejecutar scraping
extraer_clasificacion_laliga()
# Output: ¡Éxito! Tabla encontrada y guardada en 'data/csvs/clasificacion_laliga_24_25.csv'
```

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo de clasificación"

**Solución:**
```bash
python -c "from src.scrape_laliga import extraer_clasificacion_laliga; extraer_clasificacion_laliga()"
```

### Error: "No se pudo enviar el correo"

**Causas comunes:**
1. Variables de entorno no configuradas
2. Contraseña de aplicación incorrecta
3. Verificación en 2 pasos no activada

**Solución:**
1. Verifica que `EMAIL_USER` y `EMAIL_PASS` estén definidos
2. Genera una nueva contraseña de aplicación en Google
3. Asegúrate de que la verificación en 2 pasos esté activa

### Error: "ModuleNotFoundError"

**Solución:**
```bash
pip install -r requirements.txt
```

O instala manualmente:
```bash
pip install fastapi uvicorn pandas requests matplotlib
```

### Puerto 8000 ya en uso

**Solución:**
Cambiar puerto en `server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Cambiar a 8080 o cualquier otro
```

### Error al importar módulos de `src/`

**Solución:**
Asegúrate de ejecutar desde el directorio raíz del proyecto:
```bash
cd DAVID_SANTIAGO_PROYECTO
python main.py
```

## 🚧 Roadmap - Mejoras Futuras

### Versión 2.0
- [ ] Migrar base de datos de JSON a PostgreSQL
- [ ] Implementar JWT para autenticación
- [ ] Sistema de caché con Redis
- [ ] Rate limiting en API

### Versión 2.1
- [ ] Historial de clasificación (múltiples temporadas)
- [ ] Comparación entre equipos
- [ ] Sistema de favoritos
- [ ] Notificaciones push para cambios importantes

### Versión 2.2
- [ ] Modo oscuro/claro toggle
- [ ] Filtros avanzados en tablas
- [ ] Export de datos a PDF/Excel
- [ ] Compartir estadísticas en redes sociales

### Versión 3.0
- [ ] Aplicación móvil nativa (React Native)
- [ ] Machine Learning para predicción de resultados
- [ ] Chat en tiempo real entre usuarios
- [ ] Sistema de ligas fantasy

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. **Fork** el proyecto
2. Crea una **rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

### Guía de Estilo

- Usa nombres de variables descriptivos
- Comenta código complejo
- Sigue PEP 8 para Python
- Escribe tests para nuevas funcionalidades
- Actualiza la documentación



## 👨‍💻 Autores

**David y Santiago**

- GitHub: [@davidggarciiia](https://github.com/davidggarciiia) y [@santiago25gotor](https://github.com/santiago25gotor)
- Email: davidgomezgarcia00@gmail.com y santiago25goam@gmail.com

## 🙏 Agradecimientos

- [TheSportsDB](https://www.thesportsdb.com/) - API gratuita de datos deportivos
- [Wikipedia](https://es.wikipedia.org/) - Fuente de datos de La Liga
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
- [React](https://react.dev/) - Biblioteca de UI
- [Chart.js](https://www.chartjs.org/) - Gráficos interactivos
- [Tailwind CSS](https://tailwindcss.com/) - Framework de estilos
- Comunidad de Python y JavaScript por las excelentes bibliotecas

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~3000+
- **Archivos Python**: 10
- **Endpoints API**: 8
- **Componentes React**: 10
---

<div align="center">

⭐ **Si te ha gustado este proyecto, dale una estrella en GitHub!** ⭐

</div>

---

**Nota**: Este proyecto es para fines educativos. Los datos de La Liga son propiedad de sus respectivos dueños.
