# Sistema de Gestión de Fútbol - Frontend React

Este proyecto ha sido actualizado con una interfaz web moderna construida con React (servida estáticamente) y un backend en Python con FastAPI.

## Características Nuevas

- **Frontend React**: Interfaz moderna, reactiva y con diseño "Glassmorphism" usando TailwindCSS.
- **Backend API**: Servidor FastAPI que expone la lógica de negocio original (auth, scraping, datos).
- **Ojeador AI**: Interfaz gráfica para buscar jugadores con visualización de fotos y datos.
- **La Liga**: Visualización de tablas, estadísticas detalladas de equipos y actualización de datos en tiempo real desde la web.

## Cómo Ejecutar

1. **Opción Fácil**: Doble clic en `run_app.bat`.
2. **Opción Manual**:
   ```bash
   pip install fastapi uvicorn pydantic python-multipart pandas requests matplotlib
   python server.py
   ```
3. Abre tu navegador en [http://localhost:8000](http://localhost:8000).

## Estructura

- `server.py`: El servidor principal. Sirve la API y el Frontend.
- `frontend_static/index.html`: El código fuente del Frontend (Single File React App).
- `src/`: Lógica de negocio en Python (adaptada del proyecto original).
