"""
Uses Jenkins REST API to update the validation_pipeline job config
to point to the local Git repo + Jenkinsfile.
"""
import urllib.request
import urllib.parse
import urllib.error
import base64
import sys

JENKINS_URL = "http://127.0.0.1:8080"
JOB_NAME    = "validation_pipeline"

# ── new config.xml ─────────────────────────────────────────────────────────
NEW_CONFIG = r"""<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@1571.1580.v18e46842c125">
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition"
              plugin="workflow-cps@3990.vd281dd77a_388">
    <scm class="hudson.plugins.git.GitSCM" plugin="git@5.7.0">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>C:/Users/RAGHAVENDRA R/OneDrive/Desktop/Validation</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/main</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="empty-list"/>
      <extensions/>
    </scm>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
"""

def get_crumb(opener):
    """Fetch Jenkins crumb for CSRF protection."""
    try:
        url = f"{JENKINS_URL}/crumbIssuer/api/json"
        with opener.open(url) as r:
            import json
            data = json.loads(r.read().decode())
            return data["crumbRequestField"], data["crumb"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Crumb issuer not found – CSRF disabled, continuing without crumb.")
            return None, None
        raise

def main():
    # Build opener (no auth needed if Jenkins has no security configured)
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "Python-Jenkins-Updater/1.0")]

    # Try fetching crumb
    crumb_field, crumb_value = get_crumb(opener)

    # POST new config.xml
    post_url  = f"{JENKINS_URL}/job/{urllib.parse.quote(JOB_NAME)}/config.xml"
    body      = NEW_CONFIG.encode("utf-8")
    headers   = {"Content-Type": "application/xml"}
    if crumb_field:
        headers[crumb_field] = crumb_value

    req = urllib.request.Request(post_url, data=body, headers=headers, method="POST")

    try:
        with opener.open(req) as resp:
            print(f"SUCCESS – Jenkins responded with HTTP {resp.status}")
            print("Job config updated. Now reload Jenkins config from disk.")
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode(errors="ignore")
        print(f"HTTP ERROR {e.code}: {e.reason}")
        print(body_txt[:800])
        if e.code == 403:
            print("\n>> Jenkins has security enabled. We need credentials.")
            print(">> Run this script again with: python fix_jenkins.py <username> <api_token>")
            print(">> Get your API token from: http://127.0.0.1:8080/user/<youruser>/configure")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        # If credentials provided, add Basic Auth
        user, token = sys.argv[1], sys.argv[2]
        creds = base64.b64encode(f"{user}:{token}".encode()).decode()
        import urllib.request as ur
        ur.install_opener(
            ur.build_opener(ur.HTTPBasicAuthHandler())
        )
        # rebuild opener with auth header
        opener_with_auth = urllib.request.build_opener()
        opener_with_auth.addheaders = [
            ("User-Agent",    "Python-Jenkins-Updater/1.0"),
            ("Authorization", f"Basic {creds}"),
        ]
        # patch get_crumb and main to use this opener
        import builtins
        _orig_open = urllib.request.urlopen
        urllib.request.urlopen = opener_with_auth.open
    main()
