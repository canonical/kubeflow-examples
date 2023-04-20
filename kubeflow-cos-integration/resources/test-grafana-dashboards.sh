#
# Validate Grafana dashboards that are referenced by this guide
#
# Grafana dashboards covered by this tests are tracked in this directory and are in format:
# <repo-name>-<dashboard-filename>
#
set -e

TEST_DASHBOARD="jupyter-notebook-controller.json.tmpl"
REPO="notebook-operators"
REPO_DASHBOARD="charms/jupyter-controller/src/grafana_dashboards/$TEST_DASHBOARD"
echo "Validate $TEST_DASHBOARD in $REPO"
mkdir -p $REPO
cd $REPO
git init -q
git remote add -f origin https://github.com/canonical/$REPO &> /dev/null
git sparse-checkout set "$REPO_DASHBOARD"
git pull -q origin main
cd -
DIFF=$(diff $REPO-$TEST_DASHBOARD  $REPO/$REPO_DASHBOARD)
if [ "$DIFF" != "" ]; then
	echo "Test of $TEST_DASHBOARD failed. Diff:"
	echo "$DIFF"
	exit 1
fi
rm -rf $REPO

TEST_DASHBOARD="basic.json.tmpl"
REPO="argo-operators"
REPO_DASHBOARD="charms/argo-controller/src/grafana_dashboards/$TEST_DASHBOARD"
echo "Validate $TEST_DASHBOARD in $REPO"
mkdir -p $REPO
cd $REPO
git init -q
git remote add -f origin https://github.com/canonical/$REPO &> /dev/null
git sparse-checkout set "$REPO_DASHBOARD"
git pull -q origin main
cd -
DIFF=$(diff $REPO-$TEST_DASHBOARD $REPO/$REPO_DASHBOARD)
if [ "$DIFF" != "" ]; then
        echo "Test of $TEST_DASHBOARD failed. Diff:"
        echo "$DIFF"
        exit 1
fi
rm -rf $REPO

TEST_DASHBOARD="seldon-core.json.tmpl"
REPO="seldon-core-operator"
REPO_DASHBOARD="src/grafana_dashboards/$TEST_DASHBOARD"
echo "Validate $TEST_DASHBOARD in $REPO"
mkdir -p $REPO
cd $REPO
git init -q
git remote add -f origin https://github.com/canonical/$REPO &> /dev/null
git sparse-checkout set "$REPO_DASHBOARD"
git pull -q origin main
cd -
DIFF=$(diff $REPO-$TEST_DASHBOARD $REPO/$REPO_DASHBOARD)
if [ "$DIFF" != "" ]; then
        echo "Test of $TEST_DASHBOARD failed. Diff:"
        echo "$DIFF"
        exit 1
fi
rm -rf $REPO
