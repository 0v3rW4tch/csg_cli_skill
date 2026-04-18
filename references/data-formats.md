# Data Formats Reference

All CLI commands output JSON for easy parsing and integration with other tools.

## Balance Response

**Command:** `balance`, `balance --account N`

```json
{
  "account": "0319090057086457",
  "balance_cny": 100.0,
  "arrears_cny": 0.0
}
```

| Field | Type | Description |
|-------|------|-------------|
| `account` | string | Electricity account number |
| `balance_cny` | float | Current balance in CNY (RMB) |
| `arrears_cny` | float | Outstanding arrears in CNY |

**Example parsing:**
```bash
# jq example
uv run python scripts/csg_cli.py balance | jq '.balance_cny'
```

---

## Yesterday Response

**Command:** `yesterday`, `yesterday --account N`

```json
{
  "account": "0319090057086457",
  "date": "2026-04-17",
  "power_kwh": 3.65
}
```

| Field | Type | Description |
|-------|------|-------------|
| `account` | string | Electricity account number |
| `date` | string | Date of the reading (YYYY-MM-DD) |
| `power_kwh` | float | Total power consumed in kWh |

---

## Calendar Response

**Command:** `calendar`, `calendar --year Y --month M`, `calendar --account N`

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

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `meteringPointNumber` | string | Meter point identifier |
| `totalPower` | string | Total power for the month in kWh |
| `result` | array | Daily readings array |

### Daily Result Item

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date of reading (YYYY-MM-DD) |
| `power` | string | Power consumed that day in kWh |
| `maxTemperature` | string | Maximum temperature for the day |
| `minTemperature` | string | Minimum temperature for the day |
| `averageTemperature` | string | Average temperature for the day |
| `isHot` | string | "1" if hot day (air conditioning indicator), "0" otherwise |

**Example parsing:**
```bash
# Get total power for current month
uv run python scripts/csg_cli.py calendar | jq '.totalPower'

# Get all daily readings
uv run python scripts/csg_cli.py calendar | jq '.result[]'

# Get dates with highest usage
uv run python scripts/csg_cli.py calendar | jq '.result | sort_by(.power) | reverse | .[0:5]'
```

---

## Electricity Bill Response

**Command:** `elec-bill YEAR MONTH`, `elec-bill YEAR MONTH --account N`

```json
{
  "account": "0319090057086457",
  "year_month": "202603",
  "total_charge_cny": 66.28,
  "total_power_kwh": 112.55
}
```

| Field | Type | Description |
|-------|------|-------------|
| `account` | string | Electricity account number |
| `year_month` | string | Billing period (YYYYMM format) |
| `total_charge_cny` | float | Total charge in CNY |
| `total_power_kwh` | float | Total power consumed in kWh |

**Note:** This is the electricity bill for the specified month, not the current month's usage.

---

## Year Statistics Response

**Command:** `year-stats YEAR`, `year-stats YEAR --account N`

```json
{
  "account": "0319090057086457",
  "year": 2026,
  "total_charge_cny": 1234.56,
  "total_power_kwh": 5678.9,
  "monthly": [
    {"month": "202601", "charge": 123.45, "kwh": 234.5},
    {"month": "202602", "charge": 110.23, "kwh": 210.8},
    {"month": "202603", "charge": 66.28, "kwh": 112.55}
  ]
}
```

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `account` | string | Electricity account number |
| `year` | integer | Year of statistics |
| `total_charge_cny` | float | Total charge for the year in CNY |
| `total_power_kwh` | float | Total power for the year in kWh |
| `monthly` | array | Monthly breakdown array |

### Monthly Item

| Field | Type | Description |
|-------|------|-------------|
| `month` | string | Month identifier (YYYYMM format) |
| `charge` | float | Charge for that month in CNY |
| `kwh` | float | Power consumed that month in kWh |

**Example parsing:**
```bash
# Get total annual consumption
uv run python scripts/csg_cli.py year-stats 2026 | jq '.total_power_kwh'

# Get all monthly breakdowns
uv run python scripts/csg_cli.py year-stats 2026 | jq '.monthly'

# Calculate average monthly bill
uv run python scripts/csg_cli.py year-stats 2026 | jq '.total_charge_cny / .monthly | length'
```

---

## Data Notes

### Data Delay
- **Current month data** has approximately **2 day delay**
- Yesterday's data is typically available by 10 AM the next day

### Historical Data
- **Last year's data** is fully updated during the **first 7 days of January**
- Prior years' data is preserved but may not be updated

### Tiered Pricing
The CSG uses tiered pricing (阶梯电价). Monthly bills reflect:
- Base tier rates for the first tier of consumption
- Higher rates for consumption exceeding tier thresholds
- The exact tier thresholds depend on your account type and location
