"""
Build script for the DMP Corpus.

This script generates:

- RDF/Turtle metadata description of the dataset
- GitHub Pages website

Source of truth: CSV metadata table.
"""

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, XSD


BASE = "https://jmartinkova.github.io/DMP-corpus/"
DMPC = Namespace(BASE + "ontology#")
SCHEMA = Namespace("https://schema.org/")


COLUMN_ALIASES = {
    "Internal ID": ["Internal ID"],
    "Source": ["Source"],
    "Direct DMP Link": ["Direct DMP Link"],
    "Public ID": ["Public ID"],
    "Name": ["Name"],
    "Date of Creation": ["Date of Creation"],
    "Format": ["Format"],
    "Template": ["Template"],
    "Language": ["Language"],
    "License": ["License"],
    "Template correspondence": [
        "Parts/Questions according to template",
        "Parts/Quesions according to template",
    ],
    "Estimated completeness": [
        "Completeness",
        "Completeness (with relation to the template)",
    ],
    "Declared access level": [
        "Declared access level",
        "Declarated access level",
    ],
    "Notes": ["Notes", "notes"],
    "Tool": ["Tool"],
    "Figures": ["Figures"],
    "Tables": [
        "Tables",
        "Tables (beside first page of metadata)",
    ],
    "Lists": ["Lists"],
}


def clean_value(value):
    if pd.isna(value):
        return None

    text = str(value).strip()

    if not text or text.casefold() in {
        "nan",
        "none",
        "null",
    }:
        return None

    return text


def find_column(df, logical_name):
    for candidate in COLUMN_ALIASES[logical_name]:
        if candidate in df.columns:
            return candidate
    return None


def get_value(row, columns, logical_name):
    column = columns.get(logical_name)
    if column is None:
        return None
    return clean_value(row.get(column))


def normalize_date(value, row_number, warnings):
    """
    Return YYYY-MM-DD or None.

    Full ISO datetimes are shortened to their date part.
    Unknown-like values are treated as missing.
    """
    if value is None:
        return None

    normalized = value.strip()
    lowered = normalized.casefold()

    if lowered in {
        "",
        "unknown",
        "unk",
        "n/a",
        "na",
        "none",
        "null",
        "not known",
        "not available",
    }:
        return None

    iso_datetime_match = re.match(
        r"^(\d{4}-\d{2}-\d{2})[Tt ]",
        normalized,
    )
    if iso_datetime_match:
        normalized = iso_datetime_match.group(1)

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", normalized):
        try:
            parsed = pd.to_datetime(
                normalized,
                format="%Y-%m-%d",
                errors="raise",
            )
            return parsed.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            pass

    warnings.append(
        f"Row {row_number}: date {value!r} could not be normalized "
        f"to YYYY-MM-DD and was omitted."
    )
    return None


def parse_boolean(value, row_number, field, warnings):
    if value is None:
        return None

    normalized = value.casefold()

    true_values = {"yes", "true", "1", "y", "ano"}
    false_values = {"no", "false", "0", "n", "ne"}

    if normalized in true_values:
        return True

    if normalized in false_values:
        return False

    warnings.append(
        f"Row {row_number}: {field} value {value!r} could not be "
        f"converted to boolean and was omitted."
    )
    return None


def parse_integer(value, row_number, field, warnings):
    if value is None:
        return None

    try:
        return int(float(value.replace(",", ".")))
    except ValueError:
        warnings.append(
            f"Row {row_number}: {field} value {value!r} could not be "
            f"converted to integer and was omitted."
        )
        return None


def valid_http_uri(value):
    if value is None:
        return None

    if re.match(r"^https?://", value, flags=re.IGNORECASE):
        return value

    return None


def record_uri(internal_id):
    return BASE + "dmp/" + quote(internal_id, safe="") + "/"


def add_literal(graph, subject, predicate, value, datatype=None):
    if value is None:
        return

    if datatype is None:
        graph.add((subject, predicate, Literal(value)))
    else:
        graph.add((subject, predicate, Literal(value, datatype=datatype)))


def build_record(row, columns, row_number, warnings):
    internal_id = get_value(row, columns, "Internal ID")

    if internal_id is None:
        warnings.append(
            f"Row {row_number}: skipped because Internal ID is empty."
        )
        return None

    direct_link_raw = get_value(row, columns, "Direct DMP Link")
    direct_link = valid_http_uri(direct_link_raw)

    if direct_link_raw and direct_link is None:
        warnings.append(
            f"Row {row_number}: Direct DMP Link value "
            f"{direct_link_raw!r} is not an HTTP(S) URL and was omitted."
        )

    return {
        "internal_id": internal_id,
        "uri": record_uri(internal_id),
        "source": get_value(row, columns, "Source"),
        "direct_link": direct_link,
        "public_id": get_value(row, columns, "Public ID"),
        "name": get_value(row, columns, "Name"),
        "date": normalize_date(
            get_value(row, columns, "Date of Creation"),
            row_number,
            warnings,
        ),
        "format": get_value(row, columns, "Format"),
        "template": get_value(row, columns, "Template"),
        "language": get_value(row, columns, "Language"),
        "license": get_value(row, columns, "License"),
        "template_correspondence": parse_integer(
            get_value(row, columns, "Template correspondence"),
            row_number,
            "Template correspondence",
            warnings,
        ),
        "estimated_completeness": parse_integer(
            get_value(row, columns, "Estimated completeness"),
            row_number,
            "Estimated completeness",
            warnings,
        ),
        "declared_access_level": get_value(
            row,
            columns,
            "Declared access level",
        ),
        "notes": get_value(row, columns, "Notes"),
        "tool": get_value(row, columns, "Tool"),
        "figures": parse_boolean(
            get_value(row, columns, "Figures"),
            row_number,
            "Figures",
            warnings,
        ),
        "tables": parse_boolean(
            get_value(row, columns, "Tables"),
            row_number,
            "Tables",
            warnings,
        ),
        "lists": parse_boolean(
            get_value(row, columns, "Lists"),
            row_number,
            "Lists",
            warnings,
        ),
    }


def add_record_to_graph(graph, record):
    subject = URIRef(record["uri"])

    graph.add((subject, RDF.type, DMPC.DMPRecord))
    add_literal(
        graph,
        subject,
        DCTERMS.identifier,
        record["internal_id"],
    )
    add_literal(
        graph,
        subject,
        DCTERMS.identifier,
        record["public_id"],
    )
    add_literal(graph, subject, DCTERMS.title, record["name"])
    add_literal(graph, subject, DCTERMS.source, record["source"])
    add_literal(graph, subject, DCTERMS.format, record["format"])
    add_literal(graph, subject, DCTERMS.language, record["language"])
    add_literal(graph, subject, DCTERMS.license, record["license"])
    add_literal(graph, subject, DCTERMS.description, record["notes"])

    if record["date"] is not None:
        add_literal(
            graph,
            subject,
            DCTERMS.created,
            record["date"],
            datatype=XSD.date,
        )

    if record["direct_link"] is not None:
        graph.add(
            (
                subject,
                SCHEMA.url,
                URIRef(record["direct_link"]),
            )
        )

    add_literal(graph, subject, DMPC.template, record["template"])
    add_literal(
        graph,
        subject,
        DMPC.templateCorrespondence,
        record["template_correspondence"],
        datatype=XSD.integer,
    )
    add_literal(
        graph,
        subject,
        DMPC.estimatedCompleteness,
        record["estimated_completeness"],
        datatype=XSD.integer,
    )
    add_literal(
        graph,
        subject,
        DMPC.declaredAccessLevel,
        record["declared_access_level"],
    )
    add_literal(graph, subject, DMPC.creationTool, record["tool"])
    add_literal(
        graph,
        subject,
        DMPC.hasFigures,
        record["figures"],
        datatype=XSD.boolean,
    )
    add_literal(
        graph,
        subject,
        DMPC.hasTables,
        record["tables"],
        datatype=XSD.boolean,
    )
    add_literal(
        graph,
        subject,
        DMPC.hasLists,
        record["lists"],
        datatype=XSD.boolean,
    )


def jsonld_for_record(record):
    data = {
        "@context": {
            "dcterms": "http://purl.org/dc/terms/",
            "schema": "https://schema.org/",
            "dmpc": BASE + "ontology#",
            "title": "dcterms:title",
            "identifier": "dcterms:identifier",
            "created": {
                "@id": "dcterms:created",
                "@type": "http://www.w3.org/2001/XMLSchema#date",
            },
            "source": "dcterms:source",
            "format": "dcterms:format",
            "language": "dcterms:language",
            "license": "dcterms:license",
            "description": "dcterms:description",
            "url": {
                "@id": "schema:url",
                "@type": "@id",
            },
            "template": "dmpc:template",
            "templateCorrespondence": "dmpc:templateCorrespondence",
            "estimatedCompleteness": "dmpc:estimatedCompleteness",
            "declaredAccessLevel": "dmpc:declaredAccessLevel",
            "creationTool": "dmpc:creationTool",
            "hasFigures": "dmpc:hasFigures",
            "hasTables": "dmpc:hasTables",
            "hasLists": "dmpc:hasLists",
        },
        "@id": record["uri"],
        "@type": "dmpc:DMPRecord",
        "identifier": [
            value
            for value in [
                record["internal_id"],
                record["public_id"],
            ]
            if value is not None
        ],
    }

    mapping = {
        "title": record["name"],
        "created": record["date"],
        "source": record["source"],
        "format": record["format"],
        "language": record["language"],
        "license": record["license"],
        "description": record["notes"],
        "url": record["direct_link"],
        "template": record["template"],
        "templateCorrespondence": record["template_correspondence"],
        "estimatedCompleteness": record["estimated_completeness"],
        "declaredAccessLevel": record["declared_access_level"],
        "creationTool": record["tool"],
        "hasFigures": record["figures"],
        "hasTables": record["tables"],
        "hasLists": record["lists"],
    }

    for key, value in mapping.items():
        if value is not None:
            data[key] = value

    return data


def display_value(value):
    if value is None:
        return "—"

    if isinstance(value, bool):
        return "Yes" if value else "No"

    return str(value)


def detail_row(label, value, raw_html=False, class_name=None):
    if value is None:
        return ""

    if raw_html:
        rendered = value
    else:
        rendered = html.escape(display_value(value))

    class_attr = (
        f' class="{html.escape(class_name, quote=True)}"'
        if class_name
        else ""
    )

    return (
        "        <dt>"
        + html.escape(label)
        + "</dt>\n"
        f"        <dd{class_attr}>"
        + rendered
        + "</dd>\n"
    )


def score_badge(value):
    if value is None:
        return None

    score = max(0, min(100, value))

    if score == 100:
        level = "complete"
    elif score >= 75:
        level = "high"
    elif score >= 50:
        level = "medium"
    else:
        level = "low"

    return (
        f'<span class="score score-{level}" '
        f'aria-label="{score} percent">{score}%</span>'
    )


def boolean_badge(value):
    if value is None:
        return None

    label = "Yes" if value else "No"
    state = "yes" if value else "no"
    return f'<span class="badge badge-{state}">{label}</span>'


def render_record_page(record):
    title = record["name"] or f"DMP {record['internal_id']}"
    jsonld = json.dumps(
        jsonld_for_record(record),
        ensure_ascii=False,
        indent=2,
    ).replace("</", "<\\/")

    original_link = None
    if record["direct_link"] is not None:
        escaped_url = html.escape(record["direct_link"], quote=True)
        original_link = (
            f'<a href="{escaped_url}" rel="noopener noreferrer">'
            "Open original DMP"
            "</a>"
        )

    rows = ""
    rows += detail_row("Internal ID", record["internal_id"])
    rows += detail_row("Public ID", record["public_id"])
    rows += detail_row("Date of creation", record["date"])
    rows += detail_row("Source", record["source"])
    rows += detail_row("Format", record["format"])
    rows += detail_row("Template", record["template"])
    rows += detail_row(
        "Template correspondence",
        score_badge(record["template_correspondence"]),
        raw_html=True,
        class_name="score-cell",
    )
    rows += detail_row(
        "Estimated completeness",
        score_badge(record["estimated_completeness"]),
        raw_html=True,
        class_name="score-cell",
    )
    rows += detail_row("Language", record["language"])
    rows += detail_row("License", record["license"])
    rows += detail_row(
        "Declared access level",
        record["declared_access_level"],
    )
    rows += detail_row("Creation tool", record["tool"])
    rows += detail_row(
        "Figures",
        boolean_badge(record["figures"]),
        raw_html=True,
    )
    rows += detail_row(
        "Tables",
        boolean_badge(record["tables"]),
        raw_html=True,
    )
    rows += detail_row(
        "Lists",
        boolean_badge(record["lists"]),
        raw_html=True,
    )
    rows += detail_row(
        "Notes",
        record["notes"],
        class_name="notes",
    )
    rows += detail_row("Original document", original_link, raw_html=True)

    canonical = html.escape(record["uri"], quote=True)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} — DMP Corpus</title>
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="../../assets/style.css">
  <script type="application/ld+json">
{jsonld}
  </script>
</head>
<body>
  <header class="site-header">
    <a href="../../">DMP Corpus</a>
  </header>

  <main>
    <p class="eyebrow">Data Management Plan record</p>
    <h1>{html.escape(title)}</h1>
    <p class="uri"><code>{canonical}</code></p>

    <dl class="metadata">
{rows}    </dl>

    <nav class="record-nav">
      <a href="../../records.html">All records</a>
      <a href="../../data/dmp_corpus_v1.ttl">RDF/Turtle dataset</a>
      <a href="../../ontology_dmpc.ttl">Ontology</a>
    </nav>
  </main>
</body>
</html>
"""


def render_home_page(record_count, codebook_filename="codebook.md"):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DMP Corpus</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header class="site-header">
    <span>DMP Corpus</span>
  </header>

  <main>
    <p class="eyebrow">Curated metadata dataset</p>
    <h1>DMP Corpus</h1>

    <p class="lede">
      A curated metadata corpus describing publicly accessible
      Data Management Plans.
    </p>

    <p>
      This version contains {record_count} records. The repository publishes
      metadata only; original DMP documents are not redistributed.
    </p>

    <div class="link-grid">
      <a class="card" href="records.html">
        <strong>Browse records</strong>
        <span>Open the human-readable page for each DMP.</span>
      </a>

      <a class="card" href="data/dmp_corpus_v1.csv">
        <strong>CSV dataset</strong>
        <span>Download the tabular source dataset.</span>
      </a>

      <a class="card" href="data/dmp_corpus_v1.ttl">
        <strong>RDF/Turtle dataset</strong>
        <span>Download the complete RDF representation.</span>
      </a>

      <a class="card" href="ontology_dmpc.ttl">
        <strong>DMP Corpus ontology</strong>
        <span>Open the custom vocabulary used by the dataset.</span>
      </a>

      <a class="card" href="{html.escape(codebook_filename, quote=True)}">
        <strong>Codebook</strong>
        <span>Read the metadata field definitions.</span>
      </a>
    </div>
  </main>
</body>
</html>
"""


def render_records_page(records):
    items = []

    for record in sorted(
        records,
        key=lambda item: (
            (item["name"] or "").casefold(),
            item["internal_id"],
        ),
    ):
        title = record["name"] or f"DMP {record['internal_id']}"
        identifier = quote(record["internal_id"], safe="")
        metadata = []

        if record["date"] is not None:
            metadata.append(record["date"])

        if record["language"] is not None:
            metadata.append(record["language"])

        secondary = " · ".join(metadata)
        secondary_html = (
            f'<span class="record-meta">{html.escape(secondary)}</span>'
            if secondary
            else ""
        )

        items.append(
            "      <li>\n"
            f'        <a href="dmp/{identifier}/">'
            f"{html.escape(title)}</a>\n"
            f"        {secondary_html}\n"
            "      </li>"
        )

    list_html = "\n".join(items)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Records — DMP Corpus</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header class="site-header">
    <a href="./">DMP Corpus</a>
  </header>

  <main>
    <p class="eyebrow">Dataset index</p>
    <h1>Records</h1>
    <p>{len(records)} DMP metadata records.</p>

    <ol class="record-list">
{list_html}
    </ol>
  </main>
</body>
</html>
"""


STYLE_CSS = r"""
:root {
  color-scheme: light;
  font-family:
    Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  line-height: 1.55;
  color: #172033;
  background: #f7f8fb;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
}

a {
  color: #2457c5;
}

.site-header {
  padding: 1rem max(1.25rem, calc((100vw - 920px) / 2));
  background: #ffffff;
  border-bottom: 1px solid #dfe3eb;
  font-weight: 700;
}

main {
  width: min(920px, calc(100% - 2.5rem));
  margin: 0 auto;
  padding: 4rem 0 6rem;
}

h1 {
  margin-top: 0.25rem;
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.05;
}

.eyebrow {
  margin-bottom: 0;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  font-size: 0.8rem;
  font-weight: 700;
  color: #647087;
}

.lede {
  max-width: 42rem;
  font-size: 1.25rem;
}

.link-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.card {
  display: block;
  padding: 1.25rem;
  color: inherit;
  text-decoration: none;
  background: #ffffff;
  border: 1px solid #dfe3eb;
  border-radius: 0.75rem;
  transition:
    border-color 160ms ease,
    box-shadow 160ms ease,
    transform 160ms ease;
}

.card:hover {
  border-color: #2457c5;
  box-shadow: 0 8px 24px rgb(36 87 197 / 10%);
  transform: translateY(-2px);
}

.card strong,
.card span {
  display: block;
}

.card span {
  margin-top: 0.5rem;
  color: #5d687d;
}

.uri {
  overflow-wrap: anywhere;
  color: #5d687d;
}

.metadata {
  display: grid;
  grid-template-columns: minmax(160px, 220px) 1fr;
  margin: 2.5rem 0;
  background: #ffffff;
  border: 1px solid #dfe3eb;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 10px 30px rgb(23 32 51 / 6%);
}

.metadata dt,
.metadata dd {
  margin: 0;
  padding: 0.9rem 1rem;
  border-bottom: 1px solid #e7eaf0;
}

.metadata dt {
  font-weight: 700;
  background: #f1f3f7;
}

.metadata dt:last-of-type,
.metadata dd:last-of-type {
  border-bottom: 0;
}

.score-cell {
  display: flex;
  align-items: center;
}

.score,
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 3.5rem;
  padding: 0.28rem 0.7rem;
  border-radius: 999px;
  font-size: 0.88rem;
  font-weight: 750;
  line-height: 1.2;
  letter-spacing: 0.01em;
  border: 1px solid transparent;
}

.score-complete {
  color: #12603a;
  background: #dcf8e9;
  border-color: #a9e7c8;
}

.score-high {
  color: #174ea6;
  background: #e5efff;
  border-color: #bdd2fa;
}

.score-medium {
  color: #7a4a00;
  background: #fff3cd;
  border-color: #f2d98b;
}

.score-low {
  color: #8b2635;
  background: #fde7eb;
  border-color: #f2bcc6;
}

.badge-yes {
  color: #12603a;
  background: #dcf8e9;
  border-color: #a9e7c8;
}

.badge-no {
  color: #596273;
  background: #f1f3f6;
  border-color: #d8dde6;
}

.notes {
  position: relative;
  margin: 0.8rem 1rem !important;
  padding: 0.9rem 1rem 0.9rem 1.15rem !important;
  color: #536078;
  background: #fafbfe;
  border: 0 !important;
  border-left: 4px solid #aab7d4 !important;
  border-radius: 0.35rem;
  font-style: italic;
  white-space: pre-line;
}

.record-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.record-list {
  padding-left: 1.5rem;
}

.record-list li {
  padding: 0.55rem 0;
}

.record-meta {
  margin-left: 0.5rem;
  color: #68748a;
  font-size: 0.9rem;
}

@media (max-width: 640px) {
  main {
    padding-top: 2.5rem;
  }

  .metadata {
    display: block;
  }

  .metadata dt {
    border-bottom: 0;
  }

  .metadata dd {
    padding-top: 0;
  }

  .score-cell {
    padding-top: 0.25rem !important;
  }

  .notes {
    margin-top: 0 !important;
  }
}
""".strip() + "\n"


def copy_optional_file(source, destination):
    if source is None:
        return False

    source_path = Path(source)
    if not source_path.exists():
        return False

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination)
    return True


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Build the DMP Corpus GitHub Pages site and RDF/Turtle "
            "dataset from a CSV file."
        )
    )
    parser.add_argument(
        "input_csv",
        help="Path to the source CSV file",
    )
    parser.add_argument(
        "--output-dir",
        default="docs",
        help="GitHub Pages output directory (default: docs)",
    )
    parser.add_argument(
        "--ontology",
        help="Optional path to ontology_dmpc.ttl",
    )
    parser.add_argument(
        "--codebook",
        help="Optional path to a Markdown or HTML codebook to copy",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete the output directory before rebuilding",
    )
    args = parser.parse_args()

    input_path = Path(args.input_csv)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    if args.clean and output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "assets").mkdir(parents=True, exist_ok=True)
    (output_dir / "data").mkdir(parents=True, exist_ok=True)
    (output_dir / "dmp").mkdir(parents=True, exist_ok=True)

    try:
        df = pd.read_csv(input_path, dtype=str, keep_default_na=True)
    except Exception as exc:
        print(f"Error while reading CSV: {exc}", file=sys.stderr)
        return 1

    columns = {
        logical_name: find_column(df, logical_name)
        for logical_name in COLUMN_ALIASES
    }

    if columns["Internal ID"] is None:
        print(
            "Error: the CSV must contain an 'Internal ID' column.",
            file=sys.stderr,
        )
        return 1

    warnings = []
    records = []

    for index, row in df.iterrows():
        record = build_record(
            row,
            columns,
            index + 2,
            warnings,
        )

        if record is not None:
            records.append(record)

    graph = Graph()
    graph.bind("dcterms", DCTERMS)
    graph.bind("schema", SCHEMA)
    graph.bind("dmpc", DMPC)

    for record in records:
        add_record_to_graph(graph, record)

    ttl_path = output_dir / "data" / "dmp_corpus_v1.ttl"
    graph.serialize(destination=ttl_path, format="turtle")

    shutil.copy2(
        input_path,
        output_dir / "data" / "dmp_corpus_v1.csv",
    )

    for record in records:
        identifier = quote(record["internal_id"], safe="")
        record_dir = output_dir / "dmp" / identifier
        record_dir.mkdir(parents=True, exist_ok=True)
        (record_dir / "index.html").write_text(
            render_record_page(record),
            encoding="utf-8",
        )

    codebook_filename = (
        Path(args.codebook).name
        if args.codebook
        else "codebook.md"
    )

    (output_dir / "index.html").write_text(
        render_home_page(len(records), codebook_filename),
        encoding="utf-8",
    )
    (output_dir / "records.html").write_text(
        render_records_page(records),
        encoding="utf-8",
    )
    (output_dir / "assets" / "style.css").write_text(
        STYLE_CSS,
        encoding="utf-8",
    )

    ontology_copied = copy_optional_file(
        args.ontology,
        output_dir / "ontology_dmpc.ttl",
    )
    codebook_copied = copy_optional_file(
        args.codebook,
        output_dir / codebook_filename,
    )

    if warnings:
        warning_path = output_dir / "build.warnings.txt"
        warning_path.write_text(
            "\n".join(warnings) + "\n",
            encoding="utf-8",
        )

    print(f"Built {len(records)} record pages in {output_dir}")
    print(f"Generated {len(graph)} RDF triples.")
    print(f"Turtle dataset: {ttl_path}")
    print(f"CSV copy: {output_dir / 'data' / 'dmp_corpus_v1.csv'}")

    if warnings:
        print(
            f"{len(warnings)} non-fatal warnings: "
            f"{output_dir / 'build.warnings.txt'}"
        )

    if args.ontology and not ontology_copied:
        print(
            f"Warning: ontology file was not found: {args.ontology}",
            file=sys.stderr,
        )

    if args.codebook and not codebook_copied:
        print(
            f"Warning: codebook file was not found: {args.codebook}",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())