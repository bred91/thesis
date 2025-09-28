# RQ2 Quantitative Evaluation


### Average
| Metric         | Value  |
|----------------|--------|
| ROUGE-1        | 0.4131 |
| ROUGE-2        | 0.2144 |
| ROUGE-L        | 0.3114 |
| BLEU           | 0.0759 |
| METEOR         | 0.2805 |
| BERT Precision | 0.8614 |
| BERT Recall    | 0.8629 |
| BERT F1        | 0.8615 |

### Min-Max
| Metric         | Range           |
|----------------|-----------------|
| ROUGE-1        | 0.0488 - 1.0000 |
| ROUGE-2        | 0.0000 - 1.0000 |
| ROUGE-L        | 0.0488 - 1.0000 |
| BLEU           | 0.0000 - 1.0000 |
| METEOR         | 0.0113 - 0.9977 |
| BERT Precision | 0.7505 - 1.0000 |
| BERT Recall    | 0.7688 - 1.0000 |
| BERT F1        | 0.7919 - 1.0000 |    

### Range Distribution
| Metric         | Range           | Count |
|----------------|-----------------|-------|
| rouge_1        | 0.00 ≤ x < 0.20 | 7     |
| rouge_1        | 0.20 ≤ x < 0.40 | 17    |
| rouge_1        | 0.40 ≤ x < 0.60 | 18    |
| rouge_1        | 0.60 ≤ x < 0.80 | 7     |
| rouge_1        | 0.80 ≤ x ≤ 1.00 | 1     |
| rouge_1        | out_of_range    | 0     |
| rouge_2        | 0.00 ≤ x < 0.20 | 31    |
| rouge_2        | 0.20 ≤ x < 0.40 | 11    |
| rouge_2        | 0.40 ≤ x < 0.60 | 4     |
| rouge_2        | 0.60 ≤ x < 0.80 | 3     |
| rouge_2        | 0.80 ≤ x ≤ 1.00 | 1     |
| rouge_2        | out_of_range    | 0     |
| rouge_l        | 0.00 ≤ x < 0.20 | 21    |
| rouge_l        | 0.20 ≤ x < 0.40 | 13    |
| rouge_l        | 0.40 ≤ x < 0.60 | 10    |
| rouge_l        | 0.60 ≤ x < 0.80 | 5     |
| rouge_l        | 0.80 ≤ x ≤ 1.00 | 1     |
| rouge_l        | out_of_range    | 0     |
| bleu           | 0.00 ≤ x < 0.20 | 41    |
| bleu           | 0.20 ≤ x < 0.40 | 7     |
| bleu           | 0.40 ≤ x < 0.60 | 1     |
| bleu           | 0.60 ≤ x < 0.80 | 0     |
| bleu           | 0.80 ≤ x ≤ 1.00 | 1     |
| bleu           | out_of_range    | 0     |
| meteor         | 0.00 ≤ x < 0.20 | 17    |
| meteor         | 0.20 ≤ x < 0.40 | 25    |
| meteor         | 0.40 ≤ x < 0.60 | 6     |
| meteor         | 0.60 ≤ x < 0.80 | 1     |
| meteor         | 0.80 ≤ x ≤ 1.00 | 1     |
| meteor         | out_of_range    | 0     |
| bert_precision | 0.00 ≤ x < 0.20 | 0     |
| bert_precision | 0.20 ≤ x < 0.40 | 0     |
| bert_precision | 0.40 ≤ x < 0.60 | 0     |
| bert_precision | 0.60 ≤ x < 0.80 | 5     |
| bert_precision | 0.80 ≤ x ≤ 1.00 | 44    |
| bert_precision | out_of_range    | 1     |
| bert_recall    | 0.00 ≤ x < 0.20 | 0     |
| bert_recall    | 0.20 ≤ x < 0.40 | 0     |
| bert_recall    | 0.40 ≤ x < 0.60 | 0     |
| bert_recall    | 0.60 ≤ x < 0.80 | 3     |
| bert_recall    | 0.80 ≤ x ≤ 1.00 | 46    |
| bert_recall    | out_of_range    | 1     |
| bert_f1        | 0.00 ≤ x < 0.20 | 0     |
| bert_f1        | 0.20 ≤ x < 0.40 | 0     |
| bert_f1        | 0.40 ≤ x < 0.60 | 0     |
| bert_f1        | 0.60 ≤ x < 0.80 | 1     |
| bert_f1        | 0.80 ≤ x ≤ 1.00 | 48    |
| bert_f1        | out_of_range    | 1     |

### Median & Quantiles
| Metric         | 25° Quantile | Median | 75° Quantile |
|----------------|--------------|--------|--------------|
| ROUGE-1        | 0.3066       | 0.4035 | 0.5137       |
| ROUGE-2        | 0.0707       | 0.1389 | 0.3154       |
| ROUGE-L        | 0.1692       | 0.2336 | 0.4443       |
| BLEU           | 0.0093       | 0.0632 | 0.1630       |
| METEOR         | 0.1879       | 0.2670 | 0.3401       |
| BERT Precision | 0.8307       | 0.8513 | 0.8946       |
| BERT Recall    | 0.8261       | 0.8552 | 0.8950       |
| BERT F1        | 0.8297       | 0.8517 | 0.8873       |