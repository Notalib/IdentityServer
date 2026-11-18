# Nota builds of Duende IdentityServer

This fork publishes `Duende.IdentityServer.*` packages with Nota's in-house
patches to GitHub Packages (`https://nuget.pkg.github.com/Notalib/index.json`)
as version `X.Y.Z-nota`.

## How it works

`.github/workflows/nota-release.yml` runs daily (and on demand):

1. `discover.py` compares upstream `is-X.Y.Z` tags in
   [DuendeSoftware/products](https://github.com/DuendeSoftware/products) with
   the `is-X.Y.Z-nota` tags in this repository. For each release line
   (`major.minor`, 7.4 and later) it builds every stable release newer than the
   newest `-nota` build; a line without any `-nota` build only gets its latest
   release. Previews and release candidates are skipped.
2. For each selected version it checks out the upstream tag, applies
   `patches/*.patch` with `git am`, tags the result `is-X.Y.Z-nota` (MinVer
   derives the package version from it), runs the unit tests and packs
   `identity-server/src/*`.
3. Packages are pushed to GitHub Packages, then the tag and a GitHub release
   (with the `.nupkg` files) are created.

If a patch no longer applies, or tests fail, an issue is opened. If every patch
is already contained in upstream, the build is skipped with a warning — time to
retire the patch.

## Common tasks

- **Build a specific version:** Actions → *nota/identity-server-release* → Run
  workflow, enter `X.Y.Z`. Tick *dry-run* to only build and test.
- **Add or update a patch:** commit on top of an upstream tag and export it with
  `git format-patch -1 --zero-commit -o .github/nota/patches`.
- **Rebuild a version:** delete the `is-X.Y.Z-nota` tag, release and package
  versions, then run the workflow for that version.
- **Publishing fails with 403:** packages that existed before this repository
  published them must grant it access under Package settings → *Manage Actions
  access* with the **Write** role (adding a repository defaults to Read).
  Packages first created by this workflow get Admin access automatically.

## Patches

| Patch | Upstream status |
| --- | --- |
| `0001-use-refresh-token-service-error.patch` — return the error from `IRefreshTokenService.ValidateRefreshTokenAsync` instead of always `invalid_grant`. Needed by our session-limiting service, which reports its own error when a retired refresh token is used. | Proposed upstream: [DuendeSoftware discussion #659](https://github.com/orgs/DuendeSoftware/discussions/659) |
