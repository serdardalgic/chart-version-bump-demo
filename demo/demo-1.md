# Demo 1: happy path

This PR demonstrates the full `/merge` flow:

1. Opened without a bullet under `## Unreleased` (checklist should show unchecked).
2. A follow-up commit adds the bullet (checklist should flip to checked).
3. Comment `/merge please` first (should be ignored, not an exact match).
4. Comment `/merge` (approval check skipped since base is `test/*`): bumps Chart.yaml, finalizes CHANGELOG, merges.
5. Comment `/merge` again after merge (idempotency check: should be rejected, no double bump).
