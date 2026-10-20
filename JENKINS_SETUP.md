# Jenkins setup for the Student CI/CD project

This project pipeline is stored in the root `Jenkinsfile`. Jenkins should load it from the `main` branch using **Pipeline script from SCM**.

## Jenkins prerequisites

- Jenkins Git and Pipeline plugins are installed.
- The Jenkins service account can run Docker, as verified on the EC2 host.
- `kubectl` is installed and available to the Jenkins service account.
- The Jenkins service account has a working kubeconfig/context for the team's Minikube cluster. Do not expose the Kubernetes API or Docker daemon on a public port.
- Member 3's Kubernetes manifests are in `k8s/`. The current Deployment and container are both named `student-portal` in the `default` namespace.

## Add Docker Hub credentials

In **Manage Jenkins → Credentials → System → Global credentials → Add Credentials**, add a **Username with password** credential:

- Username: Docker Hub username for the account that can push to `palomapoduval/student-cicd`
- Password: a Docker Hub access token with the minimum permissions needed to push
- ID: `dockerhub-creds`

Do not put the token in the repository, Jenkinsfile, job parameters, or screenshots.

## Create the Jenkins pipeline job

1. From the Jenkins dashboard, select **New Item**.
2. Name it `student-cicd-pipeline` and choose **Pipeline**.
3. In the Pipeline section, set **Definition** to **Pipeline script from SCM**.
4. Set SCM to **Git** and repository URL to `https://github.com/PalzGit/Student-CICD-Project.git`.
5. Set the branch specifier to `*/main`.
6. Set Script Path to `Jenkinsfile`.
7. Save, then use **Build with Parameters** or **Build Now**.

The first stages run the repository tests in a temporary Python container, build the application image, and push a build-number tag plus `latest`. The deployment stage applies the Kubernetes YAML, updates the named Deployment container to the build-number image, waits for rollout, and prints the pod/service state.

## Kubernetes naming assumptions

The deployment stage defaults to:

- Manifest directory: `k8s`
- Namespace: `default`
- Deployment: `student-portal`
- Container: `student-portal`

Set these build parameters to match Member 3's YAML if their resource names change. The current Deployment manifest references `palomapoduval/student-cicd:latest`; the pipeline updates its image to the current Jenkins build tag.

## Evidence for the lab

Keep screenshots of the successful build stages, test results, pushed image tag in Docker Hub, and Minikube rollout/pods. Remove or obscure usernames, tokens, and other credentials before sharing screenshots.
