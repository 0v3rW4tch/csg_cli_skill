---
name: csg-cli
description: Use when user wants to query China Southern Power Grid (南方电网) electricity data. Triggers on: 电费, 电量, 余额, 用电, 缴费号, 南方电网, electricity, power usage, electricity bill, or any CSG related queries. This skill provides CLI commands to login, check balance, query usage data, and manage electricity accounts.
---

# CSG CLI - China Southern Power Grid

## ⚠️ CRITICAL: Login Status Check (MUST DO)

**Before executing ANY data query command, you MUST check login status first.**

### Step 1: Check if session file exists

```bash
# Check if session.json exists in scripts/ directory
ls scripts/session.json
```

### Step 2: Verify login status (only if session.json exists)

```bash
uv run python scripts/csg_cli.py status
```

- **If `session.json` does NOT exist** → Not logged in, proceed to Step 3
- **If `session.json` exists but `status` shows "Session expired"** → Session invalid, proceed to Step 3
- **If `status` shows "Logged in"** → Ready to query data

### Step 3: Login if needed

```bash
uv run python scripts/csg_cli.py login-sms PHONE
# Enter 6-digit SMS code when prompted
```

### Decision Tree

```
User wants to query data (balance/yesterday/calendar/elec-bill/year-stats)
         │
         ▼
┌─────────────────────┐
│ session.json exists? │
└─────────────────────┘
         │
    ┌────┴────┐
    │Yes      │No
    ▼         ▼
┌─────────┐  ┌─────────────────┐
│status   │  │login-sms PHONE │
│command  │  │→ Enter SMS code │
└─────────┘  └─────────────────┘
    │
    ├─ "Logged in" → Proceed with query
    └─ "Session expired" → login-sms PHONE
```

**Commands that require login**: `balance`, `yesterday`, `calendar`, `elec-bill`, `year-stats`

**Commands that do NOT require login**: `login-sms`, `logout`, `status`

## Overview

CLI tool for querying China Southern Power Grid (南方电网) electricity data.

**Location**: `scripts/csg_cli.py`

## Setup

```bash
# Install dependencies (if not already installed)
uv pip install typer rich

# Or use uv run directly (dependencies auto-installed if pyproject.toml exists)
uv run python scripts/csg_cli.py --help
```

## Quick Commands

```bash
# Authentication
uv run python scripts/csg_cli.py login-sms PHONE
uv run python scripts/csg_cli.py logout

# Status check (always do this first!)
uv run python scripts/csg_cli.py status
uv run python scripts/csg_cli.py accounts

# Data queries
uv run python scripts/csg_cli.py balance
uv run python scripts/csg_cli.py yesterday
uv run python scripts/csg_cli.py calendar --year 2026 --month 4
uv run python scripts/csg_cli.py elec-bill 2026 3
uv run python scripts/csg_cli.py year-stats 2026

# Multi-account support
uv run python scripts/csg_cli.py balance --account 1
```

## Account Selection

Use `--account N` when multiple accounts exist:
- `--account 0` - First account (default)
- `--account 1` - Second account, etc.

Run `accounts` command to see all account indices.

## Notes

- Session persists in `session.json` file
- Data has ~2 day delay for current month
- Last year's data updated during first 7 days of January

## Detailed Documentation

See `references/` directory for:
- `commands.md` - Complete command reference with all options
- `data-formats.md` - Return data format specifications
