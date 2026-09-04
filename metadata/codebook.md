# Codebook

This document describes the metadata fields included in the DMP Corpus dataset.

## Metadata Fields

| Field | Description | Allowed values |
|---|---|---|
| `Internal ID` | Internal identifier assigned to each DMP record within the corpus. | Unique integer |
| `Source` | Repository, platform, or other source from which the DMP was collected. | Free text |
| `Source Link` | URL of the repository, platform, or other source from which the DMP was collected, when available. | URL / Unknown |
| `Direct DMP Link` | URL pointing to the original publicly available DMP or its landing page, when available. | URL / Unknown |
| `Public ID` | Public identifier assigned by the original repository or platform, when available (e.g., DOI or repository-specific identifier). | DOI / repository-specific identifier / Unknown |
| `Name` | Title of the Data Management Plan. | Free text |
| `Date of Creation` | Creation or publication date of the DMP, when available. | `YYYY-MM-DD` / Unknown |
| `Format` | File format of the DMP. | PDF, DOCX, HTML, TXT, ... |
| `Template` | Template or framework used to create the DMP, when identifiable. | Template name / Unknown |
| `Template Source` | URL providing information about or access to the identified template, when available. | URL / Unknown |
| `Language` | Language of the document. | ISO 639-1 language code (e.g., `en`, `cs`, `de`, `es`, `fr`, ...) |
| `License` | License or rights statement associated with the original DMP, when available. | CC BY, CC BY-SA, CC0, All rights reserved, Unknown, ... |
| `License Link` | URL of the identified license, when an applicable license URI is available. | URL / Unknown |
| `Parts/Questions according to template` | Curator-estimated degree to which the structure and sections of the DMP correspond to the identified template. This value represents an expert assessment rather than an exact count. | Integer |
| `Completeness` | Curator-estimated degree to which the DMP addresses and completes the identified template. This value represents an expert assessment rather than an exact quantitative measure. | Integer |
| `Declared access level` | Access level explicitly declared in the original DMP or repository metadata. | Public / Restricted / Unknown |
| `Notes` | Additional curator notes regarding document structure, template compliance, language, or other relevant characteristics. | Free text |
| `Tool` | Tool or platform used to create or manage the DMP, when known. | DMPonline, Argos, DMPTuuli, Unknown, ... |
| `Tool Link` | URL of the identified DMP creation or management tool, when available. | URL / Unknown |
| `Figures` | Indicates whether the DMP contains figures, diagrams, or other graphical elements. | YES / NO |
| `Tables` | Indicates whether the DMP contains tables beyond the initial metadata page. | YES / NO |
| `Lists` | Indicates whether the DMP contains lists or enumerations. | YES / NO |

## Notes on Interpretation

Some metadata fields were created through manual review and may involve curator interpretation.

Template identification was based on explicit references within the document whenever possible. In some cases, the template could not be identified unambiguously.

The `Parts/Questions according to template` field reflects the extent to which the document follows the identified template structure. It does not evaluate the quality of the content.

The `Completeness` field indicates the degree to which the DMP addresses the questions or sections defined by the identified template. It does not assess the quality or adequacy of the responses.

The `Notes` field contains observations about structural characteristics of the DMPs and should not be interpreted as an assessment of scientific quality.

The value `unknown` is used in the CSV representation where information could not be identified or was not available during curation. On the human-readable record pages, such missing values are displayed as *Not available*. Missing or unknown values are generally omitted from the RDF representation.

The `Source Link`, `Template Source`, `License Link`, and `Tool Link` fields provide links to external resources where such links could be identified. In the RDF representation, these links are represented as resource URIs where available; otherwise, the corresponding textual metadata value may be retained as a literal.