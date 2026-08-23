<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Codebook — DMP Corpus</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header class="site-header">
    <a href="./">DMP Corpus</a>
  </header>

  <main class="codebook">
    <h1>Codebook</h1>
<p>This document describes the metadata fields included in the DMP Corpus
dataset.</p>
<h2>Metadata Fields</h2>
<table>
<thead>
<tr>
<th>Field</th>
<th>Description</th>
<th>Allowed values</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Internal ID</code></td>
<td>Internal identifier assigned to each DMP record within the corpus.</td>
<td>Unique integer</td>
</tr>
<tr>
<td><code>Source</code></td>
<td>Repository or platform from which the DMP was collected.</td>
<td>Free text</td>
</tr>
<tr>
<td><code>Direct DMP Link</code></td>
<td>URL pointing to the original publicly available DMP or its landing page.</td>
<td>URL</td>
</tr>
<tr>
<td><code>Public ID</code></td>
<td>Public identifier assigned by the original repository (e.g., DOI or repository-specific identifier).</td>
<td>DOI / repository-specific identifier</td>
</tr>
<tr>
<td><code>Name</code></td>
<td>Title of the Data Management Plan.</td>
<td>Free text</td>
</tr>
<tr>
<td><code>Date of Creation</code></td>
<td>Creation or publication date of the DMP, when available.</td>
<td><code>YYYY-MM-DD</code> / Unknown</td>
</tr>
<tr>
<td><code>Format</code></td>
<td>File format of the DMP (e.g., PDF, DOCX, HTML).</td>
<td>PDF, DOCX, HTML, TXT, ...</td>
</tr>
<tr>
<td><code>Template</code></td>
<td>Template or framework used to create the DMP, if identifiable.</td>
<td>Horizon Europe, Horizon 2020, Science Europe, ...</td>
</tr>
<tr>
<td><code>Language</code></td>
<td>Language of the document.</td>
<td>ISO 639-1 language codes (e.g., <code>en</code>, <code>cs</code>, <code>de</code>, <code>es</code>, <code>fr</code>, ...)</td>
</tr>
<tr>
<td><code>License</code></td>
<td>License information associated with the original DMP.</td>
<td>CC BY, CC BY-SA, CC0, All rights reserved, unknown, ...</td>
</tr>
<tr>
<td><code>Parts/Questions according to template</code></td>
<td>Curator-estimated degree to which the structure and sections of the DMP correspond to the identified template. This value represents an expert assessment rather than an exact count.</td>
<td>Integer</td>
</tr>
<tr>
<td><code>Completeness</code></td>
<td>Curator-estimated degree to which the DMP addresses and completes the identified template. This value represents an expert assessment rather than an exact quantitative measure.</td>
<td>Integer</td>
</tr>
<tr>
<td><code>Declared access level</code></td>
<td>Access level explicitly declared in the original DMP or repository metadata.</td>
<td>Public / Restricted / Unknown</td>
</tr>
<tr>
<td><code>Tool</code></td>
<td>Tool or platform used to create or manage the DMP, when known.</td>
<td>DMPonline, Data Stewardship Wizard, Argos, unknown, ...</td>
</tr>
<tr>
<td><code>Figures</code></td>
<td>Indicates whether the DMP contains figures, diagrams, or other graphical elements.</td>
<td>YES / NO</td>
</tr>
<tr>
<td><code>Tables</code></td>
<td>Indicates whether the DMP contains tables beyond the initial metadata page.</td>
<td>YES / NO</td>
</tr>
<tr>
<td><code>Lists</code></td>
<td>Indicates whether the DMP contains lists or enumerations.</td>
<td>YES / NO</td>
</tr>
<tr>
<td><code>Notes</code></td>
<td>Additional curator notes regarding document structure, template compliance, language, or other relevant characteristics.</td>
<td>Free text</td>
</tr>
</tbody>
</table>
<h2>Notes on Interpretation</h2>
<p>Some metadata fields were created through manual review and may involve
curator interpretation.</p>
<p>Template identification was based on explicit references within the
document whenever possible. In some cases, the template could not be
identified unambiguously.</p>
<p>The <code>Parts/Questions according to template</code> field reflects the extent to which the document
follows the identified template structure. It does not evaluate the
quality of the content.</p>
<p>The <code>Completeness</code> field indicates the degree to which the DMP addresses the
questions or sections defined by the identified template. It does not
assess the quality or adequacy of the responses.</p>
<p>The <code>Notes</code> field contains observations about structural characteristics
of the DMPs and should not be interpreted as an assessment of scientific
quality.</p>
  </main>
</body>
</html>
