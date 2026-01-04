---
name: inbox-assistant
description: Manage Gmail inbox with AI-powered triage, cleanup, and restore. Use when the user mentions "need to check at my emails", inbox, email triage, clean inbox, email cleanup, "check email", email summary, delete emails, manage inbox, or wants to organize their email.
---

# Inbox Assistant

**Why?** Email overload is real—most inboxes are cluttered with newsletters, promotions, and notifications that bury important messages. This skill applies expert classification to surface what matters and safely clean the rest.

Comprehensive Gmail inbox management using the `inboxd` CLI tool. Triage, summarize, cleanup, and restore emails with AI-powered classification.

## Quick Start

| Task | Command |
|------|---------|
| Check status | `inbox summary --json` |
| Full triage | `inbox analyze --count 50` → classify → present |
| Delete emails | `inbox delete --ids "id1,id2" --confirm` |
| Undo deletion | `inbox restore --last N` |

## Package Information

| | |
|---|---|
| **Package** | `inboxd` |
| **Install** | `npm install -g inboxd` |
| **Setup** | `inbox setup` (interactive wizard) |
| **Documentation** | https://github.com/dparedesi/inboxd |
| **npm** | https://www.npmjs.com/package/inboxd |

## Pre-flight Check

Before any inbox operation, always verify the setup:

```bash
# 1. Check if inboxd is installed
inbox --version

# 2. Check if accounts are configured
inbox accounts
```

### If Not Installed

> [!TIP]
> Guide the user through installation—it takes about 5 minutes.

```
inboxd is not installed. To install:

1. Run: npm install -g inboxd
2. Run: inbox setup
3. Follow the wizard to configure your Gmail account

The setup requires creating OAuth credentials in Google Cloud Console.
```

### If No Accounts Configured
```
No Gmail accounts configured. Run: inbox setup

This will guide you through:
1. Creating OAuth credentials in Google Cloud Console
2. Authenticating your Gmail account
```

## Command Reference

### Status & Reading

| Command | Description | Output |
|---------|-------------|--------|
| `inbox summary --json` | Quick inbox overview | `{accounts: [{name, email, unreadCount}], totalUnread}` |
| `inbox analyze --count 50` | Get email data for analysis | JSON array of email objects |
| `inbox analyze --count 50 --all` | Include read emails | JSON array (read + unread) |
| `inbox accounts` | List configured accounts | Account names and emails |

### Actions

| Command | Description |
|---------|-------------|
| `inbox delete --ids "id1,id2,id3" --confirm` | Move emails to trash |
| `inbox restore --last N` | Restore last N deleted emails |
| `inbox restore --ids "id1,id2"` | Restore specific emails |
| `inbox deletion-log` | View recent deletions |

### Email Object Shape
```json
{
  "id": "18e9abc123",
  "threadId": "18e9abc123",
  "from": "Sender Name <sender@example.com>",
  "subject": "Email Subject Line",
  "snippet": "Preview of the email content...",
  "date": "Fri, 03 Jan 2026 10:30:00 -0800",
  "account": "personal",
  "labelIds": ["UNREAD", "INBOX", "CATEGORY_PROMOTIONS"]
}
```

## Workflow

### 1. Check Inbox Status
```bash
inbox summary --json
```
Report the total unread count and per-account breakdown.

### 2. Fetch Emails for Analysis
```bash
inbox analyze --count 50
```
Parse the JSON output and classify each email.

### 3. Classify Emails

Categorize each email into one of these categories:

#### Important
- From known contacts or domains the user has corresponded with
- Contains urgent keywords: "urgent", "asap", "action required", "deadline"
- Direct replies to user's emails (Re: in subject)
- From the user's organization domain

#### Newsletters
- From contains: newsletter, digest, weekly, noreply, news@
- Subject contains: issue #, edition, roundup, weekly, digest
- Has CATEGORY_PROMOTIONS or CATEGORY_UPDATES label

#### Promotions
- From contains: marketing, promo, sales, deals, offers, shop
- Subject contains: % off, sale, discount, limited time, exclusive, deal, save
- Has CATEGORY_PROMOTIONS label

#### Notifications
- From contains: notify, alert, noreply, automated, no-reply
- Subject contains: notification, alert, update, reminder, receipt, confirmation
- Snippet is short (<50 chars) and appears templated (generic text like "You have a new notification" or "Your order has shipped")
- Has CATEGORY_UPDATES label

#### Low-Priority / Spam-like
- Repeated sender (>3 emails from same sender in batch)
- Generic/clickbait subjects
- No personalization in snippet
- Unknown sender with promotional tone

### 4. Present Summary

Show the user a categorized breakdown:
```
## Inbox Analysis

**Total Unread:** 47 emails across 2 accounts

### By Category:
- Important: 5 emails
- Newsletters: 12 emails
- Promotions: 18 emails
- Notifications: 8 emails
- Low-Priority: 4 emails

### Recommended for Cleanup:
I found 22 emails that could be deleted:
- 12 newsletters (older than 3 days)
- 8 promotional emails
- 2 duplicate notifications

Would you like me to show the list before deleting?
```

### 5. Show Deletion Candidates

> [!CAUTION]
> Always show the full list before any deletion. Never skip this step.

```
## Emails Recommended for Deletion

### Newsletters (12)
1. "TechCrunch Daily" - Issue #423: AI News...
2. "Morning Brew" - Your Daily Digest...
...

### Promotions (8)
1. "Amazon" - 50% off electronics...
2. "Best Buy" - Limited time deals...
...

Delete these 20 emails? (y/n)
```

### 6. Execute Deletion

Only after explicit user confirmation:
```bash
inbox delete --ids "id1,id2,id3,..." --confirm
```

### 7. Confirm & Remind About Undo

After deletion:
```
Deleted 20 emails successfully.

To undo, run: inbox restore --last 20
Deletion log: inbox deletion-log
```

## Safety Rules

> [!CAUTION]
> These rules are non-negotiable. Violating them risks deleting important emails.

1. **NEVER auto-delete** - Always show what will be deleted and wait for explicit confirmation
2. **NEVER delete "Important" emails** - Do not even suggest deleting emails classified as Important
3. **Show sender + subject** - User must see exactly what will be deleted
4. **Batch limit: 20** - For large cleanups, suggest multiple passes
5. **Always remind about undo** - After every deletion, mention `inbox restore --last N`
6. **Preserve by default** - When in doubt about classification, keep the email

## Common Mistakes to Avoid

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Deleting without showing the list first | User can't verify what's being deleted | Always show full list, wait for "yes" |
| Suggesting deletion of "Re:" emails | These are often important replies | Classify as Important, never suggest deletion |
| Batching >20 emails at once | Harder to undo, overwhelming to review | Suggest multiple passes |
| Skipping pre-flight check | Tool may not be installed | Always run `inbox --version` first |
| Forgetting the `--confirm` flag | Command will hang waiting for input | Always include `--confirm` for non-interactive |

## Example Interactions

### "Clean up my inbox"
1. Run `inbox summary --json` to check status
2. Run `inbox analyze --count 50` to get emails
3. Classify and present summary
4. Show deletion candidates (excluding Important)
5. Wait for explicit confirmation
6. Execute and remind about undo

### "What's in my inbox?"
1. Run `inbox summary --json`
2. Report counts per account
3. Offer full triage if count is high

### "Undo last deletion"
1. Run `inbox restore --last 1`
2. Confirm restoration

## Multi-Account Support

> [!TIP]
> When user has multiple accounts, always show which account each email belongs to.

- Group recommendations by account
- Allow user to specify account: "clean up my work inbox"
- Use `--account <name>` flag when needed

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `command not found: inbox` | Run: `npm install -g inboxd` |
| "No accounts configured" | Run: `inbox setup` |
| Token expired / auth errors | Delete token and re-auth: `rm ~/.config/inboxd/token-<account>.json && inbox auth -a <account>` |
| Permission errors on delete | Re-authenticate: `inbox logout -a <account> && inbox auth -a <account>` |

## Testing

### Evaluation Scenarios

| Scenario | Expected Behavior | Failure Indicator |
|----------|-------------------|-------------------|
| User says "clean my inbox" | Run summary → analyze → classify → present → wait for confirmation | Auto-deletes without confirmation |
| inboxd not installed | Detect missing tool, guide installation | Proceeds to run commands that fail |
| User says "delete all emails" | Show list first, ask for confirmation | Deletes without showing list |
| User says "undo" | Run `inbox restore --last N` | Fails to restore or wrong count |

### Model Coverage
- Tested with: Sonnet, Opus
- Pre-flight check critical for all models to avoid tool errors
