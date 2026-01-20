# Temporal.io x LLM: Enterprise-Ready AI Orchestration

This project demonstrates how to build resilient, production-grade AI workflows using **Temporal.io** and **Google Gemini for exemple**. It focuses on overcoming common distributed systems challenges: API instability, long-running processes, and seamless code versioning.

## Key Features
- **Durable Execution**: Workflows resume automatically after server or network failures.
- **Resilient AI Calls**: Integrated retry policies for Gemini API to handle rate limits (429) and timeouts.
- **Safe Versioning**: Demonstrates `workflow.patched` for zero-downtime updates.
- **Clean Architecture**: Separation of concerns between Workflows (orchestration) and Activities (business logic).

---


# Temporal.io

Temporal is an open-source platform that simplifies the development of reliable and resilient distributed applications.

## The Core Concept

Temporal lets you write complex code (workflows, asynchronous tasks, orchestrations) as if it were simple sequential code, while automatically handling typical distributed system problems: failures, retries, timeouts, intermediate states, etc.

**What Temporal handles automatically:**
- ✅ Retries on failure
- ✅ State persistence
- ✅ Recovery from crashes
- ✅ Timeouts
- ✅ Visibility and monitoring

## Typical Use Cases

- **Microservices orchestration**: coordinate multiple services to accomplish complex business processes
- **Payment processing**: manage transactions with automatic retries and failure handling
- **Data pipelines**: orchestrate long-running ETL or data transformations
- **Business processes**: user onboarding, order validation, approval workflows

## Key Benefits

**Reliability**: Temporal guarantees your workflows run to completion, even through server crashes, restarts, or deployments.

**Simplicity**: You write standard imperative code (no complex state machines or manual message queue management).

**Observability**: Web UI to visualize the state of all your running or completed workflows.

**Scalability**: Handles millions of concurrent workflows.

---

# Starter Kit

## Project Structure

This layout follows Python best practices for Temporal projects, ensuring scalability and ease of testing.

```text
.
├── src/
|   |── worker
│   │   ├── activities/
│   │   │   ├── __init__.py
│   │   │   └── activities.py              # AI-related activities
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── call_llm.py                # External call example
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── DefaultSettings.py         # Project variables
│   │   ├── logs/
│   │   │   ├── __init__.py
│   │   │   ├── log_config.py              # Logger configuration
│   │   │   ├── logger.py
│   │   ├── workflows/
│   │   │   ├── __init__.py
│   │   │   └── genai_workflow.py          # Workflow definitions & orchestration
│   │   ├── main_worker.py                 # The Worker (The execution engine)
│   │   └── shared.py                      # Common constants and data models
│   ├── main_workflow.py                   # Workflow requested from application side
├── tests/                                 # Unit and integration tests
├── .env.example                           # Environment variables template
├── pyproject.toml
└── README.md
```

## Prerequisites & Setup


### Self-Hosted Temporal Server
reference page : temporal python dev_environnement


Download the cli and add it to you PATH
## Temporal server

``` 
temporal server start-dev
```

Once your server is running, visit the Temporal Web UI at http://localhost:8233. You can inspect:

- The full history of your AI workflows.
- Real-time retries of failing Gemini calls.
- Input/Output data for every step.


## Testing

This project uses `pytest` and `pytest-asyncio` along with Temporal's testing SDK.

```bash
# Run all tests
pytest