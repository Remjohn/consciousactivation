# Book Source Preparation Tools

Use the PDF→Markdown converter when the assigned book exists as PDF. The Markdown becomes the local processing representation; the PDF remains the source artifact.

Recommended command:

```bash
python tools/prepare_book_markdown.py --input <book.pdf> --output <book.md> --overwrite
```

The converter is intentionally deterministic and records page boundaries where the PDF extractor exposes them.
