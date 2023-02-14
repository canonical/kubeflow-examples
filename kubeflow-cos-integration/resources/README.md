# Resources

## Files

- `kubeflow-cos-integration.ipynb` Jupyter notebook with all steps of the demo, all graphics, and diagrams.

## Convert Jupyter notebook into markdown guide

To convert Jupyter notebook to markdown guide:
```
jupyter nbconvert --to markdown kubeflow-cos-integration.ipynb --output README.md
```

## Automated documentation testing

To convert Jupyter notebook to code-only notebook that contains only code with graphics and text removed:
```
jupyter nbconvert --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags="{'text'}" --to notebook kubeflow-cos-integration.ipynb --output kubeflow-cos-integration.code.ipynb
```

Code only Jupyter notebook will be created `kubeflow-cos-integration.code.ipynb`. Use this notebook for automated testing of this guide.

To convert to text:
```
jupyter nbconvert --to script kubeflow-cos-integration.code.ipynb
```

Text version can be used in automated testing of this guide.

To test doc all prerequisites described in this guide should be satisified:

```
bash test-doc.sh
```

