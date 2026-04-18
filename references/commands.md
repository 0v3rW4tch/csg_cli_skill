# Commands Reference

## Authentication Commands

### login-sms
Login with SMS verification code.

```bash
# Interactive - will prompt for 6-digit code
uv run python scripts/csg_cli.py login-sms PHONE

# With password (alternative method)
uv run python scripts/csg_cli.py login-sms PHONE --password PASSWORD
```

**Arguments:**
- `PHONE` (required): Phone number for SMS verification

**Options:**
- `--password`: Optional password for dual authentication

**Output:**
```
SMS sent. Enter 6-digit code:
[User enters code]
Logged in successfully!
```

### logout
Clear session and logout.

```bash
uv run python scripts/csg_cli.py logout
```

---

## Status & Account Commands

### status
Check current login status.

```bash
uv run python scripts/csg_cli.py status
```

**Output (logged in):**
```
Logged in
```

**Output (session expired):**
```
Session expired
```

### accounts
List all electricity accounts associated with the logged-in user.

```bash
uv run python scripts/csg_cli.py accounts
```

**Output:**
```
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃   Idx ┃ Account           ┃ User    ┃ Address             ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│     0 │ 0319090057086457  │ 张三    │ 广州市天河区xxx路... │
└───────┴───────────────────┴─────────┴────────────────────┘
```

Use the `Idx` column with `--account` option for other commands.

---

## Data Query Commands

All data query commands require login. **Run `status` first to verify.**

### balance
Get account balance and any arrears.

```bash
uv run python scripts/csg_cli.py balance
uv run python scripts/csg_cli.py balance --account 0
```

**Options:**
- `--account` (int, default=0): Account index from `accounts` command

**Output (JSON):**
```json
{
  "account": "0319090057086457",
  "balance_cny": 100.0,
  "arrears_cny": 0.0
}
```

### yesterday
Get yesterday's total electricity usage.

```bash
uv run python scripts/csg_cli.py yesterday
uv run python scripts/csg_cli.py yesterday --account 0
```

**Options:**
- `--account` (int, default=0): Account index

**Output (JSON):**
```json
{
  "account": "0319090057086457",
  "date": "2026-04-17",
  "power_kwh": 3.65
}
```

### calendar
Get daily electricity usage and temperature data for a month.

```bash
uv run python scripts/csg_cli.py calendar
uv run python scripts/csg_cli.py calendar --year 2026 --month 4
uv run python scripts/csg_cli.py calendar --account 0
```

**Options:**
- `--year` (int, default=current year): Target year
- `--month` (int, default=current month): Target month (1-12)
- `--account` (int, default=0): Account index

**Output (JSON):**
```json
{
  "meteringPointNumber": "1117482840",
  "totalPower": "63.95",
  "result": [
    {
      "date": "2026-04-01",
      "power": "3.65",
      "maxTemperature": "28.8",
      "minTemperature": "16.0",
      "averageTemperature": "22.40",
      "isHot": "0"
    }
  ]
}
```

### elec-bill
Get monthly electricity bill with total charge and power consumption.

```bash
uv run python scripts/csg_cli.py elec-bill 2026 3
uv run python scripts/csg_cli.py elec-bill 2026 3 --account 0
```

**Arguments:**
- `year` (required): Target year (e.g., 2026)
- `month` (required): Target month (1-12)

**Options:**
- `--account` (int, default=0): Account index

**Output (JSON):**
```json
{
  "account": "0319090057086457",
  "year_month": "202603",
  "total_charge_cny": 66.28,
  "total_power_kwh": 112.55
}
```

### year-stats
Get yearly statistics with monthly breakdown.

```bash
uv run python scripts/csg_cli.py year-stats 2026
uv run python scripts/csg_cli.py year-stats 2026 --account 0
```

**Arguments:**
- `year` (required): Target year

**Options:**
- `--account` (int, default=0): Account index

**Output (JSON):**
```json
{
  "account": "0319090057086457",
  "year": 2026,
  "total_charge_cny": 1234.56,
  "total_power_kwh": 5678.9,
  "monthly": [
    {"month": "202601", "charge": 123.45, "kwh": 234.5},
    {"month": "202602", "charge": 110.23, "kwh": 210.8}
  ]
}
```

---

## Common Workflows

### First Time Setup
```bash
# 1. Check if dependencies are available
uv run python scripts/csg_cli.py --help

# 2. Login with SMS
uv run python scripts/csg_cli.py login-sms 13800138000

# 3. Verify login
uv run python scripts/csg_cli.py status

# 4. List accounts
uv run python scripts/csg_cli.py accounts
```

### Daily Usage Check
```bash
# 1. Always verify login first
uv run python scripts/csg_cli.py status

# 2. Check balance
uv run python scripts/csg_cli.py balance

# 3. Check yesterday's usage
uv run python scripts/csg_cli.py yesterday
```

### Monthly Bill Review
```bash
# 1. Verify login
uv run python scripts/csg_cli.py status

# 2. Get current month calendar
uv run python scripts/csg_cli.py calendar

# 3. Get last 3 months bills
uv run python scripts/csg_cli.py elec-bill 2026 3
uv run python scripts/csg_cli.py elec-bill 2026 2
uv run python scripts/csg_cli.py elec-bill 2026 1
```
