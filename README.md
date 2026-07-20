# DMP Corpus

A curated corpus of publicly available Data Management Plans (DMPs)
collected from multiple repositories and manually reviewed for
structural and metadata characteristics.

## About

This repository contains metadata describing a curated corpus of
publicly available Data Management Plans (DMPs). The corpus was created
as part of PhD research focused on the analysis of DMP structure,
templates, and related metadata.

Version 1.0 contains metadata for 150 manually reviewed DMPs collected
from public repositories and DMP platforms.

## Data Collection

The corpus was compiled from publicly accessible repositories and DMP
management platforms, including:

-   Zenodo
-   DMPonline
-   TU Wien institutional repository
-   EOSC

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

## Repository Structure

``` text
DMP-corpus/

├── metadata/
│   ├── dmp_metadata_v1.csv
│   └── dmp_metadata_v1.ttl
│
├── docs/
│   └── codebook.md
│
├── README.md
├── LICENSE
└── CITATION.cff
```

## Dataset Contents

The dataset includes metadata describing individual DMPs, including:

-   internal identifier
-   source repository
-   original DMP link
-   public identifier
-   title
-   creation date
-   document format
-   template
-   language
-   license information
-   document structure
-   completeness with respect to the original template
-   presence of figures, tables, and lists
-   version information
-   software platform
-   curator notes

A detailed description of all metadata fields is available in
`docs/codebook.md`.

## Scope and Limitations

This repository contains metadata only.

The original DMP documents are not redistributed and remain subject to
their respective licenses and terms of use.

The metadata were created through manual review and curation. Although
every effort has been made to ensure consistency, some metadata fields
involve interpretation and may contain minor inconsistencies.

## RDF Representation

In addition to the tabular representation, the repository provides an
RDF version of the dataset to support interoperability, reuse, and
Linked Data applications.

The RDF representation describes the metadata records included in this
corpus and does not replace or redistribute the original DMP documents.

## License

The metadata in this repository are released under the CC0 1.0 Universal
license.

## Citation

If you use this dataset, please cite the corresponding Zenodo record.

*Citation details will be added after the first Zenodo release.*

## Versioning

This repository follows semantic versioning:

-   v1.0.0 --- Initial public release (150 manually reviewed DMPs)

## Contact

Questions, comments, and suggestions are welcome via GitHub Issues.