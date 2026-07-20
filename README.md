# DMP Corpus

A curated corpus of publicly available Data Management Plans (DMPs)
collected from multiple repositories and manually reviewed for
structural and metadata characteristics.

🌐 Project website:

https://jmartinkova.github.io/DMP-corpus/

---

## About

The DMP Corpus is a curated metadata dataset describing publicly
available Data Management Plans (DMPs). The corpus was created as part
of PhD research focused on the analysis of DMP structure, templates,
and related metadata.

Version 1.0 contains metadata for 150 manually reviewed DMPs collected
from public repositories and DMP platforms.

The repository provides:

- curated metadata in CSV format;
- an RDF/Turtle representation of the dataset;
- a lightweight ontology describing corpus-specific concepts;
- human-readable web pages and persistent identifiers for individual DMP records.

---

## Data Collection

The corpus was compiled from publicly accessible repositories and DMP
management platforms, including:

- Zenodo
- DMPonline
- TU Wien institutional repository
- EOSC

The current release represents an initial curated subset selected from a
substantially larger collection of DMP documents.

The distribution of records across repositories approximately reflects
their representation in the original collection. The selection was
designed to preserve diversity with respect to repositories, templates,
document structures, and publication platforms.

The dataset is not intended to be statistically representative of all
existing DMPs.

Future releases may extend the corpus with additional manually reviewed
records.

---

## Repository Structure

```text
DMP-corpus/

├── docs/                     # GitHub Pages website
│   ├── assets/
│   ├── data/
│   │   ├── dmp_corpus_v1.csv
│   │   └── dmp_corpus_v1.ttl
│   ├── dmp/
│   │   ├── ...
│   │   └── index.html
│   ├── codebook.md
│   ├── ontology_dmpc.ttl
│   ├── index.html
│   └── records.html
│
├── scripts/
│   └── build_dmp_corpus.py
│
├── ontology/
│   └── ontology_dmpc.ttl
│
├── metadata/
│   ├── codebook.md
│   ├── dmp_corpus_v1.csv
│   └── dmp_corpus_v1.ttl
│
├── README.md
├── LICENSE
└── CITATION.cff
```

---

## Dataset Contents

The dataset includes metadata describing individual DMPs, including:

- internal identifier;
- source repository;
- original DMP link;
- identifier from the source repository;
- title;
- creation date;
- document format;
- template;
- language;
- license information;
- document structure;
- completeness with respect to the original template;
- declared access level;
- software platform;
- presence of figures, tables, and lists;
- curator notes.

A detailed description of all metadata fields is available in:

- `metadata/codebook.md`

---

## Website and Persistent Identifiers

Each DMP record is assigned a persistent web identifier:

```text
https://jmartinkova.github.io/DMP-corpus/dmp/{internal-id}/
```

For example:

```text
https://jmartinkova.github.io/DMP-corpus/dmp/29/
```

Each record page contains:

- human-readable metadata;
- links to the RDF dataset;
- links to the original DMP document when available.

---

## RDF Representation

In addition to the tabular representation, the repository provides an
RDF version of the dataset to support interoperability, reuse, and
Linked Data applications.

The RDF representation is generated automatically from the CSV metadata
and uses:

- Dublin Core Terms;
- Schema.org;
- the custom DMP Corpus vocabulary (`dmpc`).

The ontology is available at:

```text
https://jmartinkova.github.io/DMP-corpus/ontology_dmpc.ttl
```

---

## Scope and Limitations

This repository contains metadata only.

The original DMP documents are not redistributed and remain subject to
their respective licenses and terms of use.

The metadata were created through manual review and curation. Although
every effort has been made to ensure consistency, some metadata fields
represent expert assessments and may contain minor inconsistencies.

The dataset is intended as a research corpus and is not statistically
representative of all existing Data Management Plans.

---

## License

The metadata in this repository are released under the CC0 1.0 Universal
license.

The original DMP documents remain subject to their respective licenses
and terms of use.

---

## Citation

If you use this dataset, please cite the corresponding Zenodo record.

*Citation details will be added after the first Zenodo release.*

---

## Versioning

This repository follows semantic versioning.

### v1.0.0

- initial public release;
- 150 manually reviewed DMPs;
- CSV export;
- RDF/Turtle representation;
- ontology;
- GitHub Pages website.

---

## Contact

Questions, comments, and suggestions are welcome via GitHub Issues.