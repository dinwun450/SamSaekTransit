# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from latest_ai_development.tools import custom_tool

@CrewBase
class LatestAiDevelopmentCrew():
  """LatestAiDevelopment crew"""

  agents: List[BaseAgent]
  tasks: List[Task]

  @agent
  def transit_land_departures_agent(self) -> Agent:
      return Agent(
          config=self.agents_config['transit_land_departures_agent'],  # type: ignore[index]
          verbose=True,
          tools=[custom_tool.TransitDeparturesTool(result_as_answer=True)]  # Add the Transit Departures tool here
      )
  
  @task
  def transit_land_departures_task(self) -> Task:
      return Task(
          config=self.tasks_config['transit_land_departures_task'],  # type: ignore[index]
          output_file='output/transit_departures_results.txt'  # This is the file that will contain the results from the Transit Departures tool
      )

  @agent
  def nearby_transit_agent(self) -> Agent:
      return Agent(
          config=self.agents_config['nearby_transit_agent'],  # type: ignore[index]
          verbose=True,
          tools=[custom_tool.NearbyTransitTool(result_as_answer=True)]  # Add the Nearby Transit tool here
      )
  
  @task
  def nearby_transit_task(self) -> Task:
      return Task(
          config=self.tasks_config['nearby_transit_task'],  # type: ignore[index]
          output_file='output/nearby_transit_results.txt'  # This is the file that will contain the results from the Nearby Transit tool
      )

  @agent
  def traffic_data_agent(self) -> Agent:
      return Agent(
          config=self.agents_config['traffic_data_agent'],  # type: ignore[index]
          verbose=True,
          tools=[custom_tool.TrafficDataTool(result_as_answer=True)]  # Add the Traffic Data tool here
      )
  
  @task
  def traffic_data_task(self) -> Task:
      return Task(
          config=self.tasks_config['traffic_data_task'],  # type: ignore[index]
          output_file='output/traffic_data_results.txt'  # This is the file that will contain the results from the Traffic Data tool
      )

  @agent
  def transit_land_agent(self) -> Agent:
      return Agent(
          config=self.agents_config['transit_land_agent'],  # type: ignore[index]
          verbose=True,
          tools=[custom_tool.transitlandAPICaller(result_as_answer=True)]  # Add the custom tool here
      )
  
  @task
  def transit_land_task(self) -> Task:
      return Task(
          config=self.tasks_config['transit_land_task'],  # type: ignore[index]
          output_file='output/transitland_results.txt'  # This is the file that will contain the results from the TransitLand API
      )
  
  @agent
  def transit_agency_search_agent(self) -> Agent:
      return Agent(
          config=self.agents_config['transit_agency_search_agent'],  # type: ignore[index]
          verbose=True,
          tools=[custom_tool.ExaSearchTool(result_as_answer=True)]  # Add the Exa search tool here
      )
  
  @task
  def transit_agency_search_task(self) -> Task:
      return Task(
          config=self.tasks_config['transit_agency_search_task'],  # type: ignore[index]
          output_file='output/transit_agency_search_results.txt'  # This is the file that will contain the results from the Exa search
      )

  @crew
  def crew(self) -> Crew:
    """Creates the LatestAiDevelopment crew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
      process=Process.sequential,  # Use sequential process for the crew
      verbose=True,
    )