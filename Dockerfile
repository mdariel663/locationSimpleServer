# Usar una imagen base de Python
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8001
ENV FLASK_APP=app.py  # Cambia 'app.py' si tu archivo principal tiene otro nombre
ENV FLASK_RUN_HOST=0.0.0.0  # Para que Flask esté accesible desde fuera del contenedor

# Comando para ejecutar la aplicación
CMD ["flask", "run"]
