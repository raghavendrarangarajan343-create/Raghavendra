pipeline {
    agent any

    environment {
        // Python 3.13 — avoids build-tool failures on 3.14
        PATH             = "C:\\Users\\RAGHAVENDRA R\\AppData\\Local\\Programs\\Python\\Python313;C:\\Users\\RAGHAVENDRA R\\AppData\\Local\\Programs\\Python\\Python313\\Scripts;${env.PATH}"
        OPENAI_API_KEY   = "your_openai_api_key_here"
        SUPABASE_URL     = "https://taytjixivurgretofvne.supabase.co"
        SUPABASE_KEY     = "sb_publishable_IM6mhchloDp9-vaCaSS8bw_OLd_Wera"
    }

    stages {

        stage('Prepare Environment') {
            steps {
                echo 'Checking Python version...'
                bat 'python --version'

                echo 'Writing .env file...'
                bat '''
                    (
                        echo OPENAI_API_KEY=%OPENAI_API_KEY%
                        echo SUPABASE_URL=%SUPABASE_URL%
                        echo SUPABASE_KEY=%SUPABASE_KEY%
                    ) > project_root\\.env
                '''

                echo 'Creating virtual environment...'
                dir('project_root') {
                    bat 'python -m venv venv'
                    bat 'venv\\Scripts\\python -m pip install --upgrade pip'
                    bat 'venv\\Scripts\\pip install pytest pytest-html python-dotenv langchain langchain-openai langgraph supabase pydantic'
                }
            }
        }

        stage('Front-end Pipeline') {
            steps {
                echo 'Running frontend validation tests (Input & Field Logic)...'
                dir('project_root') {
                    bat 'venv\\Scripts\\pytest tests\\test_01_input_validation.py tests\\test_field_logic.py tests\\test_default_value_handling.py -v --tb=short'
                }
            }
        }

        stage('Back-end Pipeline') {
            steps {
                echo 'Running backend validation tests (Classification, Risk & Sentiment)...'
                dir('project_root') {
                    bat 'venv\\Scripts\\pytest tests\\test_classification.py tests\\test_risk.py tests\\test_sentiment.py -v --tb=short'
                }
            }
        }

        stage('Agentic Orchestration Pipeline') {
            steps {
                echo 'Running full validation suite with HTML report...'
                dir('project_root') {
                    bat 'venv\\Scripts\\pytest --html=report.html --self-contained-html -v'
                }
                echo 'Running Agentic Pipeline verification for Apple...'
                dir('project_root') {
                    bat 'venv\\Scripts\\python run_pipeline.py "Apple"'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up environment files...'
            bat 'if exist project_root\\.env del /F /Q project_root\\.env'
        }
        success {
            echo 'Pipeline successfully completed!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs above.'
        }
    }
}
