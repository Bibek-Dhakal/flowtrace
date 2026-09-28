# Architecture Design

FlowTrace is designed entirely around an explicit, failure-sensitive Directed Acyclic Graph (DAG). 

## Unified System Journey

```mermaid
graph TD
    A[New Raw Data Arrives] --> B[Ingestion Stage]
    B -- Schema Validation --> C{Schema Valid?}
    C -- No --> D[Halt & Log Violation]
    C -- Yes --> E[Quality Gate]
    
    E -- Pandera Checks --> F{Quality Pass?}
    F -- No --> G[Halt & Alert Pipeline Failed]
    F -- Yes --> H[Feature Engineering]
    
    H --> I[Model Training]
    I -- MLFlow Logging --> J[Evaluation Stage]
    J -- Compare vs Prod Model --> K{Better Performance?}
    
    K -- No --> L[Retain Previous Model]
    K -- Yes --> M[Register & Promote Model to Prod]
    M --> N[Lineage Record Linked: Data Hash + Run ID]
```

## Components
- **Prefect Orchestrator**: Wraps Python functions into stages (`@task`) and combines them in an executable pipeline (`@flow`).
- **Pandera Validator**: Intercepts the Pandas DataFrame directly after ingestion, asserting bounds, typings, and non-null guarantees.
- **MLflow Tracker**: Operates as a background context manager during the Training and Evaluation phases to commit metrics and parameters to a local SQLite registry.