// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@v0.39.0') _

getApproval()

pipeline {
  agent {
    label 'documentation && x86_64 && linux'
  }
  environment {
    REPO_NAME = 'lib_gpio'
    VIEW = getViewName(REPO_NAME)
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
        xcorePrepareSandbox("${VIEW}", "${REPO_NAME}")
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
        runXmostest("${REPO_NAME}", 'tests')
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
