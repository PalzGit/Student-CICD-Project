pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        string(name: 'K8S_MANIFEST_DIR', defaultValue: 'k8s', description: 'Repository directory containing the Kubernetes YAML files')
        string(name: 'K8S_NAMESPACE', defaultValue: 'default', description: 'Kubernetes namespace for this project')
        string(name: 'K8S_DEPLOYMENT', defaultValue: 'student-portal', description: 'Deployment resource name from the Kubernetes manifests')
        string(name: 'K8S_CONTAINER', defaultValue: 'student-portal', description: 'Container name inside the Deployment')
    }

    environment {
        IMAGE_REPOSITORY = 'palomapoduval1/student-cicd'
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        IMAGE_BUILD = "${IMAGE_REPOSITORY}:${BUILD_NUMBER}"
        IMAGE_LATEST = "${IMAGE_REPOSITORY}:latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker run --rm \
                      --volume "$WORKSPACE:/workspace" \
                      --workdir /workspace \
                      python:3.11-slim \
                      sh -c 'python -m pip install --no-cache-dir -r requirements.txt && python -m pytest -v'
                '''
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build --tag "$IMAGE_BUILD" --tag "$IMAGE_LATEST" .'
            }
        }

        stage('Push image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: env.DOCKERHUB_CREDENTIALS,
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        set +x
                        printf '%s' "$DOCKERHUB_TOKEN" | docker login --username "$DOCKERHUB_USERNAME" --password-stdin
                        docker push "$IMAGE_BUILD"
                        docker push "$IMAGE_LATEST"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    test -d "$K8S_MANIFEST_DIR" || {
                      echo "Kubernetes manifest directory '$K8S_MANIFEST_DIR' was not found. Confirm Member 3's manifest path and update the build parameter."
                      exit 1
                    }
                    command -v kubectl >/dev/null || {
                      echo 'kubectl is not installed or is not on the Jenkins service account PATH.'
                      exit 1
                    }
                    kubectl apply --namespace "$K8S_NAMESPACE" --filename "$K8S_MANIFEST_DIR"
                    kubectl set image "deployment/$K8S_DEPLOYMENT" \
                      "$K8S_CONTAINER=$IMAGE_BUILD" \
                      --namespace "$K8S_NAMESPACE"
                    kubectl rollout status "deployment/$K8S_DEPLOYMENT" \
                      --namespace "$K8S_NAMESPACE" \
                      --timeout=180s
                    kubectl get pods,services --namespace "$K8S_NAMESPACE"
                '''
            }
        }
    }

    post {
        always {
            sh 'docker image rm "$IMAGE_BUILD" "$IMAGE_LATEST" >/dev/null 2>&1 || true'
        }
        success {
            echo "Build ${BUILD_NUMBER} succeeded; deployed ${IMAGE_BUILD}."
        }
        failure {
            echo 'Pipeline failed. Review the stage output before rerunning.'
        }
    }
}
