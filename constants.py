from enum import Enum
from typing import Dict

class NodeTypes(str, Enum):
    GENERATE = "generate_solutions"
    EVALUATE = "evaluate_solution"
    DEEPEN = "deepen_thought"
    RANK = "rank_solutions"

class JsonFields(str, Enum):
    SOLUTIONS = "solutions"
    REVIEW = "review"
    DEEP_THOUGHT = "deep_thought"
    RANKED_SOLUTIONS = "ranked_solutions"

MODEL_SETTINGS = {
    "name": "llama-3.2-1b-preview",
    "temperature": 0.7,
    "max_tokens": 1024
}


PROMPTS = {
    "step1": {
        "template": "Generate three comprehensive solutions for this problem: {input}\nConsider these critical factors in detail: {considerations}\n\nFor each solution, address:\n- Technical implementation\n- Resource requirements\n- Timeline and milestones\n- Potential risks and mitigations\n- Expected outcomes\n\nRespond in JSON format with an array of three solutions.",
        "variables": ["input", "considerations"]
    },
    "step2": {
        "template": "Evaluate this solution: {solutions}\n\nProvide a detailed assessment covering:\n- Technical feasibility\n- Cost-benefit analysis\n- Implementation challenges\n- Resource requirements\n- Risk assessment\n- Success metrics\n\nRespond in JSON format with a detailed review.",
        "variables": ["solutions"]
    },
    "step3": {
        "template": "Analyze this review in depth: {review}\n\nFocus your analysis on:\n- Long-term sustainability\n- Scalability potential\n- Resource optimization\n- Strategic alignment\n- Market impact\n- Future adaptability\n\nRespond in JSON format with your deep analysis.",
        "variables": ["review"]
    },
    "step4": {
        "template": "Rank and justify based on this analysis: {deepen_thought_process}\n\nConsider these ranking criteria:\n- Overall effectiveness\n- Implementation feasibility\n- Cost efficiency\n- Risk level\n- Long-term value\n- Strategic fit\n\nRespond in JSON format with your ranking and justification.",
        "variables": ["deepen_thought_process"]
    }
}
