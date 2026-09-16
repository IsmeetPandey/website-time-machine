# Change Detection Notes

Website Time Machine compares normalized text snapshots rather than raw HTML.

## Why normalize

Raw HTML often changes for reasons that are not meaningful to a reader, such as whitespace, markup structure, or generated presentation details. Normalized text gives the MVP a smaller and more interpretable signal.

## Current comparison

Each snapshot is fingerprinted with SHA-256. The next capture is compared with the previous snapshot using word-level change and a lightweight similarity measurement.

## Reading a change report

A changed fingerprint means the normalized content changed; it does not identify whether the change was important. Large word deltas can come from navigation, timestamps, cookie notices, or other dynamic content.

## Planned improvements

Screenshot history, DOM-aware diffs, resource changes, and a visual timeline can add context without replacing the stable text-snapshot primitive.
