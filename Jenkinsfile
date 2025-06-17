// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@v0.39.0') _

def clone_test_deps() {
  dir("${WORKSPACE}") {
    sh "git clone git@github.com:xmos/test_support"
    sh "git -C test_support checkout e62b73a1260069c188a7d8fb0d91e1ef80a3c4e1"
    sh "git clone git@github.com:xmos/lib_logging"
    sh "git -C lib_logging checkout v3.3.1"
  }
}

getApproval()

pipeline {
  agent {
    label 'documentation && x86_64 && linux'
  }
  environment {
    REPO_NAME = 'lib_gpio'
  }
  options {
    buildDiscarder(xmosDiscardBuildSettings())
    skipDefaultCheckout()
    timestamps()
  }
  parameters {
    string(
      name: 'TOOLS_VERSION',
      defaultValue: '15.3.1',
      description: 'The XTC tools version'
    )
    string(
      name: 'INFR_APPS_VERSION',
      defaultValue: 'v2.0.1',
      description: 'The infr_apps version'
    )
    string(
          name: 'XMOSDOC_VERSION',
          defaultValue: 'v7.1.0',
          description: 'The xmosdoc version'
    )
  }
  stages {
    stage('Checkout') {
      steps {
        println "Stage running on ${env.NODE_NAME}"
        dir("${REPO_NAME}") {
          checkoutScmShallow()
        }
      }
    }
    stage('Build examples and lib checks' ) {
      steps {
        dir("${REPO_NAME}/examples") {
          xcoreBuild()
        }
        warnError("lib checks") {
          runLibraryChecks("${WORKSPACE}/${REPO_NAME}", "${params.INFR_APPS_VERSION}")
        }
      }
    }

    stage('Tests') {
      steps {
        clone_test_deps()
        withTools(params.TOOLS_VERSION) {
          dir("${REPO_NAME}/tests") {
            createVenv(reqFile: "requirements.txt")
            withVenv{
              sh "pytest -v"
            }
          }
        } // tools
      }
    }
    stage('doc build') {
      steps {
        dir("${REPO_NAME}") {
          buildDocs()
        }
      }
    }
    stage("Archive sandbox"){
      steps {
        archiveSandbox(REPO_NAME)
      }
    } // Archive sandbox
  }
  post {
    cleanup {
      xcoreCleanSandbox()
    }
  }
}
