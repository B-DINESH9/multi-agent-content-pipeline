from crewai import Task
from textwrap import dedent

class ContentCreationTasks:
    def research_task(self, agent, topic):
        return Task(
            description=dedent(f"""
                Conduct deep research on the following topic: "{topic}".
                Find key facts, statistics, recent developments, and expert opinions.
                Ensure the information is accurate and from reliable sources.
                Compile a comprehensive report of your findings.
            """),
            expected_output="A comprehensive research report with key facts, statistics, and references.",
            agent=agent,
        )

    def planning_task(self, agent):
        return Task(
            description=dedent("""
                Review the research report provided by the Researcher.
                Create a detailed outline for an article or document based on this research.
                Include an introduction, logical sections, and a conclusion.
                Specify what information should go into each section.
            """),
            expected_output="A detailed, logical outline with sections and bullet points of what to cover.",
            agent=agent,
        )

    def writing_task(self, agent):
        return Task(
            description=dedent("""
                Using the outline provided by the Planner and the facts from the Researcher, write a full draft.
                Ensure the tone is professional, engaging, and authoritative.
                Do not invent facts; rely strictly on the research provided.
                Write the content in markdown format.
            """),
            expected_output="A complete, well-written draft in markdown format.",
            agent=agent,
        )

    def review_task(self, agent):
        return Task(
            description=dedent("""
                Review the full draft produced by the Writer.
                Check for flow, clarity, tone consistency, and grammatical errors.
                Ensure it accurately reflects the original research and follows the planned outline.
                Make necessary edits to polish it into a final, production-ready piece.
            """),
            expected_output="The final, polished markdown document, ready for publication.",
            agent=agent,
        )
