pipeline {
  agent any

  environment {
    IMAGE_NAME = "tushardubey/weather_app"
    # Replace <SECOND_EC2_IP> with your second instance public or private IP
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
        sshagent(['ssh-ec2']) {
          script {
            for (srv in env.SERVERS.split()) {
              sh """
                ssh -o StrictHostKeyChecking=no ${srv} '
                  docker pull ${IMAGE_NAME}:latest &&
                  docker rm -f weather_app || true &&
                  docker run -d --name weather_app --restart always -p 80:5000 ${IMAGE_NAME}:latest
                '
              """
            }
          }
        }
      }
    }
  }

  post {
    always { sh 'docker image prune -f || true' }
  }
}
