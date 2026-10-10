# Poly-Scan Architecture

This document provides a deeper look into the Poly-Scan V1 architecture.

## Design Philosophy
The system strictly decouples the language-specific parsing from the language-agnostic behavioral analysis. 

### 1. Parsers (`app/parsers/`)
Responsible for reading raw string code and converting it to metadata blocks without execution.
- `PythonParser`: Uses `ast.NodeVisitor` to recurse through nodes.
- `JavaScriptParser`: Uses `esprima.parseScript` and recursively extracts `CallExpression` nodes.

### 2. Action Mapper (`app/analyzer/action_mapper.py`)
Responsible for acting as the "dictionary" that translates known language-specific function calls into the Universal Tag format.

### 3. Behavior Graph (`app/analyzer/behavior_graph.py`)
Constructs directed edges between identified actions based on line numbers to establish the execution sequence.

### 4. Similarity Engine (`app/analyzer/similarity.py`)
Provides deterministic algorithms (non-ML) to output an explainable similarity percentage, calculating:
- **Jaccard similarity** for tags present.
- **Longest Common Subsequence (LCS)** for structural execution order.

### 5. API & UI
- **FastAPI** handles the REST endpoints and WebSockets with Pydantic payload validation.
- **React + Vite** frontend parses the generated graphs using `@xyflow/react`.
