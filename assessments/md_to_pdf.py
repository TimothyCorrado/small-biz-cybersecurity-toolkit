"""
Simple Markdown → PDF converter.

Usage:
    python md_to_pdf.py input.md output.pdf

Requirements:
    pip install markdown pdfkit
    Install wkhtmltopdf (https://wkhtmltopdf.org/)
"""

import argparse
import os
import sys

import markdown
import pdfkit


def build_html(markdown_text: str, title: str = "Report") -> str:
    """Wrap markdown-converted HTML with a basic styled HTML document."""
    body = markdown.markdown(
        markdown_text,
        extensions=["tables", "fenced_code"],
    )

    # Simple, clean styling for reports
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{title}</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      font-size: 11pt;
      line-height: 1.4;
      color: #222222;
      max-width: 800px;
      margin: 40px auto;
    }}
    h1, h2, h3 {{
      font-weight: bold;
      color: #111111;
      margin-top: 1.4em;
      margin-bottom: 0.5em;
    }}
    h1 {{
      font-size: 20pt;
      border-bottom: 1px solid #cccccc;
      padding-bottom: 6px;
    }}
    h2 {{
      font-size: 16pt;
      border-bottom: 1px solid #e0e0e0;
      padding-bottom: 4px;
    }}
    h3 {{
      font-size: 13pt;
    }}
    p {{
      margin: 0.3em 0 0.6em 0;
    }}
    ul, ol {{
      margin: 0.2em 0 0.6em 1.5em;
    }}
    table {{
      border-collapse: collapse;
      margin: 0.8em 0;
      width: 100%;
    }}
    th, td {{
      border: 1px solid #cccccc;
      padding: 6px 8px;
      text-align: left;
    }}
    th {{
      background-color: #f5f5f5;
      font-weight: bold;
    }}
    code {{
      font-family: Consolas, "Courier New", monospace;
      font-size: 10pt;
      background: #f2f2f2;
      padding: 1px 3px;
      border-radius: 3px;
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""
    return html


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to a styled PDF report."
    )
    parser.add_argument("input_md", help="Path to input Markdown file")
    parser.add_argument("output_pdf", help="Path to output PDF file")
    parser.add_argument(
        "--wkhtmltopdf",
        help="Optional path to wkhtmltopdf binary if not in PATH",
        default=None,
    )

    args = parser.parse_args()

    if not os.path.isfile(args.input_md):
        print(f"[!] Input file not found: {args.input_md}")
        sys.exit(1)

    with open(args.input_md, "r", encoding="utf-8") as f:
        md_text = f.read()

    title = os.path.splitext(os.path.basename(args.input_md))[0]
    html = build_html(md_text, title=title)

    # Configure wkhtmltopdf if a path is provided
    if args.wkhtmltopdf:
        config = pdfkit.configuration(wkhtmltopdf=args.wkhtmltopdf)
    else:
        config = None  # assumes wkhtmltopdf is in PATH

    try:
        pdfkit.from_string(html, args.output_pdf, configuration=config)
        print(f"[+] PDF written to: {args.output_pdf}")
    except OSError as e:
        print("[!] Failed to generate PDF.")
        print("    Make sure wkhtmltopdf is installed and accessible.")
        print(f"    Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
