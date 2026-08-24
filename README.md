# chart-version-bump-demo

Demo repo for an automated Helm `Chart.yaml` version bump + `CHANGELOG.md` finalization workflow, triggered by a `/merge` PR comment.

## How it works

1. Contributors add their change as a bullet under the `## Unreleased` heading in `CHANGELOG.md`, instead of hand-editing `Chart.yaml`'s version or writing dates into the changelog themselves.
2. Once a PR has at least 1 approval, a user with write access comments `/merge` on it.
3. The `Version Bump` workflow ([.github/workflows/version-bump.yml](.github/workflows/version-bump.yml)) then:
   - checks the commenter has write access and the PR has at least 1 approval (skipped if the PR's base branch starts with `test/`, for demo purposes),
   - checks the PR is mergeable,
   - checks PR labels to decide the bump type (see below),
   - bumps `Chart.yaml`'s `version`,
   - renames `## Unreleased` to `## X.Y.Z (DD.MM.YYYY)` and re-adds a fresh empty `## Unreleased` heading,
   - commits that to the PR branch, then merges the PR into its base branch as a merge commit.
4. The `Checklist` workflow ([.github/workflows/checklist.yml](.github/workflows/checklist.yml)) posts a sticky PR comment showing whether `## Unreleased` already has a bullet, as a reminder before commenting `/merge`.

It can also be triggered manually via `workflow_dispatch` (no PR involved) to bump a branch directly, with an optional changelog note.

## Labels

- `no-version-bump`: skip the bump/changelog step entirely on `/merge`, go straight to merge.
- `minor-bump`: bump the minor version instead of patch.
- `major-bump`: bump the major version instead of patch.

`no-version-bump` combined with `minor-bump`/`major-bump`, or `minor-bump` combined with `major-bump`, both fail the run with an explanatory PR comment. No label at all defaults to a patch bump.

## Scripts

- [.github/scripts/bump_chart_version.py](.github/scripts/bump_chart_version.py): bumps the `version:` line in `Chart.yaml`.
- [.github/scripts/changelog_tool.py](.github/scripts/changelog_tool.py): checks/finalizes/inserts entries in the `## Unreleased` section of `CHANGELOG.md`.

## Trying it out

Open a PR that adds a bullet under `## Unreleased`, get it approved (or target a `test/*` base branch to skip that), then comment `/merge`.
