# First-half visual adjudication

Reviewed 28 IDs: sort baseline entries with `verdict == needs-user-review`, exclude structural records, ordinary entries, and the three parent-handled IDs, then take the first 28 of the remaining 56. Scope runs arctic-ocean through namibia.

- **26 preview-accepted-with-limitations.** Ordinary palette, texture, geometric simplification, and promotional realism differences are accepted as disclosed miniature styling, not deferred for taste approval.
- **2 substantive-feature-hold:** Indonesia (named copper openwork is not reliably readable in actual closed views); Morocco (named ceramic interlocking/border fidelity remains unresolved in partial v6). Neither is a claim that the relevant geometry is absent.
- All 28 exact comparison boards were extracted with `git show commit:path` and SHA256 validated. Seven readable contact sheets were inspected using vision; Atlantic Ocean, Brazil, and Indonesia also received individual-board inspection. Independent-review observations were read for every ID.
- Closer inspection resolves Atlantic Ocean's low split ridge and Brazil's winding wooded channel as present, with reduced relief/readability. Central African Republic's small water detail is a pond/clearing motif: an extended river is not imposed as a new requirement.

`decisions.json` contains the required per-ID disposition, meaningful issue, rationale, and exact board commit/path/hash. `scope.json`, `observations.json`, extracted `boards/`, contact sheets, and two local scripts support this short review only; they do not create a new acceptance graph.

No artwork, models, viewers, or files outside visual-a were changed. No fresh runtime/mechanical/source-parity tests were performed. Hidden exterior ornament in open-lid views is not judged missing. Ambiguous hinge silhouettes are not diagnosed as detached components. Separate preservation/archive holds, including Morocco and Namibia, remain untouched. Preview acceptance is not final user approval, publication, sale, mint, or release authorization.

Tool issue: the initial helper filename shadowed Python's inspect module during Pillow import. Renaming it to prepare_boards.py resolved the issue; extraction/hash validation and sheet generation then completed successfully.
