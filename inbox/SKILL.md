---
name: inbox
description: Check Gmail inbox for unread emails and show summary. Use when the user wants to check their email, see new messages, get inbox status, analyze inbox, triage emails, delete emails, or when they mention "check email", "inbox", "unread", "new mail", "analyze", "triage", "categorize", or "delete".
---

# Gmail Inbox Monitor

Check your Gmail inbox for unread emails without leaving the CLI.

**Why?** Reduces context-switching by letting you monitor email from the terminal instead of opening a browser.

## Quick Start

1. Run summary → 2. See unread count + emails → Done

```bash
cd /Users/danielparedes/Documents/Github/inboxd && node src/cli.js summary
```

## Prerequisites

- Gmail API credentials set up (see SETUP.md in project)
- Authenticated with `node src/cli.js auth`

## How It Works

### Step 1: Check Inbox Summary

Run the CLI to see a formatted summary of unread emails:

```bash
cd /Users/danielparedes/Documents/Github/inboxd && node src/cli.js summary
```

This shows:
- Total unread count
- Recent emails with sender and subject
- Last check timestamp

### Step 2: Check for New Emails (with notifications)

For background-style check that notifies of new emails:

```bash
cd /Users/danielparedes/Documents/Github/inboxd && node src/cli.js check
```

This:
- Fetches unread emails
- Compares against previously seen emails
- Sends macOS notification if new ones found
- Marks them as "seen" for next check

### Step 3: Analyze & Categorize Emails

To triage the inbox using AI analysis:

1. Run the analyze command (fetches unread emails only by default):
```bash
cd /Users/danielparedes/Documents/Github/inboxd && node src/cli.js analyze -n 20
```

Options:
- `-n 20` - Number of emails per account (default: 20)
- `-a <account>` - Specific account or "all" (default: all)
- `--all` - Include read AND unread emails (only use if user asks for "read and unread")

2. The command outputs JSON with email data including:
   - `from`, `subject`, `snippet` (preview text)
   - `labelIds` (Gmail categories like CATEGORY_PROMOTIONS, CATEGORY_UPDATES)
   - `account` (which inbox it's from)

3. Categorize each email into one of these groups:

   **⚡ Action Needed** - Requires a response or action
   - Direct questions addressed to the user
   - Meeting requests, invites requiring RSVP
   - Bills, payments due
   - Urgent work matters

   **⭐ Worth Reading** - Interesting content to read when time permits
   - Newsletters you actually read
   - Industry updates relevant to your work
   - Job alerts that match your interests (check the actual role, not just any job)

   **📦 FYI Only** - Informational, no action needed
   - Receipts, order confirmations
   - Shipping notifications
   - Automated system alerts
   - GitHub notifications (unless you're tagged directly)

   **🗑️ Safe to Delete** - Can be deleted without reading
   - Promotional emails (labelIds contains CATEGORY_PROMOTIONS)
   - Cold outreach, spam
   - Newsletters you never read
   - Expired offers or events

4. Present results in this format:

```markdown
# Inbox Analysis (X emails across Y accounts)

## ⚡ Action Needed
- **[Account] Sender**: Subject - why action is needed

## ⭐ Worth Reading
- **[Account] Sender**: Subject - why it's worth reading

## 📦 FYI Only
- **[Account] Sender**: Subject

## 🗑️ Safe to Delete
- **[Account] Sender**: Subject - why safe to delete
```

## Examples

**Example 1: Quick inbox check**
- Input: User says "check my email"
- Output: Run `summary` command and present formatted output

**Example 2: Background monitoring**
- Input: User wants notifications for new mail
- Output: Run `check` command (can be automated via launchd)

**Example 3: Inbox triage**
- Input: User says "analyze my inbox" or "triage my emails"
- Output: Run `analyze` command, categorize results, present markdown report

**Example 4: Delete emails**
- Input: User says "delete the safe to delete emails" after analysis
- Output: Collect IDs from 🗑️ category, run `delete --ids "..." --confirm`, report results

### Step 4: Delete Emails

To delete emails identified as safe to delete:

1. From the analysis output, collect the message IDs of emails to delete
2. Run the delete command:
```bash
cd /Users/danielparedes/Documents/Github/inboxd && node src/cli.js delete --ids "id1,id2,id3" -a <account> --confirm
```

Options:
- `--ids` - Comma-separated message IDs (required)
- `-a <account>` - Account name (required if multiple accounts configured)
- `--confirm` - Skip confirmation prompt

3. Deletions are logged to: `~/.config/inboxd/deletion-log.json`

**Important:** Emails are moved to Gmail Trash (recoverable for 30 days), not permanently deleted.

### Step 5: View Deletion History

To see what emails have been deleted:

```bash
cd /Users/danielparedes/Documents/Github/inboxd && node src/cli.js deletion-log
```

Options:
- `-n <days>` - Show deletions from last N days (default: 30)

The log contains full email metadata (from, subject, snippet, ID) for manual recovery if needed.

## Quality Guidelines

- Always run from the project directory
- If auth fails, prompt user to run `node src/cli.js auth`
- Present output in a clean, readable format
- For analysis, explain WHY each email is categorized (helps user learn their preferences)

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "credentials.json not found" | Missing OAuth setup | Follow SETUP.md to create credentials |
| "Token expired" | Auth token needs refresh | Run `node src/cli.js auth` again |
| No notifications | macOS settings | Check System Preferences > Notifications |
| "Permission denied" (403) on delete | Scope changed | Re-run `node src/cli.js auth` for each account |
