# Demo: GitHub Actions outage

This PR demonstrates that the `Version Bump` workflow is a convenience,
not a merge gate. With the workflow manually disabled (simulating an
Actions outage), a write-access user can still merge this PR directly
through the GitHub UI, without commenting `/merge` and without any
approvals, since `main` has no branch protection rule requiring them.

No `## Unreleased` bullet is added here on purpose, so merging this
PR leaves nothing dangling in CHANGELOG.md for later automation to
pick up.
