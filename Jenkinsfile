@Library('xmos_jenkins_shared_library@master') _
getApproval()
pipeline {
  agent {
    label 'x86&&macOS&&Apps'
  }
  environment {
    VIEW = 'gpio'
    REPO = 'lib_gpio'
  }
  options {
    skipDefaultCheckout()
  }
  stages {
    stage('Get view') {
      steps {
        prepareAppsSandbox("${VIEW}", "${REPO}")
      }
    }
    stage('Library checks') {
      steps {
        xcoreLibraryChecks("${REPO}")
      }
    }
    stage('Tests') {
      steps {
        runXmostest("${REPO}", 'tests')
      }
    }
    stage('xCORE builds') {
      steps {
        dir("${REPO}") {
          xcoreAllAppsBuild('examples')
          dir("${REPO}") {
            runXdoc('doc')
          }
        }
      }
    }
  }
  post {
    success {
      updateViewfiles()
    }
    cleanup {
      cleanWs()
    }
  }
}
