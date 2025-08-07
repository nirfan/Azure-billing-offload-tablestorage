# Azure Billing Records Cost Optimization – Table Storage Approach

## Overview
This solution demonstrates an efficient, API-preserving, and production-ready method to minimize Azure Cosmos DB costs for billing records. By archiving records older than 3 months into Azure Table Storage, we leverage affordable storage while ensuring all records stay available (with seconds-level latency). The approach uses timer-triggered automation and a federated data provider to keep API contracts unchanged and transitions seamless.

## Architecture

![Architecture Diagram](architecture-diagram.png)

## Why Azure Table Storage?
- Lower cost per operation and per GB than Cosmos DB for large, infrequently accessed datasets.
- Fast key-based record lookup, making it ideal for cold archival needs.
- Simple integration and native durability via Azure.

## Core Components
- **Cosmos DB:** Holds “hot” (<3 months) data.
- **Azure Table Storage:** Archives “cold” (>3 months) records.
- **Timer-triggered Azure Function:** Automates migration/offload.
- **Unified Data Access Layer:** Handles API data access with Cosmos-or-table fallback logic.

## Files Overview

| File                    | Description                                            |
|-------------------------|--------------------------------------------------------|
| README.md               | This documentation.                                    |
| architecture-diagram.png| Visual representation of the architecture.             |
| offload_to_table.py     | Script/function to move old data to Table Storage.     |
| billing_data_access.py  | Data retrieval library for federated queries.          |
| .gitignore              | Ignore list
