#!/usr/bin/env bash
# Runner job-start hook: reject PRs before checkout or any workflow step.
set -euo pipefail
if [[ ${GITHUB_REPOSITORY:-} != Rafalbanas/Cycling ||
      ${GITHUB_REF:-} != refs/heads/main ||
      ${GITHUB_WORKFLOW_REF:-} != Rafalbanas/Cycling/.github/workflows/ci-cd.yml@refs/heads/main ||
      ( ${GITHUB_EVENT_NAME:-} != push && ${GITHUB_EVENT_NAME:-} != workflow_dispatch ) ]]; then
    echo 'Production runner only accepts the main-branch deployment workflow.' >&2
    exit 1
fi
