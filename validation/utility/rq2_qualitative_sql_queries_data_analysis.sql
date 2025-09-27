-- Average values for each evaluation metric
SELECT
    AVG(accuracy)      AS avg_accuracy,
    AVG(completeness)  AS avg_completeness,
    AVG(usefulness)    AS avg_usefulness,
    AVG(readability)   AS avg_readability,
    AVG(overall)       AS avg_overall
FROM rq2_qualitative_evaluations
WHERE evaluation_type = 'g_eval';


-- Min/Max values for each evaluation metric
SELECT
    MIN(accuracy)      AS min_accuracy,
    MAX(accuracy)      AS max_accuracy,
    MIN(completeness)  AS min_completeness,
    MAX(completeness)  AS max_completeness,
    MIN(usefulness)    AS min_usefulness,
    MAX(usefulness)    AS max_usefulness,
    MIN(readability)   AS min_readability,
    MAX(readability)   AS max_readability,
    MIN(overall)       AS min_overall,
    MAX(overall)       AS max_overall
FROM rq2_qualitative_evaluations
WHERE evaluation_type = 'g_eval';

-- Distribution of evaluation scores (bins: [1,2), [2,3), [3,4), [4,5])
SELECT 'accuracy' AS campo,
    CASE
        WHEN accuracy >= 1 AND accuracy < 2 THEN '1.00 ≤ x < 2.00'
        WHEN accuracy >= 2 AND accuracy < 3 THEN '2.00 ≤ x < 3.00'
        WHEN accuracy >= 3 AND accuracy < 4 THEN '3.00 ≤ x < 4.00'
        WHEN accuracy >= 4 AND accuracy <= 5 THEN '4.00 ≤ x ≤ 5.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_qualitative_evaluations
WHERE evaluation_type = 'g_eval'
GROUP BY range

UNION ALL

SELECT 'completeness' AS campo,
    CASE
        WHEN completeness >= 1 AND completeness < 2 THEN '1.00 ≤ x < 2.00'
        WHEN completeness >= 2 AND completeness < 3 THEN '2.00 ≤ x < 3.00'
        WHEN completeness >= 3 AND completeness < 4 THEN '3.00 ≤ x < 4.00'
        WHEN completeness >= 4 AND completeness <= 5 THEN '4.00 ≤ x ≤ 5.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_qualitative_evaluations
WHERE evaluation_type = 'g_eval'
GROUP BY range

UNION ALL

SELECT 'usefulness' AS campo,
    CASE
        WHEN usefulness >= 1 AND usefulness < 2 THEN '1.00 ≤ x < 2.00'
        WHEN usefulness >= 2 AND usefulness < 3 THEN '2.00 ≤ x < 3.00'
        WHEN usefulness >= 3 AND usefulness < 4 THEN '3.00 ≤ x < 4.00'
        WHEN usefulness >= 4 AND usefulness <= 5 THEN '4.00 ≤ x ≤ 5.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_qualitative_evaluations
WHERE evaluation_type = 'g_eval'
GROUP BY range

UNION ALL

SELECT 'readability' AS campo,
    CASE
        WHEN readability >= 1 AND readability < 2 THEN '1.00 ≤ x < 2.00'
        WHEN readability >= 2 AND readability < 3 THEN '2.00 ≤ x < 3.00'
        WHEN readability >= 3 AND readability < 4 THEN '3.00 ≤ x < 4.00'
        WHEN readability >= 4 AND readability <= 5 THEN '4.00 ≤ x ≤ 5.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_qualitative_evaluations
WHERE evaluation_type = 'g_eval'
GROUP BY range

UNION ALL

SELECT 'overall' AS campo,
    CASE
        WHEN overall >= 1 AND overall < 2 THEN '1.00 ≤ x < 2.00'
        WHEN overall >= 2 AND overall < 3 THEN '2.00 ≤ x < 3.00'
        WHEN overall >= 3 AND overall < 4 THEN '3.00 ≤ x < 4.00'
        WHEN overall >= 4 AND overall <= 5 THEN '4.00 ≤ x ≤ 5.00'
        ELSE 'out_of_range'
    END AS range,
    COUNT(*) AS valore
FROM rq2_qualitative_evaluations
WHERE evaluation_type = 'g_eval'
GROUP BY range;


-- Distribution of hallucination presence
SELECT
    is_hallucinated,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*)
                              FROM rq2_qualitative_evaluations
                              WHERE evaluation_type = 'g_eval'), 2) AS percentage
FROM rq2_qualitative_evaluations
WHERE evaluation_type = 'g_eval'
GROUP BY is_hallucinated
ORDER BY total DESC;