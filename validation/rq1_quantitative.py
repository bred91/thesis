import evaluate
import numpy as np

from utils.entities import DetailedRq1QuantitativeResults, Summary
from utils.enums import SummaryType
from utils.sqlite_utils import save_r1_quantitative_results

# Metrics
rouge = evaluate.load('rouge')
bleu = evaluate.load('bleu')
meteor = evaluate.load('meteor')
bert_score = evaluate.load('bertscore')

def calculate_save_rq1_quantitative_evaluation(summaries: list[Summary], references: dict[str,list], with_bert: bool = False) -> None:

    # Calculation of the various text summarization metrics (ROUGE, BLEU, METEOR, BERTScore)
    general_bert_precision = general_bert_recall = general_bert_f1 \
        = technical_bert_precision = technical_bert_recall = technical_bert_f1 = None

    general_predictions = [s.llama_summary for s in summaries]
    technical_predictions = [s.llama_tech_summary for s in summaries]

    # Aggregate Scores
    # general
    general_rouge_results, general_bleu_results, general_meteor_results = compute_aggregated_scores(
        general_predictions, references[SummaryType.GENERAL.value]
    )
    # technical
    technical_rouge_results, technical_bleu_results, technical_meteor_results = compute_aggregated_scores(
        technical_predictions, references[SummaryType.TECHNICAL.value]
    )
    # note: Bert already returns details -> for aggregation it is done manually below

    # Detailed Scores
    # general
    general_rouge_results_details, general_bleu_results_details, general_meteor_results_details, \
        general_bert_score_results_details = compute_detailed_scores(
            general_predictions, references[SummaryType.GENERAL.value], with_bert
        )
    # technical
    technical_rouge_results_details, technical_bleu_results_details, technical_meteor_results_details, \
        technical_bert_score_results_details = compute_detailed_scores(
            technical_predictions, references[SummaryType.TECHNICAL.value], with_bert
        )

    detailed_results = []

    for i, summary in enumerate(summaries):
        append_detailed_results(
            detailed_results=detailed_results,
            commit_id=summary.commit_id,
            summary_type=SummaryType.GENERAL.value,
            rouge_1_result=general_rouge_results_details["rouge1"][i],
            rouge_2_result=general_rouge_results_details["rouge2"][i],
            rouge_l_result=general_rouge_results_details["rougeL"][i],
            bleu_result=general_bleu_results_details[i],
            meteor_result=general_meteor_results_details[i],
            bert_precision=general_bert_score_results_details["precision"][i] if with_bert else None,
            bert_recall=general_bert_score_results_details["recall"][i] if with_bert else None,
            bert_f1=general_bert_score_results_details["f1"][i] if with_bert else None,
        )
        append_detailed_results(
            detailed_results=detailed_results,
            commit_id=summary.commit_id,
            summary_type=SummaryType.TECHNICAL.value,
            rouge_1_result=technical_rouge_results_details["rouge1"][i],
            rouge_2_result=technical_rouge_results_details["rouge2"][i],
            rouge_l_result=technical_rouge_results_details["rougeL"][i],
            bleu_result=technical_bleu_results_details[i],
            meteor_result=technical_meteor_results_details[i],
            bert_precision=technical_bert_score_results_details["precision"][i] if with_bert else None,
            bert_recall=technical_bert_score_results_details["recall"][i] if with_bert else None,
            bert_f1=technical_bert_score_results_details["f1"][i] if with_bert else None,
        )

    print("<---- Saving evaluations --->")
    save_r1_quantitative_results(detailed_results)

    print("<-------- RQ1 Quantitative Evaluation -------->")
    if with_bert:
        general_bert_precision = float(np.mean(general_bert_score_results_details["precision"]))
        general_bert_recall = float(np.mean(general_bert_score_results_details["recall"]))
        general_bert_f1 = float(np.mean(general_bert_score_results_details["f1"]))
        technical_bert_precision = float(np.mean(technical_bert_score_results_details["precision"]))
        technical_bert_recall = float(np.mean(technical_bert_score_results_details["recall"]))
        technical_bert_f1 = float(np.mean(technical_bert_score_results_details["f1"]))

    print(f"General Summary results:")
    print(f"ROUGE-1  {general_rouge_results['rouge1']:.4f}  \n"
          f"ROUGE-2  {general_rouge_results['rouge2']:.4f}  \n"
          f"ROUGE-L  {general_rouge_results['rougeL']:.4f}")
    print(f"BLEU     {general_bleu_results['bleu']:.4f}")
    print(f"METEOR   {general_meteor_results['meteor']:.4f}")
    if with_bert:
        print(f"BERT P/R/F1 (avg)  {general_bert_precision:.4f} / {general_bert_recall:.4f} / {general_bert_f1:.4f}")


    print(f"Technical Summary results:")
    print(f"ROUGE-1  {technical_rouge_results['rouge1']:.4f}  \n"
          f"ROUGE-2  {technical_rouge_results['rouge2']:.4f}  \n"
          f"ROUGE-L  {technical_rouge_results['rougeL']:.4f}")
    print(f"BLEU     {technical_bleu_results['bleu']:.4f}")
    print(f"METEOR   {technical_meteor_results['meteor']:.4f}")
    if with_bert:
        print(f"BERT P/R/F1 (avg)  {technical_bert_precision:.4f} / {technical_bert_recall:.4f} / {technical_bert_f1:.4f}")
    print("<-------------------- Done -------------------->")



def compute_aggregated_scores(predictions_list, references_list):
    rouge_results = rouge.compute(predictions=predictions_list, references=references_list, use_aggregator=True)
    bleu_results = bleu.compute(predictions=predictions_list, references=[[r] for r in references_list])
    meteor_results = meteor.compute(predictions=predictions_list, references=references_list)
    return rouge_results, bleu_results, meteor_results

def compute_detailed_scores(predictions_list, references_list, with_bert = False):
    rouge_results_details = rouge.compute(predictions=predictions_list, references=references_list, use_aggregator=False)
    bleu_results_details = [
        bleu.compute(predictions=[p], references=[[r]])["bleu"]
        for p, r in zip(predictions_list, references_list)
    ]
    meteor_results_details = [
        meteor.compute(predictions=[p], references=[r])["meteor"]
        for p, r in zip(predictions_list, references_list)
    ]
    if with_bert:
        bert_score_results_details = bert_score.compute(predictions=predictions_list, references=references_list, lang="en")
        return rouge_results_details, bleu_results_details, meteor_results_details, bert_score_results_details
    else:
        return rouge_results_details, bleu_results_details, meteor_results_details, None

def append_detailed_results(detailed_results, commit_id, summary_type, rouge_1_result, rouge_2_result, rouge_l_result, bleu_result,
                            meteor_result, bert_precision=None, bert_recall=None, bert_f1=None):
    detailed_results.append(
        DetailedRq1QuantitativeResults(
            commit_id=commit_id,
            summary_type=summary_type,
            rouge_1=rouge_1_result,
            rouge_2=rouge_2_result,
            rouge_l=rouge_l_result,
            bleu=bleu_result,
            meteor=meteor_result,
            bert_precision= bert_precision,
            bert_recall=bert_recall,
            bert_f1=bert_f1,
        )
    )