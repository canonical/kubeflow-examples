#
# Automated testing of instructions in this guide
#
cd ..
jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="{'text'}" --to notebook kubeflow-cos-integration.ipynb --output kubeflow-cos-integration.code.ipynb
jupyter nbconvert --to script kubeflow-cos-integration.code.ipynb
mv kubeflow-cos-integration.code.txt kubeflow-cos-integration.code.sh
bash kubeflow-cos-integration.code.sh
