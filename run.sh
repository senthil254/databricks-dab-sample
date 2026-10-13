#!/bin/bash
# Usage (web terminal): bash /Workspace/Users/praveen@networth.awsapps.com/dab_v1/run.sh dev|prod|both
set -e
export DATABRICKS_CONFIG_FILE=/Workspace/Users/praveen@networth.awsapps.com/databrickscfg
# web terminal injects auth for the current workspace; clear it so the profile decides
unset DATABRICKS_HOST DATABRICKS_TOKEN DATABRICKS_CLIENT_ID DATABRICKS_CLIENT_SECRET DATABRICKS_AUTH_TYPE
cd "$(dirname "$0")"
T=${1:-both}; [ "$T" = both ] && T="dev prod"
for t in $T; do
  echo "===== $t"
  databricks bundle validate -t $t
  databricks bundle deploy -t $t
  databricks bundle run dab_demo_project_job -t $t
done
