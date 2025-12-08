pipeline {
    agent any

    parameters {
        choice(
            name: 'ACTION',
            choices: ['FULL_PIPELINE', 'FRONTEND_ONLY', 'BACKEND_ONLY', 'DATABASE_ONLY'],
            description: 'Select what you want to deploy'
        )
    }

    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
        REGISTRY = "yourregistry/kp3"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        /* ================================
           FRONTEND BUILD + PUSH
        ================================= */
        stage('Build Frontend Image') {
            when {
                anyOf {
                    expression { params.ACTION == 'FULL_PIPELINE' }
                    expression { params.ACTION == 'FRONTEND_ONLY' }
                }
            }
            steps {
                echo "Building Frontend Image"
                sh """
                    docker build -t ${REGISTRY}-frontend:${IMAGE_TAG} ./frontend
                    docker push ${REGISTRY}-frontend:${IMAGE_TAG}
                """
            }
        }

        /* =================================
           BACKEND BUILD + PUSH
        ================================== */
        stage('Build Backend Image') {
            when {
                anyOf {
                    expression { params.ACTION == 'FULL_PIPELINE' }
                    expression { params.ACTION == 'BACKEND_ONLY' }
                }
            }
            steps {
                echo "Building Backend Image"
                sh """
                    docker build -t ${REGISTRY}-backend:${IMAGE_TAG} ./backend
                    docker push ${REGISTRY}-backend:${IMAGE_TAG}
                """
            }
        }

        /* =================================
           DATABASE BUILD (Optional)
        ================================== */
        stage('Build Database Image') {
            when {
                anyOf {
                    expression { params.ACTION == 'FULL_PIPELINE' }
                    expression { params.ACTION == 'DATABASE_ONLY' }
                }
            }
            steps {
                echo "Building Database Image"
                sh """
                    docker build -t ${REGISTRY}-database:${IMAGE_TAG} ./database
                    docker push ${REGISTRY}-database:${IMAGE_TAG}
                """
            }
        }

        /* ====================================
           APPLY K8s DEPLOYMENT (YOUR STAGE)
        ===================================== */

        stage('Apply Kubernetes Deployment') {
            when { expression { params.ACTION == 'FULL_PIPELINE' } }
            steps {
                script {

                    // Update image tags in YAML
                    sh """
                        sed -i 's/__IMAGE_TAG__/${IMAGE_TAG}/g' k8s/frontend-deployment.yaml
                        sed -i 's/__IMAGE_TAG__/${IMAGE_TAG}/g' k8s/backend-deployment.yaml
                    """

                    // Delete old deployments/services
                    sh """
                        kubectl delete deployment frontend --ignore-not-found
                        kubectl delete deployment backend --ignore-not-found
                        kubectl delete statefulset database --ignore-not-found
                        kubectl delete service frontend --ignore-not-found
                        kubectl delete service backend --ignore-not-found
                        kubectl delete service database --ignore-not-found
                    """

                    // Create PVC if not exists
                    sh """
                        kubectl get pvc shared-pvc || kubectl apply -f k8s/shared-pvc.yaml
                    """

                    // Apply all YAMLs
                    sh "kubectl apply -f k8s/"
                }
            }
        }
    }
}
