import os
import dotenv

from registry.agents.file_access_agent import FileAccessAgent
from registry.agents.python_code_exec_agent import PythonExecAgent
from docker.docker_worker import DockerWorker

dotenv.load_dotenv()

default_model_name = os.getenv("DEFAULT_MODEL_NAME")

print("Composing docker...")
docker_worker = DockerWorker()
docker_worker.compose_up()
print("Docker environment ready.")

prompt = """Use the file traffic_accidents.csv for your analysis. The column names are:
Variable	Description
accidents	Number of recorded accidents, as a positive integer.
traffic_fine_amount	Traffic fine amount, expressed in thousands of USD.
traffic_density	Traffic density index, scale from 0 (low) to 10 (high).
traffic_lights	Proportion of traffic lights in the area (0 to 1).
pavement_quality	Pavement quality, scale from 0 (very poor) to 5 (excellent).
urban_area	Urban area (1) or rural area (0), as an integer.
average_speed	Average speed of vehicles in km/h.
rain_intensity	Rain intensity, scale from 0 (no rain) to 3 (heavy rain).
vehicle_count	Estimated number of vehicles, in thousands, as an integer.
time_of_day	Time of day in 24-hour format (0 to 24).
accidents	traffic_fine_amount
"""

print("Setup: ")
print(prompt)

print("Setting up the agents... ")

# instantiate the agents with the default constructor defined values
# developer may override the default values - prompt, model, logger, and client if needed

# this agent uses qwen2.5-coder by default
file_ingestion_agent = FileAccessAgent()

# let's make sure the agent uses default model
data_analysis_agent = PythonExecAgent(model_name=default_model_name)

print("Understanding the contents of the file...")
# give a task to the file ingestion agent to read the file and provide the context to the data analysis agent
file_ingestion_agent_output = file_ingestion_agent.task(prompt)

# add the file content as context to the data analysis agent
# the context is added to the agent's tool manager so the tool manager can use the context to generate the code

data_analysis_agent.add_context(prompt)
data_analysis_agent.add_context(file_ingestion_agent_output)

while True:
  print("Type your question related to the data in the file. Type 'exit' to exit.")
  user_input = input("Type your question: ")

  if user_input == "exit":
    print("Exiting the application.")
    break

  print(f"User question: {user_input}")

  print("Generating dynamic tools and using code interpreter...")
  data_analysis_agent_output = data_analysis_agent.task(user_input)

  print("Output...")
  print(data_analysis_agent_output)