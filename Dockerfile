 #Se especifica la imagen base
 FROM python:3.9-slim

 #Se establece el directorio de trabajo en el contenedor
 WORKDIR /app      
 #Se copian los archivos necesarios
 COPY app/send_notifications.py app/
 COPY token.json .
 COPY requirements.txt .

 #Se instalan los paquetes requeridos en requirements.txt
 RUN pip install --no-cache-dir -r requirements.txt                        

 #Se establece el comando por defecto que ejecutara la imagen
 CMD ["python", "app/send_notifications.py"]