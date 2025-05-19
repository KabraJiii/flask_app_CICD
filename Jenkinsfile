pipeline{
    agent any
    environment{
        DOCKER_USERNAME = "kabrajii"
        APP_NAME = "flask-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKER_USERNAME}/${APP_NAME}"


    }


    stages{
        stage('clean the workspace'){
            steps{
                script{
                    cleanWs()
                }
            }
        }

        stage('checkout git scm'){
            steps{
                git branch: 'main', url: 'https://github.com/KabraJiii/flask_app_CICD.git'
            }
        }

        stage('build docker image'){
            steps{
                script{
                    sh "sudo docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }
        stage('Push the Image to DockerHub') {


            steps {
              withCredentials([usernamePassword(credentialsId: 'Docker', passwordVariable: 'password', usernameVariable: 'user')]) {
                // some block


                    sh """
                    
                        echo ${password} | docker login -u ${user} --password-stdin

                        sudo docker push ${IMAGE_NAME}:"${IMAGE_TAG}"
                      


                    """
            }
            }

        }
        stage('Delete Image Locally') {

            steps {
                sh """
                    sudo docker rmi -f ${IMAGE_NAME}:${IMAGE_TAG}
                   
                """

            }

            
        }
         stage('Update the deployment file in CD') {

            steps {
                script{
                    withCredentials([usernamePassword(credentialsId: 'GitHub', usernameVariable: 'user', passwordVariable: 'pass')]) {

                        sh """
                            git clone -b main https://${user}:${pass}@github.com/KabraJiii/flask_app_CICD.git
                            
                            cd flask_app_CICD
                            
                            cat flask-deploy.yml
                            
                            cd  /var/lib/jenkins/workspace/CricketAPI-Pipeline/flask_app_CICD
                            
                            cat flask-deploy.yml

                            echo "Changing tag to ${BUILD_NUMBER}"

                            sed -i 's|image: kabrajii/flask-app:.*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|g' flask-deploy.yml

                            echo "changed tag"

                            cat flask-deploy.yml
                            
                            echo "hello" >> hi.txt
                            
                            git add .
                            git commit . -m "Updated the tag to ${BUILD_NUMBER}"
                            git push origin main

                        """

                    }

                }
            }
        }
    }
}
