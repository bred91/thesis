# CATEGORIZATION
In this section, it is shown the results of the categorization of the data. The categorization is done by using the `categorize` function, which takes a list of categories and a list of data points, and returns a dictionary with the categorization experiments.

## Table of the Results

| Experiment                          | Precision | Recall   | Accuracy |
|-------------------------------------|-----------|----------|----------|
| Original                            | **0.59**  | **0.46** |          |
| Original Examples with Llama 3.1 8B | **0.67**  | **1.0**  | **0.67** |
| New Examples with Llama 3.1 8B      | **0.73**  | **0.99** | **0.72** |


## Details of the Results
### Original
Precision: **0.59** <br>
Recall: **0.46** <br>

### Original Examples with Llama 3.1 8B
Precision: **0.67** <br>
Recall: **1.0** <br>
Accuracy: **0.67** <br>

### New Examples with Llama 3.1 8B
Precision: **0.7272727272727273** <br>
Recall: **0.9863013698630136** <br>
Accuracy: **0.72**  <br>

### Original Examples with Gwen
It does not work with Gwen, as it is not able to categorize the data points.