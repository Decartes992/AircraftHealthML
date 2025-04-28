# AircraftHealthML Documentation Plan

**Goal:** Analyze the AircrafthealthML codebase, generate foundational documentation files, add initial code-level documentation (docstrings), create a project README.md, and establish the chatbot_guide.md, using only base Roo modes.

**Primary Source Code Directories:**
*   `aircraft_health/aircraft_health/`
*   `aircraft_health/aircraft_health/monitoring/`
*   `aircraft_health/aircraft_health/monitoring/frontend/src/`
*   `aircraft_health/aircraft_health/monitoring/ml_models/`
*   `aircraft_health/aircraft_health/monitoring/management/commands/`

**Plan Overview:**

The task will be broken down into several sub-tasks, primarily executed in Code Mode, with Orchestrator Mode handling the initial planning and final reporting.

```mermaid
graph TD
    A[Start: Orchestrator Mode] --> B{Gather Context & Plan};
    B --> C[Present Plan to User];
    C --> D{User Approval?};
    D -- Yes --> E[Switch to Code Mode];
    E --> F[Sub-Task 1: Codebase Analysis & Foundational Docs];
    F --> G[Sub-Task 2: Create chatbot_guide.md];
    G --> H[Sub-Task 3: Add Initial Code-Level Docstrings];
    H --> I[Sub-Task 4: Generate/Update README.md];
    I --> J[Switch back to Orchestrator Mode];
    J --> K[Sub-Task 5: Final Report];
    K --> L[Attempt Completion];
    D -- No --> B; % Loop back for plan modification
```

**Detailed Steps:**

1.  **Initial Planning (Architect Mode - Current):**
    *   Analyze the user's request and the provided file structure.
    *   Identify primary source code directories (completed via follow-up question).
    *   Outline the sub-tasks and their dependencies.
    *   Create this detailed plan, including required outputs and constraints.
    *   Present the plan to the user for review.

2.  **User Review and Approval:**
    *   The user will review the plan and provide feedback or approval.

3.  **Switch to Code Mode:**
    *   Upon user approval, Orchestrator Mode will request a switch to Code Mode to perform the analysis and documentation generation.

4.  **Sub-Task 1: Codebase Analysis & Foundational Docs (Code Mode):**
    *   **Action:** Use `read_file` and `list_code_definition_names` on the specified primary source code directories to understand the project structure, key modules, components (data processing, ML models, web app), primary functions/classes, and potential API endpoints. Reference `aircraft_health/Presentation.pdf` for additional context using `read_file`.
    *   **Action:** Based on the analysis, use `write_to_file` to create the following markdown files in the `/documentation/` directory:
        *   `codebase_overview.md`: High-level structure, main directories, detected technologies based on code.
        *   `data_pipeline.md`: Document the data flow (ingestion, preprocessing, features) as inferred from the relevant code sections (likely in `ml_models/data/` and `management/commands/load_flight_data.py`).
        *   `ml_models.md`: Detail the ML models (Isolation Forest, Transformer) identified in the code (likely in `ml_models/Models/` and `ml_models/Testing/`), their purpose, inputs/outputs, and associated libraries.
        *   `webapp_integration.md`: Describe the web application structure found in the code (Django Rest backend in `monitoring/` and React frontend in `monitoring/frontend/src/`) and its connections.
        *   `api_endpoints.md` (if applicable): Document API endpoints found in the code (likely in `monitoring/urls.py` and `monitoring/views.py`).
    *   **Constraint Check:** Ensure all files are written to the `/documentation/` directory.

5.  **Sub-Task 2: Create Initial chatbot_guide.md (Code Mode):**
    *   **Action:** Synthesize information gathered during the analysis in Sub-Task 1 and from `aircraft_health/Presentation.pdf` to create the chatbot guide content.
    *   **Action:** Use `write_to_file` to create the file `/documentation/dev_docs/chatbot_guide.md` with the synthesized content, including:
        *   Project Goal & Overview.
        *   Key Technologies Used.
        *   Data Sources (ADAPT, NGAFID).
        *   Core Components Identified.
        *   Pointers to the main documentation files created in Sub-Task 1.
    *   **Constraint Check:** Ensure the file is written to the `/documentation/dev_docs/` directory.

6.  **Sub-Task 3: Add Initial Code-Level Docstrings (Code Mode):**
    *   **Action:** Identify primary Python scripts/modules within the specified source directories (e.g., files in `monitoring/`, `ml_models/`, `management/commands/`).
    *   **Action:** For each identified Python file, use `read_file` to get its content. Analyze key functions and classes. Use `insert_content` or `apply_diff` to add PEP 257 compliant docstrings explaining purpose, parameters, and returns.
    *   **Constraint Check:** Apply standard Python docstring conventions.
    *   **CRITICAL Constraint (Persistent Documentation Rule):** After successfully modifying a code file with docstrings, use `read_file` on the relevant `.md` files in `/documentation/` (created in Sub-Task 1) and compare the new docstring information. If new information is pertinent, use `apply_diff` or `write_to_file` to update the relevant documentation file to reflect the changes. Log this action to `project_scratchpad.md`.

7.  **Sub-Task 4: Generate/Update README.md (Code Mode):**
    *   **Action:** Check if `README.md` exists in the project root using `list_files`.
    *   **Action:** If it exists, use `read_file` to get its content. If not, prepare content for a new file.
    *   **Action:** Use `write_to_file` to create or update the `README.md` file in the project root with:
        *   Project Title & Description.
        *   Key Features/Objectives.
        *   Technology Stack Summary (derived from analysis).
        *   Basic Setup/Usage Instructions (placeholder).
        *   A prominent link to the `/documentation/` directory.
    *   **Constraint Check (Persistent Documentation Rule - Read-Only):** Use `read_file` on the relevant `.md` files in `/documentation/` to verify that the summary information added to the README is consistent with the details in the documentation files. Log this verification to `project_scratchpad.md`.

8.  **Switch back to Orchestrator Mode:**
    *   After completing Sub-Tasks 1-4, Code Mode will request a switch back to Orchestrator Mode.

9.  **Sub-Task 5: Final Report (Orchestrator Mode):**
    *   **Action:** Consolidate the results and logs from all completed sub-tasks, including confirmations of file creation/modification and adherence to documentation rules.
    *   **Action:** Use `attempt_completion` to provide a summary report detailing the files created/modified, confirmation of documentation rule adherence checks, and any issues encountered.

**Mermaid Diagram for Code Mode Sub-Tasks:**

```mermaid
graph TD
    A[Start: Code Mode] --> B[Sub-Task 1: Analyze Code & Presentation];
    B --> C[Sub-Task 1: Create Foundational Docs in /documentation/];
    C --> D[Sub-Task 2: Create chatbot_guide.md in /documentation/dev_docs/];
    D --> E[Sub-Task 3: Identify Python Files];
    E --> F{For Each Python File};
    F --> G[Add Docstrings];
    G --> H[Check Relevant Docs in /documentation/];
    H --> I{Docs Need Update?};
    I -- Yes --> J[Update Docs & Log to Scratchpad];
    I -- No --> F; % Continue to next file
    J --> F; % Continue to next file
    F --> K[Sub-Task 4: Create/Update README.md];
    K --> L[Verify README Consistency with Docs & Log to Scratchpad];
    L --> M[Request Switch to Orchestrator Mode];