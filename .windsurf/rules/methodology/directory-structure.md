---
description: directory structure to follow
trigger: always_on
---     
# Directory Structure
```mermaid
flowchart TD
    Root[Project Root]
    Root --> Backend[backend/ — Django API]
    Root --> Frontend[frontend/ — Vite + React SPA]
    Root --> Scripts[scripts/ — Quality & tooling]
    Root --> Docs[docs/ — Standards & methodology]
    Root --> Tasks[tasks/ — Task tracking & RFCs]
    Root --> Windsurf[.windsurf/rules/ — IDE rules & methodology]
    Root --> GitHub[.github/workflows/ — CI]
```