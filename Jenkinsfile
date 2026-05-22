pipeline {
    agent any

    stages {
        stage('Setup and Environment') {
            steps {
                echo 'Checking local system environment...'
                bat 'python --version'
                
                withCredentials([file(credentialsId: 'ENV', variable: 'ENV_FILE')]) {
                    echo 'Copying environment variables to project root...'
                    bat 'copy /Y "%ENV_FILE%" project_root\\.env'
                }
                
                echo 'Setting up virtual environment and dependencies...'
                dir('project_root') {
                    bat 'python -m venv venv'
                    bat 'venv\\Scripts\\python -m pip install --upgrade pip'
                    bat 'venv\\Scripts\\pip install pytest pytest-html python-dotenv langchain langchain-openai langgraph supabase pydantic'
                }
            }
        }

        stage('Run Validation Tests') {
            steps {
                echo 'Running unit and validation tests...'
                dir('project_root') {
                    bat 'venv\\Scripts\\pytest --html=report.html --self-contained-html'
                }
            }
        }

        stage('Pipeline Verification') {
            steps {
                echo 'Starting Company Intelligence Pipeline...'
                dir('project_root') {
                    bat 'venv\\Scripts\\python run_pipeline.py "Apple"'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished. Cleaning up environment files...'
            bat 'if exist project_root\\.env del /F /Q project_root\\.env'
        }
        success {
            echo 'Pipeline successfully built, validated, and verified!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
