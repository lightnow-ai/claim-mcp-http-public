#!groovy

def PROJECT = 'claim-mcp-http-public'
def IMAGE = "harbor.apitree.net/lightnow-ai/${PROJECT}"

properties([
    disableConcurrentBuilds(abortPrevious: true),
    buildDiscarder(logRotator(daysToKeepStr: '14', numToKeepStr: '20')),
    githubProjectProperty(projectUrlStr: "https://github.com/lightnow-ai/${PROJECT}/")
])

def sourceCommit
def revision
def version
def immutableTag
node('build-agent') {
    timeout(time: 20, unit: 'MINUTES') {
        checkout scm
        sourceCommit = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
        revision = sourceCommit.take(12)
        version = sh(script: '''python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])' ''', returnStdout: true).trim()
        immutableTag = "${version}-${revision}"

        stage('Test') {
            sh '''docker run --rm \
                -v "$PWD:/workspace" \
                -w /workspace \
                python:3.13-slim \
                sh -c 'pip install --disable-pip-version-check -e ".[test]" && pytest' '''
        }

    }
}

stage('Native architecture builds') {
    def builds = [:]
    ['amd64': 'build-agent', 'arm64': 'container-build-arm64'].each { architecture, label ->
        builds[architecture] = {
            node(label) {
                timeout(time: 20, unit: 'MINUTES') {
                    checkout scm
                    if (sh(script: 'git rev-parse HEAD', returnStdout: true).trim() != sourceCommit) error('Fixture source changed')
                    def expected = architecture == 'amd64' ? 'x86_64' : 'aarch64|arm64'
                    sh "uname -m | grep -Eq '^(${expected})\$'"
                    def nativeTag = "${immutableTag}-${architecture}"
                    sh "docker build --build-arg VERSION=${version} --build-arg VCS_REF=${revision} -t ${IMAGE}:${nativeTag} ."
                    sh "docker run --rm --network none --read-only --tmpfs /tmp:rw,noexec,nosuid,nodev,size=16m --cap-drop ALL --security-opt no-new-privileges --memory 128m --cpus 0.5 --pids-limit 32 --entrypoint python ${IMAGE}:${nativeTag} -c 'import os; from claim_mcp_http_public.server import SERVER_NAME; assert os.getuid() == 10001; assert SERVER_NAME == \"io.github.lightnow-ai/claim-mcp-http-public\"'"
                    sh "docker push ${IMAGE}:${nativeTag}"
                }
            }
        }
    }
    parallel builds
}

node('build-agent') {
    timeout(time: 10, unit: 'MINUTES') {
        stage('Publish multiarchitecture fixture') {
            def tags = "--tag ${IMAGE}:${immutableTag}" + (env.BRANCH_NAME == 'master' ? " --tag ${IMAGE}:${version}" : '')
            sh "docker buildx imagetools create ${tags} ${IMAGE}:${immutableTag}-amd64 ${IMAGE}:${immutableTag}-arm64"
            sh "docker buildx imagetools inspect --raw ${IMAGE}:${immutableTag} | jq -e '[.manifests[].platform | .os + \"/\" + .architecture] | contains([\"linux/amd64\", \"linux/arm64\"])'"
        }
    }
}
