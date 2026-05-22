pipeline {
    agent any

    environment {
        // Point Jenkins to the correct Python 3.13 installation (avoids Python 3.14 build-tool issues)
        PATH = "C:\\Users\\RAGHAVENDRA R\\AppData\\Local\\Programs\\Python\\Python313;C:\\Users\\RAGHAVENDRA R\\AppData\\Local\\Programs\\Python\\Python313\\Scripts;${env.PATH}"
        // Placeholder API keys — tests run in mock mode when real keys are absent
        OPENAI_API_KEY   = "your_openai_api_key_here"
        SUPABASE_URL     = "https://taytjixivurgretofvne.supabase.co"
        SUPABASE_KEY     = "sb_publishable_IM6mhchloDp9-vaCaSS8bw_OLd_Wera"
    }

    stages {
        stage('Setup and Environment') {
            steps {
                echo 'Checking local system environment...'
                bat 'python --version'

                echo 'Writing .env file for project_root...'
                bat '''
                    (
                        echo OPENAI_API_KEY=%OPENAI_API_KEY%
                        echo SUPABASE_URL=%SUPABASE_URL%
                        echo SUPABASE_KEY=%SUPABASE_KEY%
                    ) > project_root\\.env
                '''

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
