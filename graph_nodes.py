from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from constants import JsonFields, MODEL_SETTINGS, PROMPTS
from utils import safe_json_parse
import os


class GraphNodes:
    def __init__(self):
        self.model = ChatGroq(
            model=MODEL_SETTINGS["name"],
            temperature=MODEL_SETTINGS["temperature"],
            max_tokens=MODEL_SETTINGS["max_tokens"]
        )
        self.prompts = {}
        for k, v in PROMPTS.items():
            self.prompts[k] = PromptTemplate(
                template=v["template"],
                input_variables=v["variables"]
            )

    def generate_solutions(self, state):
        try:
            prompt = self.prompts["step1"].format_prompt(
                input=state["input"],
                considerations=state["considerations"]
            ).to_string()

            response = self.model.invoke(prompt)
            parsed = safe_json_parse(response.content)

            solutions = parsed.get(JsonFields.SOLUTIONS, [response.content])
            if not isinstance(solutions, list):
                solutions = [solutions]

            return {JsonFields.SOLUTIONS: solutions}

        except Exception as e:
            print(f"Error in generate_solutions: {e}")
            return {JsonFields.SOLUTIONS: [str(e)]}

    def evaluate_solution(self, state):
        try:
            prompt = self.prompts["step2"].format_prompt(
                solutions=state["solution"]
            ).to_string()

            response = self.model.invoke(prompt)
            parsed = safe_json_parse(response.content)

            return {"reviews": [parsed.get(JsonFields.REVIEW, response.content)]}

        except Exception as e:
            print(f"Error in evaluate_solution: {e}")
            return {"reviews": [str(e)]}

    def deepen_thought(self, state):
        try:
            prompt = self.prompts["step3"].format_prompt(
                review=state["solution"]
            ).to_string()

            response = self.model.invoke(prompt)
            parsed = safe_json_parse(response.content)

            return {"deep_thoughts": [parsed.get(JsonFields.DEEP_THOUGHT, response.content)]}

        except Exception as e:
            print(f"Error in deepen_thought: {e}")
            return {"deep_thoughts": [str(e)]}

    def rank_solutions(self, state):
        try:
            deep_thoughts = "\n\n".join(state["deep_thoughts"])
            prompt = self.prompts["step4"].format_prompt(
                deepen_thought_process=deep_thoughts
            ).to_string()

            response = self.model.invoke(prompt)
            parsed = safe_json_parse(response.content)

            return {JsonFields.RANKED_SOLUTIONS: parsed.get(JsonFields.RANKED_SOLUTIONS, response.content)}

        except Exception as e:
            print(f"Error in rank_solutions: {e}")
            return {JsonFields.RANKED_SOLUTIONS: str(e)}