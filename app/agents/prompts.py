from langchain_core.prompts import ChatPromptTemplate


planner_prompt = ChatPromptTemplate.from_template(
    """
        You are a research planning agent.

        Create a clear research plan for this question:

        {query}

        The plan should include:
        1. What needs to be understood
        2. What information should be searched on the web
        3. What information should be checked from uploaded documents
        4. How the findings should be combined
        5. What should be verified before the final answer

        Return only the research plan.
        """
    )


research_prompt = ChatPromptTemplate.from_template(
    """
        You are an AI research assistant.

        Research Question:
        {query}

        Research Plan:
        {plan}

        Web Research:
        {web_results}

        Uploaded Document Research:
        {rag_results}

        Using the available research information, generate a clear and accurate answer.

        Rules:
        - Use the provided research information.
        - Do not invent facts.
        - If the available information is insufficient, clearly say so.
        - Keep the answer concise and useful.
        """
    )


verification_prompt = ChatPromptTemplate.from_template(
    """
        You are a research verification agent.

        Research Question:
        {query}

        Generated Answer:
        {final_answer}

        Available Web Evidence:
        {web_results}

        Available Document Evidence:
        {rag_results}

        Check whether the generated answer is properly supported by the available evidence.

        Return ONLY valid JSON in this format:

        {{
            "verified": true,
            "reason": "short explanation"
        }}

        Set "verified" to false if the answer contains unsupported or unreliable information.
        """
    )