---
name: paper-compile
description: Compile a LaTeX research manuscript, repair source-level build failures, and verify the rendered PDF against named-venue or venue-neutral requirements. Use when building paper/main.pdf, diagnosing LaTeX or bibliography errors, and checking references, fonts, overflow, and visual layout.
---

# Paper Compile

Build the manuscript and report what was actually checked.

## Establish the build

Inspect the repository's documented build command and available LaTeX engine first. Prefer the existing build path. When none exists, use latexmk with the engine required by the manuscript. Do not install a large TeX distribution or replace venue files without user approval.

Clean only generated build artifacts. Preserve source, figures, and bibliography files.

## Diagnose with a bounded loop

Run at most three compile-and-fix attempts for a given failure class:

1. capture the complete log;
2. locate the first actionable source error;
3. apply the smallest source fix;
4. rebuild from the documented entry point.

If the same failure remains after two focused fixes, stop broad editing and report the exact source location and log excerpt.

## Verify the actual PDF

After a successful build:

- confirm paper/main.pdf exists and opens;
- check undefined citations and references, missing figures, and unresolved placeholders;
- for a named venue, verify current page-limit and anonymity rules against the official venue source; for `venue-neutral`, record both checks as not applicable rather than stopping;
- inspect embedded fonts and severe overfull content with available local tools;
- render and visually inspect every page for clipping, unreadable figures, broken equations, blank pages, misplaced floats, and inconsistent margins;
- distinguish main text, references, and appendix when reporting page count.

Write paper/COMPILE_REPORT.md with the command, engine, result, page count, checks actually run, remaining warnings, and any uninspected item. Do not claim visual verification from a successful exit code alone.

Route content compression or narrative changes to paper-polish; keep this skill focused on build and rendering defects.
