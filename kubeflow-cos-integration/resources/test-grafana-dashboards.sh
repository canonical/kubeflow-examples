#
# Validate Grafana dashboards that are referenced by this guide
#
TEST_DASHBOARD="jupyter-notebook-controller.json.tmpl"
REPO="notebook-operators"
REPO_DASHBOARD="charms/jupyter-controller/src/grafana_dashboards/$TEST_DASHBOARD"
echo "Validate $TEST_DASHBOARD"
mkdir -p $REPO
cd $REPO
git init -q
git remote add -f origin https://github.com/canonical/$REPO &> /dev/null
git sparse-checkout set "$REPO_DASHBOARD"
git pull -q origin kf-962-gh531-cos-integration #main
cd -
diff $TEST_DASHBOARD  $REPO/$REPO_DASHBOARD
rm -rf $REPO
