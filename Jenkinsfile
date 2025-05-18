pipeline {
    agent any 
    environment {
        DOCKER_USERNAME = "kabrajii"
        APP_NAME = "flask-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKER_USERNAME}/${APP_NAME}"
    }
    
    stages {
        stage("cleaning the workspace") {
            steps {
                script{
                    cleanWs()
                }
            }
        }
        stage("checkout git scm"){
            steps {
                git branch: 'main', url: 'https://github.com/KabraJiii/flask_app_CICD.git'
            }
        }
        stage("docker build.."){
            steps {
                sh 'sudo docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }
        stage("Push Image to DockerHub"){
            steps {
                withCredentials([usernamePassword(credentialsId: 'Docker', passwordVariable: 'password', usernameVariable: 'user')]) {
                     sh """
                        docker login -u ${user} -p ${password}
                        sudo docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    """
}
            }
        }
        stage("Deleting Image Locally"){
            steps {
                sh 'sudo docker rmi -f ${IMAGE_NAME}:${IMAGE_TAG}'
            }
        }
        stage("Update the Deploy file in CD"){
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'GitHub', passwordVariable: 'pass', usernameVariable: 'user')]) {
                        sh """
                            git clone https://github.com/KabraJiii/flask_app_CICD.git
                            cd flask_app_CICD

                            ls
                            cat flask-deploy.yml
                        """
                        sh """
                            echo "new shell"
                            echo $pwd
                            cd flask_app_CICD
                            echo $pwd
                            
                            ls
                            cat flask-deploy.yml
                            echo "Changing tag to ${BUILD_NUMBER}"
                            
                            sed -i 's|image: kabrajii/flask-app:.*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|g' flask-deploy.yml
                            echo "changed tag"

                            cat flask-deploy.yml


                            git add flask-deploy.yml
                            git commit -m "Updated the tag to ${BUILD_NUMBER}"
                            git push origin main
                            
                            """
}
                }
            }
        }
    }
        
}