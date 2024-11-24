FROM python:3.9.7-slim-buster

# Instalar bibliotecas necesarias para OpenGL y ffmpeg
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar e instalar las dependencias de Python
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar los archivos de la aplicación
ADD model model
ADD service service
ADD repository repository
ADD config config
COPY app.py app.py

# Exponer el puerto 5000
EXPOSE 5000

# Comando de inicio
CMD ["python3", "app.py", "--host=0.0.0.0", "--port=5000"]
