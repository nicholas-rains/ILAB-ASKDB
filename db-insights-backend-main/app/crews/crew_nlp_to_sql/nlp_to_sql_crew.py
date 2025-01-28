from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from app.models.sql_qa_report import SQLQAResponse
from app.models.sql_response import SQLResponse
from app.tools.sql_tools import ExecuteSQLTool
from app.tools.sql_qa_tool import SQLQATool  # Import the SQL QA Tool
from app.config.dependencies import get_llm

custom_llm = get_llm()

@CrewBase
class NlpToSqlCrew:
    """NLP To SQL Crew"""
    # agents_config = "config/agents.yaml"
    #
    # tasks_config = "config/tasks.yaml"

    # @property
    # def agents_config(self):
    #     config1  = yaml.safe_load(open("app/config/agents.yaml"))
    #     print(type(config1))
    #     return {**config1}
    #
    # @property
    # def tasks_config(self):
    #     config1  = yaml.safe_load(open("app/config/tasks.yaml"))
    #     return {**config1}

    @agent
    def rewriter(self) -> Agent:
        return Agent(
            config=self.agents_config["rewriter"],
            verbose=True,
            llm=custom_llm,
            allow_delegation=False,
            max_iter=4,
        )

    @agent
    def sql_writer(self) -> Agent:
        # Instantiate the ExecuteSQLTool
        execute_sql_tool = ExecuteSQLTool()

        return Agent(
            config=self.agents_config["sql_writer"],
            verbose=True,
            llm=custom_llm,
            tools=[execute_sql_tool],  # Pass the tool as an instance of BaseTool
            allow_delegation=False,
            max_iter=4,
        )

    @agent
    def sql_qa(self) -> Agent:
        # Instantiate the SQLQATool
        sql_qa_tool = SQLQATool(llm=custom_llm)  # Pass the LLM instance

        return Agent(
            config=self.agents_config["sql_qa"],
            verbose=True,
            llm=custom_llm,
            tools=[sql_qa_tool],  # Include the QA tool
            allow_delegation=False,
            max_iter=3,
        )

    @task
    def rewrite_task(self) -> Task:
        return Task(
            config=self.tasks_config["rewrite_query_task"],
            agent=self.rewriter(),
            output_file="app/data/responses/rewritten_query.txt",
        )

    @task
    def sql_query_task(self) -> Task:
        return Task(
            config=self.tasks_config["sql_query_task"],
            agent=self.sql_writer(),
            output_file="app/data/responses/generated_sql.json",
            output_json=SQLResponse
        )

    @task
    def sql_qa_task(self) -> Task:
        return Task(
            config=self.tasks_config["sql_qa_task"],
            agent=self.sql_qa(),
            output_file="app/data/responses/sql_qa_report.json",
            output_json=SQLQAResponse
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DB-insights crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=[
                self.rewrite_task(),  # First task: rewrite the query
                self.sql_query_task(),  # Second task: generate and execute SQL
                self.sql_qa_task(),  # Third task: QA check
            ],
            process=Process.sequential,  # Running tasks one after the other
            verbose=True,
        )
