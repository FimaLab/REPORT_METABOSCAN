pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = "1"
        COMPOSE_DOCKER_CLI_BUILD = "1"
    }

    stages {
        stage('Clone') {
            steps {
                echo 'Jenkins клонирует репозиторий автоматически'
            }
        }

        stage('Build & Run containers (only if code changed)') {
            steps {
                dir("${env.PROJECT_DIR}") {
                    script {
                        def changed = sh(
                            script: 'git diff --name-only HEAD~1 HEAD | grep -q streamlit_app || echo 1',
                            returnStatus: true
                        )
                        if (changed == 0) {
                            echo 'Изменения найдены — пересобираем'
                            sh 'docker compose build'
                        } else {
                            echo 'Изменений нет — пропускаем пересборку'
                        }
                    }
                    sh 'docker compose down && docker compose up -d'
                }
            }
        }
    }
}
