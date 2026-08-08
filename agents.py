from crewai import Agent, LLM
from textwrap import dedent
from tools import ImageSearchTool, WebSearchTool, WebsiteScraperTool

class ContentCreationAgents:
    def __init__(self, agent_configs=None):
        # Using a modern supported Groq model. 
        # Token limits are now managed by our custom truncation tools.
        self.llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.7)
        self.configs = agent_configs or {}

    def _get_config(self, key, default_role, default_backstory):
        c = self.configs.get(key, {})
        return {
            "role": c.get("role", default_role),
            "backstory": dedent(c.get("backstory", default_backstory))
        }

    def researcher_agent(self):
        cfg = self._get_config("researcher", 
            "Senior Content Researcher", 
            """You are a world-class researcher, able to find precise, accurate, 
            and up-to-date information on any given topic. You have a keen eye for facts and data.""")
            
        return Agent(
            role=cfg["role"],
            backstory=cfg["backstory"],
            goal="Gather comprehensive, accurate, and relevant information on the provided topic.",
            tools=[WebSearchTool(), WebsiteScraperTool()],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

    def planner_agent(self):
        cfg = self._get_config("planner",
            "Content Strategist & Planner",
            """You are a highly analytical Content Strategist. You excel at taking raw research 
            and structuring it into a logical, compelling narrative outline.""")
            
        return Agent(
            role=cfg["role"],
            backstory=cfg["backstory"],
            goal="Create a detailed, structured outline for the content based on the provided research.",
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

    def writer_agent(self):
        cfg = self._get_config("writer",
            "Senior Writer",
            """You are a masterful writer, capable of creating engaging, insightful, and 
            well-crafted content. You take an outline and facts and weave them into a polished draft. 
            You use the ImageSearchTool to find REAL images and embed them directly into the report 
            using Markdown syntax (e.g., ![alt text](url)). Never use fake placeholders.""")
            
        return Agent(
            role=cfg["role"],
            backstory=cfg["backstory"],
            goal="Write a full, engaging draft based on the strategist's outline and the researcher's facts.",
            tools=[ImageSearchTool()],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

    def reviewer_agent(self):
        cfg = self._get_config("reviewer",
            "Expert Editor and Reviewer",
            """You are a meticulous editor with an eye for detail. You ensure that the content 
            flows well, is grammatically correct, maintains the right tone, and accurately reflects the research.""")
            
        return Agent(
            role=cfg["role"],
            backstory=cfg["backstory"],
            goal="Review and polish the written draft into a final, production-ready document.",
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
