pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clonar el repositorio
                git url: 'https://github.com/jafuentes5/integracion_continua.git', branch: 'master'
            }
        }

        stage('Se crea la imagen de docker') {
            steps {
                script {
                    def dockerfile = """
                        FROM python:3.9-slim
                        WORKDIR /app                        
                        COPY app/test.py .
                        CMD ["python", app/"test.py"]
                    """

                    writeFile file: 'Dockerfile', text: dockerfile

                    docker.build('python-app-image', '-f Dockerfile .')
                }
            }
        }

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
        }

        /*
        stage('Run Python App') {
            steps {
                script {
                    docker.image('python-app-image').run()
                }
            }
        }
        stage('Detener contenedor') {
            steps {
                script {
                    // Comando para iniciar un contenedor existente
                    sh "docker stop mysql_server"
                }
            }
        }*/
        // Puedes agregar más etapas del pipeline según sea necesario
    }
}
