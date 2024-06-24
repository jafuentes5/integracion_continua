pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clonar el repositorio Git
                git url: 'https://github.com/jafuentes5/integracion_continua.git'
            }
        }

        stage('Build and Run Python App') {
            steps {
                script {
                    // Construir la imagen Docker con Python
                    def dockerImage = docker.build('python-app-image') {
                        // Copiar el código Python al contenedor
                        copy('app/test.py', '.') // Ajusta la ruta según la estructura de tu repositorio
                    }

                    // Ejecutar el contenedor Docker
                    dockerImage.run('-p 5000:5000', '--name python-app-container')
                }
            }
        }
    }
}
