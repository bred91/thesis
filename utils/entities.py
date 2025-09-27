from typing import Optional

from pydantic import BaseModel, Field


class DetailedRq1QuantitativeResults:
    def __init__(self, commit_id, summary_type, rouge_1, rouge_2, rouge_l, bleu, meteor, bert_precision, bert_recall, bert_f1):
        self.commit_id = commit_id
        self.summary_type = summary_type
        self.rouge_1 = rouge_1
        self.rouge_2 = rouge_2
        self.rouge_L = rouge_l
        self.bleu = bleu
        self.meteor = meteor
        self.bert_precision = bert_precision
        self.bert_recall = bert_recall
        self.bert_f1 = bert_f1

    def __repr__(self):
        return (f"DetailedRq1QuantitativeResults("
                f"commit_id={self.commit_id}, summary_type={self.summary_type}, "
                f"rouge_1={self.rouge_1}, "
                f"rouge_2={self.rouge_2}, rouge_L={self.rouge_L}, "
                f"bleu={self.bleu}, meteor={self.meteor}, "
                f"bert_precision={self.bert_precision}, "
                f"bert_recall={self.bert_recall}, bert_f1={self.bert_f1})")


class Summary:
    """Class representing a commit and its associated summaries and related information."""

    def __init__(
        self,
        summary_id,
        commit_id,
        experiment_name,
        date,
        llama_category,
        llama_summary,
        llama_summary_retrieved_docs,
        llama_summary_retrieved_docs_count,
        llama_summary_retrieved_docs_scores,
        llama_tech_summary,
        llama_tech_summary_retrieved_docs,
        llama_tech_summary_retrieved_docs_count,
        llama_tech_summary_retrieved_docs_scores
    ):
        self.id = summary_id
        self.commit_id = commit_id
        self.experiment_name = experiment_name
        self.date = date
        self.llama_category = llama_category
        self.llama_summary = llama_summary
        self.llama_summary_retrieved_docs = llama_summary_retrieved_docs
        self.llama_summary_retrieved_docs_count = llama_summary_retrieved_docs_count
        self.llama_summary_retrieved_docs_scores = llama_summary_retrieved_docs_scores
        self.llama_tech_summary = llama_tech_summary
        self.llama_tech_summary_retrieved_docs = llama_tech_summary_retrieved_docs
        self.llama_tech_summary_retrieved_docs_count = llama_tech_summary_retrieved_docs_count
        self.llama_tech_summary_retrieved_docs_scores = llama_tech_summary_retrieved_docs_scores

    def __repr__(self):
        return f"Summary(id={self.id}, commit_id={self.commit_id}, experiment_name={self.experiment_name}, date={self.date}, llama_category={self.llama_category})"

class Commit:
    def __init__(self, commit_id, commit_hash, author, date, message, files, diffs):
        self.id = commit_id
        self.commit_hash = commit_hash
        self.author = author
        self.date = date
        self.message = message
        self.files = files
        self.diffs = diffs

    def __repr__(self):
        return f"Commit(id={self.id}, commit_hash={self.commit_hash}, author={self.author}, date={self.date}, message={self.message})"


class DetailedRq1Score(BaseModel):
    accuracy: int = Field(
        ge=1, le=5,
        description=(
            "Accuracy: Does the summary faithfully describe the actual code changes?"
        )
    )
    completeness: int = Field(
        ge=1, le=5,
        description=(
            "Completeness: Does the summary include all relevant aspects of the commit?"
        )
    )
    usefulness: int = Field(
        ge=1, le=5,
        description=(
            "Usefulness: Can a developer act on this information during review or maintenance?"
        )
    )
    readability: int = Field(
        ge=1, le=5,
        description=(
            "Readability: Is the text clear and concise, free of jargon or redundancy?"
        )
    )
    technical_depth: Optional[int] = Field(
        default=None, ge=1, le=5,
        description=(
            "Technical depth: Level of meaningful technical detail (APIs, data structures, algorithms)."
        )
    )
    justification: Optional[str] = Field(
        description="Brief rationale for the scores given."
    )


class QuestionAnswer:
    def __init__(self, question_id: int, question: str, answer_id: int, answer: str,
                 answer_expected: str, tool_called: str, tool_expected: str,
                 docs_retrieved: str, docs_expected: str,
                 debug_text: str):
        self.question_id = question_id
        self.question = question
        self.answer_id = answer_id
        self.answer = answer
        self.answer_expected = answer_expected
        self.tool_called = tool_called
        self.tool_expected = tool_expected
        self.docs_retrieved = docs_retrieved
        self.docs_expected = docs_expected
        self.debug_text = debug_text

    def __repr__(self):
        return f"QuestionAnswer(question_id={self.question_id}, answer_id={self.answer_id})"


class DetailedRq2Score(BaseModel):
    accuracy: int = Field(
        ge=1, le=5,
        description=(
            "Accuracy: Does the summary faithfully describe the actual code changes?"
        )
    )
    completeness: int = Field(
        ge=1, le=5,
        description=(
            "Completeness: Does the summary include all relevant aspects of the commit?"
        )
    )
    usefulness: int = Field(
        ge=1, le=5,
        description=(
            "Usefulness: Can a developer act on this information during review or maintenance?"
        )
    )
    readability: int = Field(
        ge=1, le=5,
        description=(
            "Readability: Is the text clear and concise, free of jargon or redundancy?"
        )
    )
    is_hallucinated: str = Field(
        pattern=r'^(YES|NO|PARTIALLY)$',
        description=(
            "Hallucination: Does the answer contain information not supported by the provided context?"
        )
    )
    justification: Optional[str] = Field(
        default=None,
        description="Brief rationale for the scores given."
    )


class DetailedRq2QuantitativeResults:
    def __init__(self, question_id, answer_id, rouge_1, rouge_2, rouge_l, bleu, meteor, bert_precision, bert_recall, bert_f1):
        self.question_id = question_id
        self.answer_id = answer_id
        self.rouge_1 = rouge_1
        self.rouge_2 = rouge_2
        self.rouge_L = rouge_l
        self.bleu = bleu
        self.meteor = meteor
        self.bert_precision = bert_precision
        self.bert_recall = bert_recall
        self.bert_f1 = bert_f1

    def __repr__(self):
        return (f"DetailedRq2QuantitativeResults("
                f"question_id={self.question_id}, answer_id={self.answer_id}, "
                f"rouge_1={self.rouge_1}, "
                f"rouge_2={self.rouge_2}, rouge_L={self.rouge_L}, "
                f"bleu={self.bleu}, meteor={self.meteor}, "
                f"bert_precision={self.bert_precision}, "
                f"bert_recall={self.bert_recall}, bert_f1={self.bert_f1})")