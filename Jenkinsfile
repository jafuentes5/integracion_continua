pipeline {
    agent any

    stages {
        stage("Checkout") {
            steps {
                //Se clona el repositorio donde esta la aplicación que se ejecutará 
                // para el envío de notificaciones
                git url: 'https://github.com/jafuentes5/integracion_continua.git', branch: 'master'
            }
        }        
        
        stage("Se crea la imagen de docker") {
            steps {
                script {
                    //Se construye la imagen del contenedor teniendo en cuenta el docker file
                    docker.build('python-app-image', '-f Dockerfile .')
                }
            }
        }
        
        stage("Se ejecuta la aplicacion de python") {
            steps {
                script {
                    // Ejecutar el contenedor
                    def dockerRunCommand = 'docker run --name python-app-container --network test-network python-app-image'
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
    }
}
