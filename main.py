import os

# Monkeypatch CrewAI cache_breakpoint bug for Groq
try:
    import crewai.llms.cache as _crewai_cache
    _crewai_cache.mark_cache_breakpoint = lambda msg: msg
except ImportError:
    pass

from crewai import Crew, Process
from decouple import config
from textwrap import dedent

from agents import ContentCreationAgents
from tasks import ContentCreationTasks

# Setup environment variables - ensure they are loaded
os.environ["GROQ_API_KEY"] = config("GROQ_API_KEY", default="")

class ContentCreationCrew:
    def __init__(self, topic, agent_configs=None):
        self.topic = topic
        self.agent_configs = agent_configs

    def run(self):
        agents = ContentCreationAgents(agent_configs=self.agent_configs)
        tasks = ContentCreationTasks()

        # Initialize Agents
        researcher = agents.researcher_agent()
        planner = agents.planner_agent()
        writer = agents.writer_agent()
        reviewer = agents.reviewer_agent()

        # Initialize Tasks
        research_task = tasks.research_task(researcher, self.topic)
        planning_task = tasks.planning_task(planner)
        writing_task = tasks.writing_task(writer)
        review_task = tasks.review_task(reviewer)

        # Form the Crew (Sequential processing)
        crew = Crew(
            agents=[researcher, planner, writer, reviewer],
            tasks=[research_task, planning_task, writing_task, review_task],
            verbose=True,
            process=Process.sequential
        )

        print(f"\n[INFO] Kicking off the Crew for topic: '{self.topic}'\n")
        result = crew.kickoff()
        return result

if __name__ == "__main__":
    import sys
    print("=========================================")
    print("Welcome to the Content Creation Crew")
    print("=========================================")
    
    if len(sys.argv) > 1:
        topic_input = " ".join(sys.argv[1:])
    else:
        topic_input = "Artificial Intelligence in Healthcare"
        
    print(f"Using topic: {topic_input}")

    crew_runner = ContentCreationCrew(topic_input)
    final_result = crew_runner.run()

    print("\n\n=========================================")
    print("FINAL CONTENT:")
    print("=========================================\n")
    print(final_result)
