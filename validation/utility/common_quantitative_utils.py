import evaluate

# Metrics
rouge = evaluate.load('rouge')
bleu = evaluate.load('bleu')
meteor = evaluate.load('meteor')
bert_score = evaluate.load('bertscore')

def compute_detailed_scores(predictions_list, references_list, with_bert: bool = False):
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