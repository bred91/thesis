from statistics import mean
from time import sleep

from google import genai
from google.genai import types
from pydantic import ValidationError

from utils.config import SEED
from utils.entities import Summary, Commit, DetailedRq1Score
from utils.enums import SummaryType
from utils.sqlite_utils import save_rq1_g_evals

client = genai.Client()


def calculate_save_rq1_g_eval(summaries: list[Summary], commits: list[Commit]) -> None:
    print("<-------- RQ1 GEval -------->")
    general_summaries_evaluations = []
    tech_summaries_evaluations = []

    for idx, summary in enumerate(summaries):
        commit_id = summary.commit_id
        commit_message = commits[idx].message
        commit_diffs = commits[idx].diffs
        generated_summary = summary.llama_summary
        generated_tech_summary = summary.llama_tech_summary
        general_summary_evaluation(commit_diffs, commit_id, commit_message, general_summaries_evaluations,
                                   generated_summary)
        tech_summary_evaluation(commit_diffs, commit_id, commit_message, tech_summaries_evaluations,
                                generated_tech_summary)

    print("<---- Saving evaluations --->")
    save_rq1_g_evals(general_summaries_evaluations + tech_summaries_evaluations)
    print("<----------- End ----------->")


def general_summary_evaluation(commit_diffs, commit_id, commit_message, general_summaries_evaluations,
                               generated_summary):
    prompt = f"""
        You are an expert code reviewer.
    
        Commit ID: {commit_id}
    
        Original commit message:
        \"\"\"{commit_message}\"\"\"
    
        Diffs:
        \"\"\"{commit_diffs}\"\"\"
    
        Generated summary:
        \"\"\"{generated_summary}\"\"\"
    
        Evaluate the generated summary on the following rubric (1 = poor, 5 = excellent):
    
        - accuracy        : Does the summary faithfully describe the actual code changes?
        - completeness    : Does the summary include all relevant aspects of the commit?
        - usefulness      : Can a developer act on this information during review or maintenance?
        - readability     : Is the text clear and concise, free of jargon or redundancy? 
    
        For each dimension, give an integer 1‑5.  
        Add a short justification explaining the main strengths or weaknesses (≤ 60 words).
    
        **Return one JSON object with exactly these keys:**  
        `accuracy`, `completeness`, `usefulness`, `readability`, `justification`.
    
        Do NOT output anything else.
    """

    response = generate_response(prompt)
    # review = response.text
    append_evaluation(commit_id, general_summaries_evaluations, response, SummaryType.GENERAL)


def tech_summary_evaluation(commit_diffs, commit_id, commit_message, tech_summaries_evaluations,
                               generated_tech_summary):
    prompt = f"""
        You are an expert code reviewer.
    
        Commit ID: {commit_id}
    
        Original commit message:
        \"\"\"{commit_message}\"\"\"
    
        Diffs (+ means removed, - means added):
        \"\"\"{commit_diffs}\"\"\"
    
        Generated technical summary:
        \"\"\"{generated_tech_summary}\"\"\"
    
        Evaluate the generated technical summary on the following rubric (1 = poor, 5 = excellent):
    
        - accuracy        : Does the summary faithfully describe the actual code changes?
        - completeness    : Does the summary include all relevant aspects of the commit?
        - usefulness      : Can a developer act on this information during review or maintenance?
        - readability     : Is the text clear and concise, free of jargon or redundancy?
        - technical_depth : Level of meaningful technical detail (APIs, data structures, algorithms).
 
    
        For each dimension, give an integer 1‑5.  
        Add a short justification explaining the main strengths or weaknesses (≤ 60 words).
    
        **Return one JSON object with exactly these keys:**  
        `accuracy`, `completeness`, `usefulness`, `readability`, `technical_depth`, `justification`.
    
        Do NOT output anything else.
    """

    response = generate_response(prompt)
    # review = response.text
    append_evaluation(commit_id, tech_summaries_evaluations, response, SummaryType.TECHNICAL)


def generate_response(prompt):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_schema=DetailedRq1Score,
            response_mime_type="application/json",
            seed=SEED,
        )
    )


def append_evaluation(commit_id: str, summaries_evaluations: list[dict], response, summary_type: SummaryType) -> None:
    try:
        score = DetailedRq1Score.model_validate_json(response.text)

        # Dimensions and overall score
        dims = [
            ("accuracy", score.accuracy),
            ("completeness", score.completeness),
            ("usefulness", score.usefulness),
            ("readability", score.readability),
        ]
        if summary_type == SummaryType.TECHNICAL and score.technical_depth is not None:
            dims.append(("technical_depth", score.technical_depth))

        overall = mean(v for _, v in dims)

        # ---------- Console log ----------
        # print(f"\nCommit {commit_id}  [{summary_type}]")
        # for name, value in dims:
        #     print(f"  {name:<15}: {value}")
        # print(f"  overall         : {overall:.2f}")
        # print(f"  justification   : {score.justification}\n")

        # ---------- Persist for later analysis ----------
        summaries_evaluations.append({
            "commit_id": commit_id,
            "summary_type": summary_type.value,
            **{name: value for name, value in dims},
            "overall": overall,
            "justification": score.justification,
        })

    except ValidationError as e:
        print(f"Evaluation error — commit {commit_id}: {e}")
        summaries_evaluations.append({
            "commit_id": commit_id,
            "summary_type": summary_type.value,
            "error": "Invalid response format",
            "raw_response": response.text,
        })
