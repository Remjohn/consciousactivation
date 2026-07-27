# Release Container Integrity Report

Updated: 2026-07-14  
Status: `PASS_FOLDER`; ZIP not produced

The aligned release is emitted as the required
`delegation-contracts/1.1.0-rc.1` folder, not as a ZIP archive. Its
`RELEASE_RECEIPT.json` hashes every included file and records a deterministic
release digest. The root validator reports the legacy optional ZIP as absent;
no ZIP integrity claim is made for this batch.
