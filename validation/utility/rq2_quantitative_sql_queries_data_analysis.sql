-- Average values for each evaluation metric
SELECT
    AVG(rouge_1)         AS avg_rouge_1,
    AVG(rouge_2)         AS avg_rouge_2,
    AVG(rouge_l)         AS avg_rouge_l,
    AVG(bleu)            AS avg_bleu,
    AVG(meteor)          AS avg_meteor,
    AVG(bert_precision)  AS avg_bert_precision,
    AVG(bert_recall)     AS avg_bert_recall,
    AVG(bert_f1)         AS avg_bert_f1
FROM rq2_quantitative_evaluations;


-- Min/Max values for each evaluation metric
SELECT
    MIN(rouge_1)         AS min_rouge_1,
    MAX(rouge_1)         AS max_rouge_1,
    MIN(rouge_2)         AS min_rouge_2,
    MAX(rouge_2)         AS max_rouge_2,
    MIN(rouge_l)         AS min_rouge_l,
    MAX(rouge_l)         AS max_rouge_l,
    MIN(bleu)            AS min_bleu,
    MAX(bleu)            AS max_bleu,
    MIN(meteor)          AS min_meteor,
    MAX(meteor)          AS max_meteor,
    MIN(bert_precision)  AS min_bert_precision,
    MAX(bert_precision)  AS max_bert_precision,
    MIN(bert_recall)     AS min_bert_recall,
    MAX(bert_recall)     AS max_bert_recall,
    MIN(bert_f1)         AS min_bert_f1,
    MAX(bert_f1)         AS max_bert_f1
FROM rq2_quantitative_evaluations;


-- Distribution of overall evaluation scores
SELECT 'rouge_1' AS campo,
    CASE
        WHEN rouge_1 >= 0.0 AND rouge_1 < 0.2 THEN '0.00 ≤ x < 0.20'
        WHEN rouge_1 >= 0.2 AND rouge_1 < 0.4 THEN '0.20 ≤ x < 0.40'
        WHEN rouge_1 >= 0.4 AND rouge_1 < 0.6 THEN '0.40 ≤ x < 0.60'
        WHEN rouge_1 >= 0.6 AND rouge_1 < 0.8 THEN '0.60 ≤ x < 0.80'
        WHEN rouge_1 >= 0.8 AND rouge_1 <= 1.0 THEN '0.80 ≤ x ≤ 1.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_quantitative_evaluations
GROUP BY range

UNION ALL

SELECT 'rouge_2' AS campo,
    CASE
        WHEN rouge_2 >= 0.0 AND rouge_2 < 0.2 THEN '0.00 ≤ x < 0.20'
        WHEN rouge_2 >= 0.2 AND rouge_2 < 0.4 THEN '0.20 ≤ x < 0.40'
        WHEN rouge_2 >= 0.4 AND rouge_2 < 0.6 THEN '0.40 ≤ x < 0.60'
        WHEN rouge_2 >= 0.6 AND rouge_2 < 0.8 THEN '0.60 ≤ x < 0.80'
        WHEN rouge_2 >= 0.8 AND rouge_2 <= 1.0 THEN '0.80 ≤ x ≤ 1.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_quantitative_evaluations
GROUP BY range

UNION ALL

SELECT 'rouge_l' AS campo,
    CASE
        WHEN rouge_l >= 0.0 AND rouge_l < 0.2 THEN '0.00 ≤ x < 0.20'
        WHEN rouge_l >= 0.2 AND rouge_l < 0.4 THEN '0.20 ≤ x < 0.40'
        WHEN rouge_l >= 0.4 AND rouge_l < 0.6 THEN '0.40 ≤ x < 0.60'
        WHEN rouge_l >= 0.6 AND rouge_l < 0.8 THEN '0.60 ≤ x < 0.80'
        WHEN rouge_l >= 0.8 AND rouge_l <= 1.0 THEN '0.80 ≤ x ≤ 1.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_quantitative_evaluations
GROUP BY range

UNION ALL

SELECT 'bleu' AS campo,
    CASE
        WHEN bleu >= 0.0 AND bleu < 0.2 THEN '0.00 ≤ x < 0.20'
        WHEN bleu >= 0.2 AND bleu < 0.4 THEN '0.20 ≤ x < 0.40'
        WHEN bleu >= 0.4 AND bleu < 0.6 THEN '0.40 ≤ x < 0.60'
        WHEN bleu >= 0.6 AND bleu < 0.8 THEN '0.60 ≤ x < 0.80'
        WHEN bleu >= 0.8 AND bleu <= 1.0 THEN '0.80 ≤ x ≤ 1.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_quantitative_evaluations
GROUP BY range

UNION ALL

SELECT 'meteor' AS campo,
    CASE
        WHEN meteor >= 0.0 AND meteor < 0.2 THEN '0.00 ≤ x < 0.20'
        WHEN meteor >= 0.2 AND meteor < 0.4 THEN '0.20 ≤ x < 0.40'
        WHEN meteor >= 0.4 AND meteor < 0.6 THEN '0.40 ≤ x < 0.60'
        WHEN meteor >= 0.6 AND meteor < 0.8 THEN '0.60 ≤ x < 0.80'
        WHEN meteor >= 0.8 AND meteor <= 1.0 THEN '0.80 ≤ x ≤ 1.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_quantitative_evaluations
GROUP BY range

UNION ALL

SELECT 'bert_precision' AS campo,
    CASE
        WHEN bert_precision >= 0.0 AND bert_precision < 0.2 THEN '0.00 ≤ x < 0.20'
        WHEN bert_precision >= 0.2 AND bert_precision < 0.4 THEN '0.20 ≤ x < 0.40'
        WHEN bert_precision >= 0.4 AND bert_precision < 0.6 THEN '0.40 ≤ x < 0.60'
        WHEN bert_precision >= 0.6 AND bert_precision < 0.8 THEN '0.60 ≤ x < 0.80'
        WHEN bert_precision >= 0.8 AND bert_precision <= 1.0 THEN '0.80 ≤ x ≤ 1.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_quantitative_evaluations
GROUP BY range

UNION ALL

SELECT 'bert_recall' AS campo,
    CASE
        WHEN bert_recall >= 0.0 AND bert_recall < 0.2 THEN '0.00 ≤ x < 0.20'
        WHEN bert_recall >= 0.2 AND bert_recall < 0.4 THEN '0.20 ≤ x < 0.40'
        WHEN bert_recall >= 0.4 AND bert_recall < 0.6 THEN '0.40 ≤ x < 0.60'
        WHEN bert_recall >= 0.6 AND bert_recall < 0.8 THEN '0.60 ≤ x < 0.80'
        WHEN bert_recall >= 0.8 AND bert_recall <= 1.0 THEN '0.80 ≤ x ≤ 1.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_quantitative_evaluations
GROUP BY range

UNION ALL

SELECT 'bert_f1' AS campo,
    CASE
        WHEN bert_f1 >= 0.0 AND bert_f1 < 0.2 THEN '0.00 ≤ x < 0.20'
        WHEN bert_f1 >= 0.2 AND bert_f1 < 0.4 THEN '0.20 ≤ x < 0.40'
        WHEN bert_f1 >= 0.4 AND bert_f1 < 0.6 THEN '0.40 ≤ x < 0.60'
        WHEN bert_f1 >= 0.6 AND bert_f1 < 0.8 THEN '0.60 ≤ x < 0.80'
        WHEN bert_f1 >= 0.8 AND bert_f1 <= 1.0 THEN '0.80 ≤ x ≤ 1.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_quantitative_evaluations
GROUP BY range;
