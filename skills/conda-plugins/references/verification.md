# Verify evidence and release artifacts

When a plugin verifies attestations, archives, or cached evidence, give each check a distinct result. A cryptographically valid signature alone does not establish artifact identity, accepted statement content, or publisher authorization.

## Apply checks in order

Apply the protocol's required checks in this order:

1. Select the expected source and enforce the configured online or offline policy.
2. Bound transport, decompression, and parser input. Check declared lengths and count actual streamed bytes. Reject oversized data before allocating or parsing the whole document.
3. If authenticated metadata advertises the evidence digest, verify that digest over the fetched bytes before interpreting them. An advertised but invalid object is an error, not a reason to accept weaker evidence.
4. Parse the bounded verification envelope and verify its cryptographic evidence with the intended trust roots and time policy.
5. Validate the authenticated statement's type and required fields, then bind its subject digest to the actual artifact being checked.
6. Apply the caller's accepted signer identities, issuer, predicate type, and authorization policy.
7. Cache only the result appropriate to those checks. Keep raw evidence storage distinct from a trusted acceptance decision.

Use the supported verification library for cryptography. Keep parsing needed for cryptographic verification inside that library. Do not act on unverified statement fields.

A generic verification helper should return verified evidence and identity. The application decides whether that evidence meets its own policy. Do not bake one caller's predicate policy into a general envelope verifier.

A content-addressed cache proves which bytes were stored, not that those bytes remain acceptable under current policy. Revalidate data after reading it, account for trust-policy changes and expiry, and write atomically. In offline mode, fail clearly when acceptable cached evidence is unavailable. Do not silently access the network.

## Separate archive integrity from metadata checks

Before publishing a built archive, check its complete compressed stream as well as package metadata. A metadata reader can succeed before reaching a truncated gzip trailer. Computing a checksum of that file binds the truncated bytes without proving the archive is usable. Use the archive format's integrity checker, then hash and upload those same files. For a downloaded artifact, an expected authenticated digest must still be checked before parsing or extracting it. Metadata validity, transport integrity, artifact binding, and authorization answer different questions.

Use a truncated archive with readable package metadata to test this distinction. Confirm the stream-integrity stage rejects it, not merely that an unrelated metadata error causes failure. Retire results when a custom build helper is replaced by another tool; successful tests of removed code do not validate the replacement.

## Test rejection stages

Build failure tests around the stage that must reject the input:

| Case | Required observation |
| --- | --- |
| Oversized stream or decompressed input | Stops before unbounded allocation or statement processing |
| Digest mismatch | No statement use or trusted cache entry |
| Valid signature, wrong artifact | Artifact binding fails |
| Correct artifact, unapproved identity or predicate | Authorization fails |
| Malformed or corrupted cache | Rejected or refreshed only when online policy allows |
| Offline cache miss | No request, explicit unavailable-evidence result |
| Failed temporary write or interrupted operation | Previous cache remains usable, no partial trusted result |
| Untrusted URL or exception text | No credentials in logs and no interpreted terminal markup |

Use local fixtures and the repository's existing verifier fakes to reach each stage. A test that fails at parsing does not prove the authorization check works.

Use [testing.md](testing.md) for runtime setup, regression-test conventions, and the repository checks required before completion.

## Order release jobs and preserve artifacts

For a plugin publishing Python distributions and a conda package, express the required order through CI job dependencies:

1. Run the complete reusable test workflow on the release commit, including the required native matrix, artifact, documentation, and workflow checks.
2. After all required jobs succeed, validate tag identity and the [resolved package version](architecture.md#share-the-resolved-package-version), then build and test the release wheel and sdist once.
3. Record provenance for those exact artifacts, retain their digests, and prepare the GitHub draft if the project's release process uses one.
4. Publish those Python artifacts through the configured protected publisher.
5. Build and test the conda package from the published sdist, verifying the digest recorded by the Python build. Preserve the version stored in that archive.
6. Attest and verify the exact conda artifact before its protected upload. Finalize the GitHub draft only after both package publications succeed.

An independent tag-triggered test workflow can still be running when a publisher starts. Make the release depend on the reusable test workflow's completion, rather than launching tests beside publication or polling historical runs. Preserve the target repository's release trigger and approval rules. Passing preparation checks does not authorize tagging, pushing, credentials changes, or publication.

Use the package index's actual normalized source URL. Retry transient download failures with bounded attempts and timeouts, then check the expected digest. A digest mismatch is a verification failure. Use existing download, archive, backend, and checksum tools instead of a custom release framework when they cover the required checks.

Verify publication evidence against the exact package digest, expected repository and signer workflow, source commit and ref, OIDC issuer, predicate type, and claimed target channel. Keep bundles with their artifacts. Public attestations disclose signer identities and artifact metadata. They provide evidence about those bytes and identities, without certifying package safety or enabling automatic verification in users' conda installations.

Configure publisher credentials and environment protection separately from workflow definitions. Reusable workflows must declare and receive required secrets explicitly. Pin actions to full commit SHAs, scope permissions to the jobs that need them, and preserve checks that refuse an existing or unverifiable channel release. Disable upload force overrides and user configuration that could change the destination. Follow the project's declared success criteria for normal uploads. Add post-upload polling or fresh channel installations only when they serve a required check.

## Recover a partial publication

Publication across indexes is not atomic. Inspect the failing stage and each destination before retrying an ambiguous upload. A failed final verification step can follow a successful upload.

Preserve the original artifacts and signing evidence. Compare existing filenames, versions, and digests before deciding what remains to publish. An existing filename alone is not a safe reason to skip an upload, and an uncertain result is not a reason to force it. If only GitHub finalization failed, confirm both package publications and finalize the existing draft without rebuilding or uploading again. Keep released tags and published bytes unchanged. Recovery that publishes or changes a release requires authorization for those actions.
