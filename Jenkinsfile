pipeline {
    agent any 
    triggers {
        githubPush() 
    }
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t selenium-test-env .'
            }
        }
        stage('Run Tests in Container') {
            steps {
                sh 'docker run --rm selenium-test-env npm test'
            }
        }
    }
    post {
        always {
            emailext (
                subject: "Assignment 3 Test Results - Build #${env.BUILD_NUMBER}",
                body: "The Jenkins pipeline has finished executing the test stage.\n\nCheck the console output here: ${env.BUILD_URL}",
                to: "qasimalik@gmail.com"
            )
        }
    }
}
