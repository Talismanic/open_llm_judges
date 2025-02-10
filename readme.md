# Open LLM Judges

## Overview
Open LLM Judges is a system that evaluates AI-generated outputs using different judging mechanisms. The system provides three predefined archetypes, each with specific rules for handling multiple worker agents.

## Installation & Setup
### Prerequisites
- Docker and Docker Compose installed on your system.
- A valid `GEMINI_API_KEY` for authentication.

### Step 1: Configure Environment Variables
Create a `.env` file in the root directory of the project with the following structure:

```
DEBUG=True
GEMINI_API_KEY=*****
```
Replace `*****` with your actual API key.

### Step 2: Start the Application
Run the following command to build and start the application:

```sh
docker compose up -d --build
```

This will boot both the backend and frontend servers.

### Step 3: Access the Application
- The **frontend** is accessible at `http://localhost:8003`.
- The **backend API** is available through the exposed endpoints.

## Archetype Logic
The system operates with three predefined **archetypes**, each determining the allowed number of worker agents:

### **Archetype 1**: Single-Agent Judging
- Only **one worker agent** is allowed.
- If multiple agents are provided, an error is raised.

### **Archetype 2**: Multi-Agent Parallel Judging
- The number of worker agents **must match** the specified number of agents (`num_agents`).
- If the count mismatches, an error occurs.

### **Archetype 3**: Odd Number Consensus Judging
- The number of worker agents **must be an odd number**.
- The specified `num_agents` value **must match** the number of worker agents.
- If an even number is provided, an error is raised.

These rules ensure that the system enforces the correct evaluation structure based on the chosen archetype.

## API Usage
To interact with the system, send JSON requests with the following parameters:
- `archetype`: Specifies the evaluation mode (1, 2, or 3).
- `num_agents`: Defines the number of worker agents (optional for archetype 1, required for others).
- `task_meta`: Metadata related to the task.
- `task`: The actual task to be performed.
- `worker_agent_models`: A list of worker agent details, including model name and API endpoint.

Ensure that the input follows the constraints defined by the chosen archetype.

## Contributing
Contributions are welcome! Please follow standard pull request procedures and ensure your changes align with the project's goals.

## License
This project is licensed under an open-source license. See the LICENSE file for details.

---

For any issues or feature requests, feel free to open an issue on GitHub.

