# RQ1 Quantitative Evaluation

## General Summary results
### Average
| Metric         | Value  |
|----------------|--------|
| ROUGE-1        | 0.4229 |
| ROUGE-2        | 0.1215 |
| ROUGE-L        | 0.2458 |
| BLEU           | 0.0890 |
| METEOR         | 0.3337 |
| BERT Precision | 0.8892 |
| BERT Recall    | 0.8877 |
| BERT F1        | 0.8884 |

### Min-Max
| Metric         | Range           |
|----------------|-----------------|
| ROUGE-1        | 0.1852 - 0.6061 |
| ROUGE-2        | 0.0075 - 0.2769 |
| ROUGE-L        | 0.1185 - 0.3896 |
| BLEU           | 0.0000 - 0.2020 |
| METEOR         | 0.1785 - 0.4766 |
| BERT Precision | 0.8325 - 0.9269 |    
| BERT Recall    | 0.8249 - 0.9184 |
| BERT F1        | 0.8249 - 0.9175 |

### Range Distribution
| Metric         | Range           | Count |
|----------------|-----------------|-------|
| rouge_1        | 0.00 ≤ x < 0.20 | 1     |
| rouge_1        | 0.20 ≤ x < 0.40 | 33    |
| rouge_1        | 0.40 ≤ x < 0.60 | 65    |
| rouge_1        | 0.60 ≤ x < 0.80 | 1     |
| rouge_1        | 0.80 ≤ x ≤ 1.00 | 0     |
| rouge_1        | out_of_range    | 0     |
| rouge_2        | 0.00 ≤ x < 0.20 | 91    |
| rouge_2        | 0.20 ≤ x < 0.40 | 9     |
| rouge_2        | 0.40 ≤ x < 0.60 | 0     |
| rouge_2        | 0.60 ≤ x < 0.80 | 0     |
| rouge_2        | 0.80 ≤ x ≤ 1.00 | 0     |
| rouge_2        | out_of_range    | 0     |
| rouge_l        | 0.00 ≤ x < 0.20 | 17    |
| rouge_l        | 0.20 ≤ x < 0.40 | 83    |
| rouge_l        | 0.40 ≤ x < 0.60 | 0     |
| rouge_l        | 0.60 ≤ x < 0.80 | 0     |
| rouge_l        | 0.80 ≤ x ≤ 1.00 | 0     |
| rouge_l        | out_of_range    | 0     |
| bleu           | 0.00 ≤ x < 0.20 | 99    |
| bleu           | 0.20 ≤ x < 0.40 | 1     |
| bleu           | 0.40 ≤ x < 0.60 | 0     |
| bleu           | 0.60 ≤ x < 0.80 | 0     |
| bleu           | 0.80 ≤ x ≤ 1.00 | 0     |
| bleu           | out_of_range    | 0     |
| meteor         | 0.00 ≤ x < 0.20 | 1     |
| meteor         | 0.20 ≤ x < 0.40 | 81    |
| meteor         | 0.40 ≤ x < 0.60 | 18    |
| meteor         | 0.60 ≤ x < 0.80 | 0     |
| meteor         | 0.80 ≤ x ≤ 1.00 | 0     |
| meteor         | out_of_range    | 0     |
| bert_precision | 0.00 ≤ x < 0.20 | 0     |
| bert_precision | 0.20 ≤ x < 0.40 | 0     |
| bert_precision | 0.40 ≤ x < 0.60 | 0     |
| bert_precision | 0.60 ≤ x < 0.80 | 0     |
| bert_precision | 0.80 ≤ x ≤ 1.00 | 100   |
| bert_precision | out_of_range    | 0     |
| bert_recall    | 0.00 ≤ x < 0.20 | 0     |
| bert_recall    | 0.20 ≤ x < 0.40 | 0     |
| bert_recall    | 0.40 ≤ x < 0.60 | 0     |
| bert_recall    | 0.60 ≤ x < 0.80 | 0     |
| bert_recall    | 0.80 ≤ x ≤ 1.00 | 100   |
| bert_recall    | out_of_range    | 0     |
| bert_f1        | 0.00 ≤ x < 0.20 | 0     |
| bert_f1        | 0.20 ≤ x < 0.40 | 0     |
| bert_f1        | 0.40 ≤ x < 0.60 | 0     |
| bert_f1        | 0.60 ≤ x < 0.80 | 0     |
| bert_f1        | 0.80 ≤ x ≤ 1.00 | 100   |
| bert_f1        | out_of_range    | 0     |

### Median & Quantiles
| Metric         | 25° Quantile | Median | 75° Quantile |
|----------------|--------------|--------|--------------|
| ROUGE-1        | 0.3854       | 0.4366 | 0.4679       |
| ROUGE-2        | 0.0824       | 0.1247 | 0.1603       |
| ROUGE-L        | 0.2069       | 0.2442 | 0.2861       |
| BLEU           | 0.0000       | 0.0614 | 0.0974       |
| METEOR         | 0.2807       | 0.3337 | 0.3839       |
| BERT Precision | 0.8773       | 0.8902 | 0.9020       |
| BERT Recall    | 0.8773       | 0.8909 | 0.9003       |
| BERT F1        | 0.8778       | 0.8895 | 0.8993       |



## Technical Summary results
### Average
| Metric         | Value  |
|----------------|--------|
| ROUGE-1        | 0.4539 |
| ROUGE-2        | 0.1368 |
| ROUGE-L        | 0.2233 |
| BLEU           | 0.1226 |
| METEOR         | 0.3145 |
| BERT Precision | 0.8756 |
| BERT Recall    | 0.8564 |
| BERT F1        | 0.8658 |

### Min-Max
| Metric         | Range           |
|----------------|-----------------|
| ROUGE-1        | 0.2849 - 0.5847 |
| ROUGE-2        | 0.0271 - 0.2393 |
| ROUGE-L        | 0.1259 - 0.3099 |
| BLEU           | 0.0000 - 0.2879 |
| METEOR         | 0.1963 - 0.5093 |
| BERT Precision | 0.8302 - 0.9165 |
| BERT Recall    | 0.8232 - 0.8974 |
| BERT F1        | 0.8313 - 0.9062 |

### Range Distribution
| Metric         | Range           | Count |
|----------------|-----------------|-------|
| rouge_1        | 0.00 ≤ x < 0.20 | 0     |
| rouge_1        | 0.20 ≤ x < 0.40 | 17    |
| rouge_1        | 0.40 ≤ x < 0.60 | 83    |
| rouge_1        | 0.60 ≤ x < 0.80 | 0     |
| rouge_1        | 0.80 ≤ x ≤ 1.00 | 0     |
| rouge_1        | out_of_range    | 0     |
| rouge_2        | 0.00 ≤ x < 0.20 | 90    |
| rouge_2        | 0.20 ≤ x < 0.40 | 10    |
| rouge_2        | 0.40 ≤ x < 0.60 | 0     |
| rouge_2        | 0.60 ≤ x < 0.80 | 0     |
| rouge_2        | 0.80 ≤ x ≤ 1.00 | 0     |
| rouge_2        | out_of_range    | 0     |
| rouge_l        | 0.00 ≤ x < 0.20 | 30    |
| rouge_l        | 0.20 ≤ x < 0.40 | 70    |
| rouge_l        | 0.40 ≤ x < 0.60 | 0     |
| rouge_l        | 0.60 ≤ x < 0.80 | 0     |
| rouge_l        | 0.80 ≤ x ≤ 1.00 | 0     |
| rouge_l        | out_of_range    | 0     |
| bleu           | 0.00 ≤ x < 0.20 | 88    |
| bleu           | 0.20 ≤ x < 0.40 | 12    |
| bleu           | 0.40 ≤ x < 0.60 | 0     |
| bleu           | 0.60 ≤ x < 0.80 | 0     |
| bleu           | 0.80 ≤ x ≤ 1.00 | 0     |
| bleu           | out_of_range    | 0     |
| meteor         | 0.00 ≤ x < 0.20 | 2     |
| meteor         | 0.20 ≤ x < 0.40 | 91    |
| meteor         | 0.40 ≤ x < 0.60 | 7     |
| meteor         | 0.60 ≤ x < 0.80 | 0     |
| meteor         | 0.80 ≤ x ≤ 1.00 | 0     |
| meteor         | out_of_range    | 0     |
| bert_precision | 0.00 ≤ x < 0.20 | 0     |
| bert_precision | 0.20 ≤ x < 0.40 | 0     |
| bert_precision | 0.40 ≤ x < 0.60 | 0     |
| bert_precision | 0.60 ≤ x < 0.80 | 0     |
| bert_precision | 0.80 ≤ x ≤ 1.00 | 100   |
| bert_precision | out_of_range    | 0     |
| bert_recall    | 0.00 ≤ x < 0.20 | 0     |
| bert_recall    | 0.20 ≤ x < 0.40 | 0     |
| bert_recall    | 0.40 ≤ x < 0.60 | 0     |
| bert_recall    | 0.60 ≤ x < 0.80 | 0     |
| bert_recall    | 0.80 ≤ x ≤ 1.00 | 100   |
| bert_recall    | out_of_range    | 0     |
| bert_f1        | 0.00 ≤ x < 0.20 | 0     |
| bert_f1        | 0.20 ≤ x < 0.40 | 0     |
| bert_f1        | 0.40 ≤ x < 0.60 | 0     |
| bert_f1        | 0.60 ≤ x < 0.80 | 0     |
| bert_f1        | 0.80 ≤ x ≤ 1.00 | 100   |
| bert_f1        | out_of_range    | 0     |

### Median & Quantiles
| Metric         | 25° Quantile | Median | 75° Quantile |
|----------------|--------------|--------|--------------|
| rouge_1        | 0.4139       | 0.4640 | 0.4932       |
| rouge_2        | 0.1062       | 0.1382 | 0.1655       |
| rouge_l        | 0.1954       | 0.2226 | 0.2488       |
| bleu           | 0.0813       | 0.1195 | 0.1624       |
| meteor         | 0.2723       | 0.3097 | 0.3485       |
| bert_precision | 0.8646       | 0.8759 | 0.8864       |
| bert_recall    | 0.8462       | 0.8557 | 0.8678       |
| bert_f1        | 0.8563       | 0.8664 | 0.8759       |