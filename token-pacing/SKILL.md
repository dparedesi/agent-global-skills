---
name: token-pacing
description: Calculate the optimal token usage burn rate to reach exactly 100% usage by the weekly reset. Use when the user asks about token budget, usage limits, spending speed, or "will I run out".
---

# Token Pacing Calculator

Analyzes current token usage against the weekly reset deadline to provide a specific daily burn rate target.

**Why?** Optimizes resource utility by ensuring the user neither runs out of tokens too early nor leaves unused budget on the table.

## Quick Start

1. Get **current usage %** and **reset date/time** from user
2. Run calculations (Steps 1-4 below)
3. Output the Token Pacing Report

---

## Inputs Required

1. **Current Usage %** (e.g., "31%")
2. **Reset Date/Time** (e.g., "Wednesday 9am" or "Jan 15 9am")

> [!TIP]
> If the user says "reset in X days", convert to an actual datetime. If either input is missing, ask the user.

---

## Calculation Steps

Perform these calculations directly — no external script needed.

### Step 1: Calculate Time Metrics

```
now = current date/time
reset = reset date/time (convert user's input to actual datetime)
days_remaining = (reset - now) in days (decimal, e.g., 4.4)
days_elapsed = 7 - days_remaining
time_elapsed_% = (days_elapsed / 7) × 100
```

### Step 2: Calculate Usage Metrics

```
usage_% = user's current usage (e.g., 31)
remaining_% = 100 - usage_%
daily_target = remaining_% / days_remaining
```

### Step 3: Determine Status

Compare `usage_%` to `time_elapsed_%`:

| Condition | Status | Meaning |
|-----------|--------|---------|
| `usage_% < time_elapsed_% - 3` | **Under Budget** | Saving tokens, can spend more freely |
| `usage_% > time_elapsed_% + 3` | **Over Budget** | Burning too fast, need to slow down |
| Otherwise | **On Track** | Balanced pace |

> [!TIP]
> The ±3% buffer avoids false alarms for minor deviations.

### Step 4: Calculate Buffer

```
buffer_% = time_elapsed_% - usage_%
```

- **Positive buffer** = tokens banked (ahead of schedule)
- **Negative buffer** = tokens owed (behind schedule)

---

## Response Template

Report the following:

```
## Token Pacing Report

**Status:** [Under Budget / On Track / Over Budget]

| Metric | Value |
|--------|-------|
| Used | X% |
| Time Elapsed | Y% |
| Buffer | ±Z% |
| Remaining | W% over N days |
| Daily Target | D%/day |

[One sentence recommendation based on status]
```

### Recommendation by Status

- **Under Budget:** "You're saving tokens. You can increase usage to [daily_target]%/day to hit 100% by reset."
- **On Track:** "You're pacing well. Maintain ~[daily_target]%/day."
- **Over Budget:** "You're burning fast. Limit usage to [daily_target]%/day to last until reset."

---

## Examples

### Example 1: Under Budget (The Saver)

**Input:** 31% used, reset Jan 15 9am, current time Jan 10 ~3am

```
days_remaining = 4.4 days
days_elapsed = 7 - 4.4 = 2.6 days
time_elapsed_% = (2.6 / 7) × 100 = 37%

usage_% = 31%
remaining_% = 69%
daily_target = 69 / 4.4 = 15.7%/day

buffer_% = 37 - 31 = +6% (saving tokens)
status = Under Budget (31 < 37 - 3)
```

**Output:**
```
## Token Pacing Report

**Status:** Under Budget

| Metric | Value |
|--------|-------|
| Used | 31% |
| Time Elapsed | 37% |
| Buffer | +6% |
| Remaining | 69% over 4.4 days |
| Daily Target | 15.7%/day |

You're saving tokens. You can increase usage to 15.7%/day to hit 100% by reset.
```

---

### Example 2: Over Budget (The Spender)

**Input:** 80% used, reset in 4 days, current time is day 3 of 7

```
days_remaining = 4 days
days_elapsed = 7 - 4 = 3 days
time_elapsed_% = (3 / 7) × 100 = 43%

usage_% = 80%
remaining_% = 20%
daily_target = 20 / 4 = 5%/day

buffer_% = 43 - 80 = -37% (behind schedule)
status = Over Budget (80 > 43 + 3)
```

**Output:**
```
## Token Pacing Report

**Status:** Over Budget

| Metric | Value |
|--------|-------|
| Used | 80% |
| Time Elapsed | 43% |
| Buffer | -37% |
| Remaining | 20% over 4 days |
| Daily Target | 5%/day |

You're burning fast. Limit usage to 5%/day to last until reset.
```

> [!WARNING]
> At 5%/day, the user has very limited capacity. Consider suggesting they prioritize critical tasks only.

---

### Example 3: On Track (The Balanced)

**Input:** 50% used, 3.5 days remaining (half the week)

```
days_remaining = 3.5 days
days_elapsed = 7 - 3.5 = 3.5 days
time_elapsed_% = (3.5 / 7) × 100 = 50%

usage_% = 50%
remaining_% = 50%
daily_target = 50 / 3.5 = 14.3%/day

buffer_% = 50 - 50 = 0% (perfectly balanced)
status = On Track (within ±3%)
```

**Output:**
```
## Token Pacing Report

**Status:** On Track

| Metric | Value |
|--------|-------|
| Used | 50% |
| Time Elapsed | 50% |
| Buffer | 0% |
| Remaining | 50% over 3.5 days |
| Daily Target | 14.3%/day |

You're pacing well. Maintain ~14.3%/day.
```

---

## Quality Guidelines

- Round percentages to 1 decimal place
- If `daily_target > 50%`, warn that this is an extremely heavy workload
- If `days_remaining < 1`, switch to hourly targets:
  ```
  hours_remaining = days_remaining × 24
  hourly_target = remaining_% / hours_remaining
  ```

> [!WARNING]
> If `daily_target > 50%/day`, add this warning: "This requires very heavy usage. Consider whether you can realistically sustain this pace."

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| User gives ambiguous date ("next Wednesday") | Parse as the next upcoming occurrence from current date |
| Reset time appears to be in the past | Ask user to confirm the next reset date |
| Usage reported as > 100% | Report status as "Exhausted" with 0% remaining, 0%/day target |
| User doesn't know exact reset time | Default to 9:00 AM in user's timezone, or ask for clarification |
| Very short time remaining (< 4 hours) | Switch to per-hour targets and emphasize urgency |

---

## Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|------------------|
| Using 5 days instead of 7 for weekly cycle | Always base calculations on 7-day cycle |
| Forgetting to convert "days left" to decimal | Use precise decimal (e.g., 4.4 days, not 4 days) |
| Reporting buffer as absolute tokens | Buffer is always a percentage |
| Not adjusting for partial days | Include fractional days in calculations |
