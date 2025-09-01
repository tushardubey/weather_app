pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')  // set in Jenkins
        IMAGE_NAME = "tushardubey/weather_app"
    }

    stages {
        stage('Build Image') {
            steps {
                sh """
                    docker build -t $IMAGE_NAME:\$BUILD_NUMBER .
                """
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh """
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                    docker push $IMAGE_NAME:\$BUILD_NUMBER
                    docker tag $IMAGE_NAME:\$BUILD_NUMBER $IMAGE_NAME:latest
                    docker push $IMAGE_NAME:latest
                """
            }
        }

        stage('Deploy to EC2s') {
            steps {
                sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@<EC2_PUBLIC_IP> '
                        docker pull $IMAGE_NAME:latest &&
                        docker stop weather_app || true &&
                        docker rm weather_app || true &&
                        docker run -d --name weather_app -p 80:80 $IMAGE_NAME:latest
                    '
                """
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f'
        }
    }
}
