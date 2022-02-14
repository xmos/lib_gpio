@Library('xmos_jenkins_shared_library@v0.16.2') _

getApproval()

pipeline {
  agent {
    label 'x86_64&&brew&&macOS'
  }
  environment {
    REPO = 'lib_gpio'
    //VIEW = "${env.JOB_NAME.contains('PR-') ? REPO+'_'+env.CHANGE_TARGET : REPO+'_'+env.BRANCH_NAME}"
    VIEW = 'lib_gpio_develop_tools_15_1_4'
  }
  options {
    skipDefaultCheckout()
  }
  stages {
    stage('Get view') {
      steps {
        xcorePrepareSandbox("${VIEW}", "${REPO}")
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

        // Archive all the generated .pdf docs
        archiveArtifacts artifacts: "${REPO}/**/pdf/*.pdf", fingerprint: true, allowEmptyArchive: true
      }
    }
  }
  post {
    success {
      updateViewfiles()
    }
    cleanup {
      xcoreCleanSandbox()
    }
  }
}
