# Acceptance

ACC-1

## Purpose

This file is for recipient self-check. The recipient needs only three things: this skill directory, one multi-line text, and the instruction "use this skill to process the input and save the result".

## Checks

- ACC-2 Grouping: classification follows line-start markers only, all four groups present, headings formatted as `## TODO (n)`.
- ACC-3 Text: every item is character-for-character identical to its input line, marker included.
- ACC-4 Order: items inside a group keep input order.
- ACC-5 Counts: the number in parentheses equals the real number of items in that group, and the four counts add up to the number of non-empty lines.

## Done criteria

ACC-6 All four checks must pass. When one fails, record the difference between actual output and the input line first, then fix the rule or the implementation; never edit the sample.

## Out of scope

The skill handles line-start markers only. It does not judge real task status, does not use the network, does not read other files, and writes nothing except the result file.
