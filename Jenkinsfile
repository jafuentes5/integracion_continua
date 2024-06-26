pipeline {
    agent any
    
    stages {

        stage("Checkout") {
            steps {
                //Se clona el repositorio donde esta la aplicación que se ejecutará 
                // para el envío de notificaciones, al igual que el dockerfile y el token
                git url: "https://github.com/jafuentes5/integracion_continua.git", branch: "master"
            }
        }        
        
        stage("Se crea la imagen de docker") {
            steps {
                script {
                    //Se construye la imagen del contenedor teniendo en cuenta el docker file
                    docker.build("python-app-image", "-f Dockerfile .")
                }
            }
        }
        
        stage("Se ejecuta la aplicacion de python") {
            steps {
                script {
                    //Se crea el contenedor y se ejecuta de manera desatendida
                    def dockerRunCommand = "docker run -d --name python-app-container --network test-network python-app-image"  
                    sh dockerRunCommand                  
                }
            }
        }
    }
}
