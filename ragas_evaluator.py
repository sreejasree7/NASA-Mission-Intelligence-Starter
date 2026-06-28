from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from typing import Dict, List, Optional

# RAGAS imports
try:
    from ragas import SingleTurnSample
    from ragas.metrics import BleuScore, NonLLMContextPrecisionWithReference, ResponseRelevancy, Faithfulness, RougeScore
    from ragas import evaluate
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

def evaluate_response_quality(question: str, answer: str, contexts: List[str]) -> Dict[str, float]:
    """Evaluate response quality using RAGAS metrics"""
    if not RAGAS_AVAILABLE:
        return {"error": "RAGAS not available"}
    
    # TODO: Create evaluator LLM with model gpt-3.5-turbo
    # TODO: Create evaluator_embeddings with model test-embedding-3-small
    # TODO: Define an instance for each metric to evaluate
    # TODO: Evaluate the response using the metrics
    # TODO: Return the evaluation results

    """Evaluate response quality using RAGAS."""

    if not RAGAS_AVAILABLE:
        return {"error": "RAGAS not available"}

    try:

        # Create evaluator LLM
        evaluator_llm = LangchainLLMWrapper(
            ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0
            )
        )

        # Create embedding model
        evaluator_embeddings = LangchainEmbeddingsWrapper(
            OpenAIEmbeddings(
                model="text-embedding-3-small"
            )
        )

        # Build evaluation sample
        sample = SingleTurnSample(
            user_input=question,
            response=answer,
            retrieved_contexts=contexts
        )

        metrics = [
            ResponseRelevancy(),
            Faithfulness(),
            BleuScore(),
            RougeScore(),
        ]

        results = evaluate(
            dataset=[sample],
            metrics=metrics,
            llm=evaluator_llm,
            embeddings=evaluator_embeddings
        )

        scores = {}

        for metric in metrics:
            name = metric.__class__.__name__
            scores[name] = float(results[name][0])

        return scores

    except Exception as e:
        return {
            "error": str(e)
        }
