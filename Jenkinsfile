pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clonar el repositorio
                git url: 'https://github.com/jafuentes5/integracion_continua.git', branch: 'master'
            }
        }

        stage('Build and Run Python App') {
            steps {
                script {
                    // Construir la imagen Docker con Python
                    def dockerImage = docker.build('python-app-image', '.')
                    
                    // Ejecutar el contenedor Docker
                    dockerImage.run('-p 5000:5000', '--name python-app-container')
                }
            }
        }
    }
}
