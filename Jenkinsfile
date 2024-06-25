pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                //Se clona el repositorio donde esta la aplicación que se ejecutará 
                // para el envío de notificaciones
                git url: 'https://github.com/jafuentes5/integracion_continua.git', branch: 'master'
            }
        }        
        
        stage('Se crea la imagen de docker') {
            steps {
                script {
                    def dockerfile = """
                        #Se especifica la imagen base
                        FROM python:3.9-slim

                        #Se establece el directorio de trabajo en el contenedor
                        WORKDIR /app      

                        #Se copian los archivos necesarios
                        COPY requirements.txt .                  
                        COPY app/test.py .
                        COPY token.json .

                        #Se instalan los paquetes requeridos en requirements.txt
                        RUN pip install --no-cache-dir -r requirements.txt

                        #Se establece el comando por defecto que ejecutara la imagen
                        CMD ["python", "test.py"]


                    """
                    writeFile file: 'Dockerfile', text: dockerfile

                    docker.build('python-app-image', '-f Dockerfile .')
                }
            }
        }

        /*
        stage('Run Python App') {
            steps {
                script {
                    // Ejecutar el contenedor
                    def dockerRunCommand = 'docker run --name python-app-container python-app-image'
                    def proc = sh(script: dockerRunCommand, returnStatus: true)
                    
                    // Verificar el estado de salida del contenedor
                    if (proc == 0) {
                        echo 'Contenedor ejecutado exitosamente.'
                    } else {
                        error 'Error al ejecutar el contenedor.'
                    }
                }
            }
        } */       
    }
}
