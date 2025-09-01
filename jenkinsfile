pipeline {
  agent any

  environment {
    IMAGE_NAME = "tushardubey/weather_app"
    IMAGE_TAG  = "latest"
    FULL_IMAGE = "${IMAGE_NAME}:${IMAGE_TAG}"
    SERVERS    = "ubuntu@3.80.218.77 ubuntu@3.84.227.187"
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/tushardubey/weather_app.git'
      }
    }

    stage('Build Image') {
      steps {
        sh "docker build -t ${FULL_IMAGE} ."
      }
    }

    stage('Push to DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh """
            echo "${DH_PASS}" | docker login -u "${DH_USER}" --password-stdin
            docker push ${FULL_IMAGE}
          """
        }
      }
    }

    stage('Deploy to EC2s') {
      steps {
        sshagent(credentials: ['ssh-ec2']) {
          script {
            for (srv in env.SERVERS.split()) {
              sh """
                ssh -o StrictHostKeyChecking=no ${srv} '
                  docker ps -q --filter "name=weather_app" | xargs -r docker stop;
                  docker ps -aq --filter "name=weather_app" | xargs -r docker rm;
                  docker pull ${FULL_IMAGE};
                  docker run -d --name weather_app --restart always -p 80:8000 ${FULL_IMAGE};
                '
              """
            }
          }
        }
      }
    }
  }

  post {
    always {
      sh 'docker image prune -f || true'
    }
  }
}
