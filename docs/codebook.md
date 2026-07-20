# Codebook

This document describes the metadata fields included in the DMP Corpus
dataset.

## Metadata Fields

| Field | Description | Allowed values |
|---|---|---|
| `Internal ID` | Internal identifier assigned to each DMP record within the corpus. | Unique integer |
| `Source` | Repository or platform from which the DMP was collected. | Free text |
| `Direct DMP Link` | URL pointing to the original publicly available DMP or its landing page. | URL |
| `Public ID` | Public identifier assigned by the original repository (e.g., DOI or repository-specific identifier). | DOI / repository-specific identifier |
| `Name` | Title of the Data Management Plan. | Free text |
| `Date of Creation` | Creation or publication date of the DMP, when available. | `YYYY-MM-DD` / Unknown |
| `Format` | File format of the DMP (e.g., PDF, DOCX, HTML). | PDF, DOCX, HTML, TXT, ... |
| `Template` | Template or framework used to create the DMP, if identifiable. | Horizon Europe, Horizon 2020, Science Europe, ... |
| `Language` | Language of the document. | ISO 639-1 language codes (e.g., `en`, `cs`, `de`, `es`, `fr`, ...) |
| `License` | License information associated with the original DMP. | CC BY, CC BY-SA, CC0, All rights reserved, unknown, ... |
| `Parts/Questions according to template` | Curator-estimated degree to which the structure and sections of the DMP correspond to the identified template. This value represents an expert assessment rather than an exact count. | Integer |
| `Completeness` | Curator-estimated degree to which the DMP addresses and completes the identified template. This value represents an expert assessment rather than an exact quantitative measure. | Integer |
| `Declared access level` | Access level explicitly declared in the original DMP or repository metadata. | Public / Restricted / Unknown |
| `Tool` | Tool or platform used to create or manage the DMP, when known. | DMPonline, Data Stewardship Wizard, Argos, unknown, ... |
| `Figures` | Indicates whether the DMP contains figures, diagrams, or other graphical elements. | YES / NO |
| `Tables` | Indicates whether the DMP contains tables beyond the initial metadata page. | YES / NO |
| `Lists` | Indicates whether the DMP contains lists or enumerations. | YES / NO |
| `Notes` | Additional curator notes regarding document structure, template compliance, language, or other relevant characteristics. | Free text |

## Notes on Interpretation

Some metadata fields were created through manual review and may involve
curator interpretation.

Template identification was based on explicit references within the
document whenever possible. In some cases, the template could not be
identified unambiguously.

The `Parts/Questions according to template` field reflects the extent to which the document
follows the identified template structure. It does not evaluate the
quality of the content.

The `Completeness` field indicates the degree to which the DMP addresses the
questions or sections defined by the identified template. It does not
assess the quality or adequacy of the responses.

The `Notes` field contains observations about structural characteristics
of the DMPs and should not be interpreted as an assessment of scientific
quality.