pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clonar el repositorio
                git url: 'https://github.com/jafuentes5/integracion_continua.git', branch: 'master'
            }
        }

        stage('Start Existing Container') {
            steps {
                script {
                    // Comando para iniciar un contenedor existente
                    sh "docker start mysql_server"
                }
            }
        }
        // Puedes agregar más etapas del pipeline según sea necesario
    }
}
