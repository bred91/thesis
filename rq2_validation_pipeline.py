from utils.sqlite_utils import retrieve_all_rq2_questions_answers
from validation.rq2_g_eval import calculate_save_rq2_g_eval
from validation.rq2_quantitative import calculate_save_rq2_quantitative_evaluation


def main():
    # Load questions and answers from the SQLite database
    questions_answers = retrieve_all_rq2_questions_answers()

    # RQ2: Validate the quality of the answers to the questions, the tool usage and the document retrieval
    calculate_save_rq2_quantitative_evaluation(questions_answers, with_bert=True)

    calculate_save_rq2_g_eval(questions_answers)


if __name__ == "__main__":
    main()
