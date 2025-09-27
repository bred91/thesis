import evaluate
import numpy as np

# TODO
from utils.entities import DetailedRq2QuantitativeResults, QuestionAnswer
from utils.sqlite_utils import save_r2_quantitative_results
from validation.utility.common_quantitative_utils import compute_detailed_scores, rouge, bleu, meteor


def calculate_save_rq2_quantitative_evaluation(answers: list[QuestionAnswer], with_bert: bool = False) -> None:
    # Calculation of the various text metrics (ROUGE, BLEU, METEOR, BERTScore)
    bert_precision_avg = bert_recall_avg = bert_f1_avg = None

    predictions = [a.answer_expected for a in answers]
    references = [a.answer for a in answers]

    # Aggregate Scores
    rouge_results, bleu_results, meteor_results = compute_aggregated_scores(
        predictions, references
    )
    # note: Bert already returns details -> for aggregation it is done manually below

    # Detailed Scores
    rouge_results_details, bleu_results_details, meteor_results_details, bert_score_results_details = compute_detailed_scores(
        predictions, references, with_bert
    )

    detailed_results = []

    for i, ans in enumerate(answers):
        append_detailed_results(
            detailed_results=detailed_results,
            question_id=ans.question_id,
            answer_id=ans.answer_id,
            rouge_1_result=rouge_results_details["rouge1"][i],
            rouge_2_result=rouge_results_details["rouge2"][i],
            rouge_l_result=rouge_results_details["rougeL"][i],
            bleu_result=bleu_results_details[i],
            meteor_result=meteor_results_details[i],
            bert_precision=bert_score_results_details["precision"][i] if with_bert else None,
            bert_recall=bert_score_results_details["recall"][i] if with_bert else None,
            bert_f1=bert_score_results_details["f1"][i] if with_bert else None,
        )

    print("<---- Saving RQ2 evaluations --->")
    save_r2_quantitative_results(detailed_results)

    print("<-------- RQ2 Quantitative Evaluation (reference-based) -------->")
    if with_bert:
        bert_precision_avg = float(np.mean(bert_score_results_details["precision"]))
        bert_recall_avg = float(np.mean(bert_score_results_details["recall"]))
        bert_f1_avg = float(np.mean(bert_score_results_details["f1"]))

    print("Answers (overall):")
    print(f"ROUGE-1  {rouge_results['rouge1']:.4f}  \n"
          f"ROUGE-2  {rouge_results['rouge2']:.4f}  \n"
          f"ROUGE-L  {rouge_results['rougeL']:.4f}")
    print(f"BLEU     {bleu_results['bleu']:.4f}")
    print(f"METEOR   {meteor_results['meteor']:.4f}")
    if with_bert:
        print(f"BERT P/R/F1 (avg)  {bert_precision_avg:.4f} / {bert_recall_avg:.4f} / {bert_f1_avg:.4f}")
    print("<-------------------- Done -------------------->")


def compute_aggregated_scores(predictions_list, references_list):
    rouge_results = rouge.compute(predictions=predictions_list, references=references_list, use_aggregator=True)
    bleu_results = bleu.compute(predictions=predictions_list, references=[[r] for r in references_list])
    meteor_results = meteor.compute(predictions=predictions_list, references=references_list)
    return rouge_results, bleu_results, meteor_results


def append_detailed_results(detailed_results, question_id, answer_id, rouge_1_result, rouge_2_result, rouge_l_result,
                            bleu_result,
                            meteor_result, bert_precision=None, bert_recall=None, bert_f1=None):
    detailed_results.append(
        DetailedRq2QuantitativeResults(
            question_id=question_id,
            answer_id=answer_id,
            rouge_1=rouge_1_result,
            rouge_2=rouge_2_result,
            rouge_l=rouge_l_result,
            bleu=bleu_result,
            meteor=meteor_result,
            bert_precision=bert_precision,
            bert_recall=bert_recall,
            bert_f1=bert_f1,
        )
    )
