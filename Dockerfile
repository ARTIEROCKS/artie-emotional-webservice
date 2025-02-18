FROM python:3.9.7-slim-bullseye

# Instalar bibliotecas necesarias para OpenGL y ffmpeg
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    build-essential \
    libhdf5-dev \
    libatlas-base-dev \
    gfortran \
    gcc-10 g++-10 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 100

RUN apt-get update && apt-get install -y \
    pkg-config \
    libhdf5-dev

WORKDIR /app

# Copiar e instalar las dependencias de Python
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-binary=h5py h5py
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
