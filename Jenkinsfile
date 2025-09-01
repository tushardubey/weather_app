pipeline {
  agent any

  environment {
    IMAGE_NAME = "tushardubey/weather_app"
    SERVERS = "ubuntu@3.80.218.77 ubuntu@3.84.227.187"
  }

  stages {
    stage('Build') {
      steps {
        sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
        sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
      }
    }

    stage('Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                         usernameVariable: 'DH_USER',
                                         passwordVariable: 'DH_PASS')]) {
          sh '''
            echo "${DH_PASS}" | docker login -u "${DH_USER}" --password-stdin
            docker push ${IMAGE_NAME}:${BUILD_NUMBER}
            docker push ${IMAGE_NAME}:latest
          '''
        }
      }
    }

    stage('Deploy to EC2s') {
      steps {
        sshagent (credentials: ['weather-app-ssh']) {
          sh '''
            ssh -o StrictHostKeyChecking=no ubuntu@3.80.218.77 "
              docker pull tushardubey/weather_app:latest &&
              docker stop weather_app || true &&
              docker rm weather_app || true &&
              docker run -d --name weather_app -p 5000:5000 tushardubey/weather_app:latest
            "

            ssh -o StrictHostKeyChecking=no ubuntu@3.84.227.187 "
              docker pull tushardubey/weather_app:latest &&
              docker stop weather_app || true &&
              docker rm weather_app || true &&
              docker run -d --name weather_app -p 5000:5000 tushardubey/weather_app:latest
            "
          '''
        }
      }
    }
  }

  post {
    always { sh 'docker image prune -f || true' }
  }
}
