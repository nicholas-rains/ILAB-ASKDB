# DB Insights with OneAskDB Crew

Welcome to DB Insights, a powerful natural language to SQL query system powered by CrewAI. This project allows users to query a PostgreSQL database using natural language, with the queries being processed by a sophisticated crew of AI agents.

## Technologies Used

- **Backend**:
  - FastAPI (Python web framework)
  - CrewAI (Multi-agent AI framework)
  - Azure OpenAI (LLM provider)
  - PostgreSQL (Database)
  - UV (Fast Python package installer)
  - Uvicorn (ASGI server)

- **Frontend**:
  - React.js
  - Node.js
  - npm (Package manager)

## Installation and Setup

### Backend Setup

1. Clone the repository and navigate to the project directory:
```bash
cd db-insights
```

2. Activate the virtual environment:
```bash
source .venv/Scripts/activate  # Windows
# OR
source .venv/bin/activate      # macOS/Linux
```

If you need to update the virtual environment, use:
```bash
crewai update
```

3. Create a `.env` file in the project root with the following variables:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/your_dbname
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
OPENAI_API_KEY=your_api_key
AZURE_OPENAI_VERSION=your_azure_version
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_MODEL_NAME=your_model_name
```

### Database Setup

1. Ensure PostgreSQL is installed and running on your system

2. Create the database and tables:
```bash
# Navigate to the database scripts directory
cd app/scripts/db_scripts

# Run the creation script
python create_and_populate_db.py
```

The script will:
- Create necessary tables (account, customer, deposit, etc.)
- Set up proper relationships and constraints
- Populate tables with sample data

You can verify the database setup by checking:
- Tables are created with correct schemas
- Sample data is properly loaded
- Relationships between tables are established

Key tables in the database:
- `account`: Stores account information
- `customer`: Contains customer details
- `deposit`: Manages deposit account information
- `account_x_customer_rltnp`: Manages account-customer relationships
- `customer_idntfctn`: Stores customer identification information

4. Start the backend server:
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 5070 --reload
```

### Frontend Setup

1. Clone the frontend repository and checkout the correct branch:
```bash
git checkout FrntEnd-Demo-with-tablesUed-orglQry
```

2. Install dependencies:
```bash
npm install
```

3. Start the frontend development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Example Queries

You can test the system with these example queries:

1. Show accounts in the deposit table that do not have a customer related to it. Display only distinct account ids.

2. Show customers who has account in Deposit table, and their tax identification number is null. Display only distinct customer id.

More example queries can be found in `Questions_to_Paste.txt` in the project root directory.

## How It Works

The system uses a crew of three specialized AI agents:

1. **Rewriter Agent**: Refines and structures the natural language query
2. **SQL Writer Agent**: Converts the refined query into SQL and executes it
3. **QA Agent**: Validates the SQL query and results

The agents work sequentially to:
- Parse natural language input
- Generate appropriate SQL queries
- Execute queries against the PostgreSQL database
- Validate results
- Return formatted responses to the frontend

## Project Structure

```
db-insights/
├── app/                    # FastAPI application
│   ├── main.py            # Main application entry
│   ├── api.py             # API endpoints
│   └── routers/           # Route handlers
├── src/
│   └── oneaskdb/         # Core CrewAI implementation
│       ├── crew.py       # Agent and crew definitions
│       ├── tools/        # Custom tools for agents
│       └── config/       # Agent and task configurations
└── requirements.txt       # Project dependencies
```

## Troubleshooting

If you encounter any issues:

1. Ensure all environment variables are correctly set in `.env`, `uv.loc`, and `pyproject.toml`
2. Verify the PostgreSQL database is running and accessible
3. Check the backend logs for detailed error messages
4. Ensure you're using Python >=3.10 <=3.13
5. If database issues occur:
   - Check PostgreSQL service is running
   - Verify DATABASE_URL is correct in .env
   - Ensure database and tables are properly created
   - Check database user permissions

## Contributing

Feel free to submit issues and enhancement requests!

# CrewAI Original Readme

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/yhatzi/config/agents.yaml` to define your agents
- Modify `src/yhatzi/config/tasks.yaml` to define your tasks
- Modify `src/yhatzi/crew.py` to add your own logic, tools and specific args
- Modify `src/yhatzi/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the yhatzi Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The yhatzi Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Yhatzi Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.


# CrewAI with PostgreSQL Setup Guide

This guide details how to set up CrewAI with a PostgreSQL database in a Docker container on a new VM.

## Prerequisites

- Linux VM with sudo access
- Docker installed
- Python 3.x installed
- Git installed

## Installation Steps

### 1. System Dependencies


bash
Update package list
sudo apt-get update
Install Python development tools and PostgreSQL client
sudo apt-get install -y python3-dev libpq-dev
Install uv (faster pip alternative)
curl -LsSf https://astral.sh/uv/install.sh | sh


### 2. PostgreSQL Docker Setup

bash
Pull PostgreSQL image
docker pull postgres:latest
Create a directory for PostgreSQL data
mkdir -p ~/postgres-data
Run PostgreSQL container
docker run -d \
--name postgres-db \
-e POSTGRES_PASSWORD=your_password \
-e POSTGRES_DB=your_dbname \
-v ~/postgres-data:/var/lib/postgresql/data \
-p 5432:5432 \
postgres:latest

### 3. Project Setup


bash
Clone the repository
git clone <your-repo-url>
cd <repo-directory>
Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate
Install dependencies using uv
uv pip install psycopg2-binary python-dotenv pandas


### 4. Environment Configuration

Create a `.env` file in the project root:

env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/your_dbname
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
OPENAI_API_KEY=your_api_key
AZURE_OPENAI_VERSION=your_azure_version
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_MODEL_NAME=your_model_name

### 5. Database Setup

The repository includes several scripts for database management:

1. **Clean existing tables** (if needed):

bash
python cleanup_db.py

2. **Create and populate tables**:

bash
python create_and_populate_db.py

3. **Verify data**:
bash
python verify_data.py