from statistics import mean
from time import sleep

from google import genai
from google.genai import types
from langchain.chains.openai_functions.citation_fuzzy_match import QuestionAnswer
from pydantic import ValidationError

from utils.config import SEED
from utils.entities import DetailedRq2Score
from utils.sqlite_utils import save_rq2_g_evals

client = genai.Client()


def calculate_save_rq2_g_eval(questions_answers: list[QuestionAnswer]) -> None:
    print("<-------- RQ2 GEval -------->")
    evaluations = []

    for question_answer in questions_answers:
        answer_evaluation(evaluations, question_answer)
        sleep(2)

    print("<---- Saving evaluations --->")
    save_rq2_g_evals(evaluations)
    print("<----------- End ----------->")


def answer_evaluation(evaluations, question_answer: QuestionAnswer):
    question_id = question_answer.question_id
    question_text = question_answer.question
    answer_id = question_answer.answer_id
    answer_text = question_answer.answer
    answer_expected = question_answer.answer_expected
    tool_called = question_answer.tool_called
    tool_expected = question_answer.tool_expected
    docs_retrieved = question_answer.docs_retrieved
    docs_expected = question_answer.docs_expected

    prompt = f"""
            You are an expert code reviewer and QA evaluator for RAG/chatbot systems.
            
            Question (id {question_id}):
            \"\"\"{question_text}\"\"\"
            
            Model answer (answer_id {answer_id}):
            \"\"\"{answer_text}\"\"\"
            
            Expected/Reference answer (if provided):
            \"\"\"{answer_expected or ""}\"\"\"
            
            Tool usage:
            - tool_called      : {tool_called or ""}
            - tool_expected    : {tool_expected or ""}
            
            Document retrieval:
            - docs_retrieved   : {docs_retrieved or ""}
            - docs_expected    : {docs_expected or ""}
            
            Evaluate the given model answer with the following rubric (1 = poor, 5 = excellent):
            
            - accuracy     : Does the answer correctly address the question, consistent with the diffs/docs?
            - completeness : Does it cover the key aspects expected?
            - usefulness   : Would this be helpful to a developer/maintainer?
            - readability  : Clear, concise, and easy to follow?
            
            For each dimension, give an integer 1‑5.  
            Add a short justification explaining the main strengths or weaknesses (≤ 60 words).
            
            Additionally, decide if the answer is hallucinated or not:
            - is_hallucinated : YES, if the answer is completely hallucinated, NO if it is not, PARTIALLY if it contains some medium hallucinated parts. 
                        
            **Return ONE JSON object with EXACTLY these keys:**
            `accuracy`, `completeness`, `usefulness`, `readability`, `justification`, `is_hallucinated`.
            
            Do NOT output anything else.
        """.strip()

    response = generate_response(prompt)
    append_evaluation(answer_id, question_id, evaluations, response)


def append_evaluation(question_id, answer_id, evaluations: list[dict], response):
    try:
        score = DetailedRq2Score.model_validate_json(response.text)

        dims = [
            ("accuracy", score.accuracy),
            ("completeness", score.completeness),
            ("usefulness", score.usefulness),
            ("readability", score.readability),
        ]
        overall_float = mean(v for _, v in dims)
        overall_int = int(round(overall_float))

        evaluations.append({
            "question_id": question_id,
            "answer_id": answer_id,
            "evaluation_type": "g_eval",
            "accuracy": score.accuracy,
            "completeness": score.completeness,
            "usefulness": score.usefulness,
            "readability": score.readability,
            "overall": overall_int,
            "justification": score.justification,
            "is_hallucinated": getattr(score, "is_hallucinated", None),
        })

    except ValidationError as e:
        print(f"Evaluation error — answer_id {answer_id} (q {question_id}): {e}")

        evaluations.append({
            "question_id": question_id,
            "answer_id": answer_id,
            "evaluation_type": "g_eval",
            "accuracy": None,
            "completeness": None,
            "usefulness": None,
            "readability": None,
            "overall": None,
            "justification": "Invalid response format",
        })


def generate_response(prompt):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_schema=DetailedRq2Score,
            response_mime_type="application/json",
            seed=SEED,
        )
    )
