# Agent Interaction Protocol

This document outlines the protocols for how agents within the system interact with each other, manage data hand-offs, and control temporary file access.

## Data Hand-Offs

1. **Completion Trigger**: Each agent must trigger a completion event after finishing its tasks, which can be a simple file flag or a status update in the project management tool.

2. **Data Transfer**: Upon completion, the agent should package its output (if any) in a pre-defined format and location that the next agent in the sequence can access.

3. **Notification**: The next agent in the sequence is notified of the new data availability either through a webhook, an update in a shared task list, or a similar mechanism.

4. **Confirmation**: The receiving agent must confirm the data integrity and log the hand-off before starting its process.

## Temporary Access Permissions

- **Granting Access**: Permissions to specific files and directories are granted on an as-needed basis, governed by an access control list (ACL) or similar permission system.

- **Scope of Access**: Access is strictly limited to the files and directories necessary for the agent's tasks. All permissions are read-write by default but should be limited to read-only where possible.

- **Revocation of Access**: Once an agent's tasks are completed, access to the files and directories is revoked to maintain security and prevent accidental changes.

## Interaction Logging

- All interactions, especially data hand-offs and permission changes, should be logged in a central `interaction_log.md` file to provide an audit trail and facilitate troubleshooting.

## Error Handling

- In case of errors during hand-offs or access issues, agents should log the error details and revert to a safe state, awaiting intervention from a system administrator or developer.

## Agent Synchronization

- Agents must be synchronized to ensure that no two agents are writing to the same file simultaneously. This can be managed through a simple locking mechanism or a queue system.

Ensure that you review and understand these protocols thoroughly as they are crucial for the smooth operation of the system. Each agent's README should include a section detailing these interaction protocols as they pertain to their specific tasks.

