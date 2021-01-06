@Library('xmos_jenkins_shared_library@v0.15.1') _

getApproval()

pipeline {
  agent none
  //Tools for AI verif stage. Tools for standard stage in view file
  parameters {
    string(
      name: 'TOOLS_VERSION',
      defaultValue: '15.0.2',
      description: 'The tools version to build with (check /projects/tools/ReleasesTools/)'
      )
  }
  stages {
    stage('Standard build and XS2 tests') {
      agent {
        label 'x86_64&&brew'
      }
      environment {
        REPO = 'lib_gpio'
        // VIEW = "${env.JOB_NAME.contains('PR-') ? REPO+'_'+env.CHANGE_TARGET : REPO+'_'+env.BRANCH_NAME}"
        VIEW = "lib_gpio_feature_test_xs3"
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
              dir('examples/app_gpio_flashing_leds'){
                runXmake(".", "", "XCOREAI=1")
                stash name: 'app_gpio_flashing_leds', includes: 'bin/xcoreai/gpio_flashing_leds_xcoreai.xe, '
              }
              dir("${REPO}") {
                runXdoc('doc')
              }
            }
          }
        }
      }
      post {
        
        cleanup {
          xcoreCleanSandbox()
        }
      }
    }

    stage('xcore.ai Verification'){
      agent {
        label 'xcore.ai-explorer'
      }
      environment {
        // '/XMOS/tools' from get_tools.py and rest from tools installers
        TOOLS_PATH = "/XMOS/tools/${params.TOOLS_VERSION}/XMOS/xTIMEcomposer/${params.TOOLS_VERSION}"
      }
      stages{
        stage('Install Dependencies') {
          steps {
            sh '/XMOS/get_tools.py ' + params.TOOLS_VERSION
            installDependencies()
          }
        }
        stage('xrun'){
          steps{
            toolsEnv(TOOLS_PATH) {  // load xmos tools
              //Just run on HW and error on incorrect binary etc. We need specific HW for it to run so just check it loads OK
              unstash 'app_gpio_flashing_leds'
              sh 'xrun --id 0 bin/xcoreai/gpio_flashing_leds_xcoreai.xe'
            }
          }
        }
      }//stages
      post {
        cleanup {
          cleanWs()
        }
      }
    }// xcore.ai

    stage('Update view files') {
      agent {
        label 'x86_64&&brew'
      }
      when {
        expression { return currentBuild.result == "SUCCESS" }
      }
      steps {
        updateViewfiles()
      }
    }
  }
}

