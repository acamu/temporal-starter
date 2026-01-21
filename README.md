# Temporal.io x LLM: Enterprise-Ready AI Orchestration

This project demonstrates how to build resilient, production-grade AI workflows using **Temporal.io** and **fake LLM for exemple**. It focuses on overcoming common distributed systems challenges: API instability, long-running processes, and seamless code versioning.

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
|   |── worker_simple
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
│   │   ├── main_simple_worker.py          # The Worker (The execution engine)
│   │   └── shared.py                      # Common constants and data models
│   ├── main_simple_workflow.py            # Workflow requested from application side
├── tests/                                 # Unit and integration tests
├── .env.example                           # Environment variables template
├── pyproject.toml
└── README.md
```

Workflows  

With Front End (Not part now of this example)

```mermaid
sequenceDiagram
    participant UI as Angular Frontend
    participant API as FastAPI Gateway
    participant T as Temporal Server
    participant W as Workflow (Worker)
    participant A as Activities (LLM/Email)

    Note over UI, API: Phase d'Initialisation
    UI->>API: POST /workflow/start (brouillon)
    API->>T: Start Workflow (ProfessionalEmailWorkflow)
    T-->>API: workflow_id
    API-->>UI: workflow_id

    Note over UI, W: Boucle de Feedback (Polling)
    loop Jusqu'à Complétion
        UI->>API: GET /workflow/state/{id}
        API->>T: Query: get_state + Describe
        T-->>API: { status: RUNNING, is_thinking: true/false, proposal: "..." }
        API-->>UI: Full State JSON
    end

    Note over W, A: Phase d'exécution IA
    W->>A: execute_activity: call_external_api (LLM)
    activate A
    A-->>W: Résultat réécrit
    deactivate A

    Note over UI, W: Interaction Humaine
    UI->>API: POST /workflow/signal/{id} (Valider ou Modifier)
    API->>T: Signal: submit_email_content OU approve_llm_result
    T->>W: Réveil du workflow (Update state)

    Note over W, A: Phase Finale
    W->>A: execute_activity: send_email
    A-->>W: Succès
    W-->>T: Completed

```
  
Worker and workflow example
```mermaid
sequenceDiagram
    participant TS as Temporal Server (Persistence)
    participant W as Workflow Definition
    participant WR as Worker (Executor)
    participant A as Activities (LLM / Email)

    Note over TS, WR: Le Worker écoute la Task Queue
    
    TS->>WR: Workflow Task (Start)
    WR->>W: Initialise l'état (_is_thinking=False)
    
    W->>TS: Wait Condition (Attente _content)
    Note right of TS: Le Workflow est suspendu (0 CPU)

    TS->>WR: Signal: submit_email_content
    WR->>W: Mise à jour _content
    
    loop Tant que pas approuvé (_is_approved == False)
        W->>W: Set _is_thinking = True
        W->>TS: Schedule Activity: call_external_api
        TS->>WR: Activity Task
        WR->>A: Execute: call_external_api
        A-->>WR: Résultat (Texte réécrit)
        WR-->>TS: Activity Task Completed
        
        TS->>WR: Workflow Task (Resume)
        WR->>W: Update _proposal & _is_thinking = False
        
        W->>TS: Wait Condition (Signal Approval ou New Content)
        Note right of TS: Le Workflow "dort" en attendant l'humain
        
        TS->>WR: Signal: approve_llm_result(True)
        WR->>W: Set _is_approved = True
    end

    W->>TS: Schedule Activity: send_email
    TS->>WR: Activity Task
    WR->>A: Execute: send_email
    A-->>WR: Success
    WR-->>TS: Activity Task Completed
    
    W->>TS: Workflow Completed
    Note over TS: Fin de l'historique

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