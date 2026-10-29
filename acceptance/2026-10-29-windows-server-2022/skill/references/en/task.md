# Task rules

TRIAGE-1

## Input

Plain text with one item per line. Reading order is document order.

## Classification

Look at the line start only, never at meaning.

- TRIAGE-2 Goes to `TODO` when the line starts with `TODO:`.
- TRIAGE-3 Goes to `DONE` when the line starts with `DONE:`.
- TRIAGE-4 Goes to `BLOCKED` when the line starts with `BLOCKED:`.
- TRIAGE-5 Goes to `UNMARKED` when none of the three matches.

TRIAGE-6 Matching is strictly literal: the marker must sit at the first character of the line, the keyword must be upper case, and it must be followed directly by an ASCII colon `:`. A space after the colon is optional. `todo:`, `Todo:`, `TODO :`, `(TODO:`, `todo TODO:`, and any ` TODO:` that starts with a space or indentation are not markers and go to `UNMARKED`.

TRIAGE-7 Do not infer status from content. Lines saying "already done", "waiting for login" or "skip for now" without a line-start marker still go to `UNMARKED`. Never rewrite, complete or polish a line.

## Preservation

- TRIAGE-8 Preserve each line verbatim: marker, spacing after the colon, punctuation, full-width characters and inner spacing stay unchanged.
- TRIAGE-9 Inside a group keep the original relative order of the items.
- TRIAGE-10 Empty and whitespace-only lines are not items: skip them, do not group them, do not count them.

## Output

TRIAGE-11 Output a Markdown document with exactly four level-2 headings in this order: `TODO`, `DONE`, `BLOCKED`, `UNMARKED`. Use the upper-case group name with the count in parentheses, for example `## TODO (2)`.

TRIAGE-12 List items under each heading as `- ` bullets, verbatim. When a group is empty, still print the heading with `(0)` and use `- (none)` as its body.

TRIAGE-13 Start the document with the level-1 heading `# Note triage` and add no summary, advice or extra sections after it.
