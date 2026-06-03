# VaultGhost™ v0.1.1 Post-Release Status

## Publication Details
- **Version:** v0.1.1
- **Release Branch:** `release/v0.1.1` (Isolated orphan branch)
- **Release Tag:** `v0.1.1`
- **Repository:** [drosenbluth25/vaultghost-protocol](https://github.com/drosenbluth25/vaultghost-protocol)

## Status Summary
- **Isolation:** v0.1.1 was published from the isolated branch `release/v0.1.1`.
- **Integrity:** The `main` branch was not overwritten, and no repository rules were disabled during this process.
- **Snapshot:** The tag `v0.1.1` correctly points to the v0.1.1 protocol snapshot.
- **Zip Artifact:** The release includes the verified zip artifact with SHA-256 `b5aceef407bc4717db787660db40559fd880ce69c99dc94b8bdd49ed8d4dd347`.

## Integration Limitations & Manual Actions
- **Workflow Permissions:** The `.github/workflows/release-check.yml` file is present in the tag and the release zip. However, it could not be pushed to the remote branch due to GitHub App workflow permission restrictions. A user or account with `workflows` permission must push this file if active CI on the branch is required.
- **GitHub Pages:** Automatic enablement via CLI was restricted (403). Pages must be manually enabled from **Settings → Pages** (Source: `release/v0.1.1` branch, Folder: `/docs`).
- **Protocol Semantics:** No changes were made to the core protocol logic, schemas, or fixtures.
