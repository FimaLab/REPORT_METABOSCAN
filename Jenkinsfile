pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                echo 'Jenkins клонирует репозиторий автоматически'
            }
        }

        stage('Build & Run containers') {
            steps {
                dir("${env.PROJECT_DIR}") {
                    sh '''
                        docker compose down
                        docker compose up -d --build
                    '''
                }
            }
        }
    }
}
