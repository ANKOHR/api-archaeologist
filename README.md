# API Archaeologist

Give it your traffic logs and code samples. It digs up the API contract and proves each claim with evidence.

Here, proof means traceability to observations, never verification of a live API. API Archaeologist is a CPU-only, standard-library Python CLI that reconstructs an inferred contract and generates a reference, typed request builders, fixture replay tests, and reports. The included acme-orders remains are entirely fictional.

## Quickstart

Python 3.10 or newer is required. Development tests require pytest.

```powershell
python -m pip install -e .
python -m pip install pytest
python -m aar fixtures --out demo/remains
python -m aar ingest demo/remains --out demo/evidence.json
python -m aar infer --evidence demo/evidence.json --out demo/schema.json
python -m aar docs --schema demo/schema.json --out demo/reference.md
python -m aar client --schema demo/schema.json --lang python --out demo/client.py
python -m aar tests --schema demo/schema.json --out demo/replay
python -m aar report --schema demo/schema.json --format md --out demo/report.md
python -m aar report --schema demo/schema.json --format json --out demo/report.json
python -m pytest demo/replay -q
python -m pytest -q
```

The installed `aar` command has the same interface as `python -m aar`. Use the module form if Python's Scripts directory is not on PATH. With no flags, `infer` reads `evidence.json`; generators read `schema.json`. No command contacts an API. The generated client returns request dictionaries for a transport supplied by the caller. It deliberately does not invent a server URL, tokens, retries, or response guarantees.

## Architecture

```text
Synthetic fixture generator -> JSON traffic + errors + Python examples
                                       |
                      JSON validation / Python AST literal extraction
                                       |
                         Evidence records with stable IDs
                                       |
                    Declared rules + counts + conflict detection
                                       |
                         Inferred schema with provenance
                        /         |          |         \
               Markdown      Typed Python   Replay    MD/JSON
               reference     builders       pytest    reports
```

`aar/core.py` parses evidence, creates fixtures, and infers contracts. `aar/generate.py` renders artifacts. `aar/cli.py` supplies the seven subcommands. No runtime dependencies, training, GPU access, torch, or tensorflow are used.

## Evidence formats

An input directory is scanned recursively in sorted order for `.json` and `.py` files. Keep generated schemas and reports outside it. JSON files contain one capture object or a list of capture objects:

```json
{
  "synthetic": true,
  "request": {
    "method": "GET",
    "path": "/orders/101?include_archived=true",
    "headers": {"Authorization": "Bearer fictional-token"}
  },
  "response": {"status": 200, "body": {"id": 101}}
}
```

Requests require a supported HTTP method and absolute path or URL containing an absolute path. Query strings and explicit `query` objects are accepted; explicit keys take precedence. Headers are string maps normalized to lowercase. Status codes must be integers from 100 to 599. Missing bodies stay unknown; explicit JSON null is an observed null. Error files use the same format and require request context. Files with `error` in their stem are catalogued as error evidence. Malformed captures raise `MalformedCaptureError` with source names. Invalid Python raises `CodeExampleError`; empty inputs raise `EvidenceError` with `NoEvidenceError` in its message.

Python extraction recognizes literal `requests`, `client`, and `session` calls for supported method attributes with literal URL, `params`, `headers`, and `json` arguments. It uses AST parsing and never executes sample code. Dynamic expressions and unrecognized callers are skipped. This is a deliberately bounded AST-lite extractor, not a general program analysis tool. A module docstring containing `SYNTHETIC` labels code evidence synthetic. Unsupported file extensions are ignored. No HAR, packet capture binary, or raw HTTP text format is claimed.

## Inference rules

* Endpoint identity is HTTP method plus normalized path template. Decimal digit segments and canonical UUID segments become positional `{param_N}` parameters, even when observed once. Every other segment remains constant. These declared heuristics can misclassify numeric constants and cannot identify arbitrary string IDs.
* Parameter types are derived from JSON values. Query strings containing signed integers or decimal numbers are classified as integer or number. Other strings, including `true`, stay strings. Arrays, objects, booleans, and null retain their JSON types. Multiple parameter types produce a conflict and remain visible.
* Each known request body and each response status has its own recursive JSON shape. Compatible objects combine fields with occurrence counts. A field is inferred required only when present in every observed object at that location, otherwise optional. This describes the samples, not server validation requirements.
* Incompatible types at any shared field or array element produce a conflict containing both observed shapes and evidence IDs. Those shapes are not silently merged into a single contract. Empty arrays have unknown item shapes. Status codes are only an observed catalogue, never an exhaustive promise.
* Auth recognition is limited to declared header patterns: `Authorization: Bearer <value>`, `Authorization: Basic <value>`, and `X-API-Key: <value>`. Observing a scheme never establishes that it is required. Other auth formats are unknown. Tokens are not copied into builder defaults.
* Unobserved request bodies, auth requirements, query necessity, unobserved behavior, and missing responses stay unknown. The tool does not invent endpoint names, field meanings, defaults, enum constraints, pagination semantics, or server URLs.

## Confidence semantics

Every inferred claim includes sorted evidence IDs and a confidence note. One supporting record is `low: one observation`; multiple supporting records are `medium: repeated observations; not verified`. There is no high or confirmed confidence. Repeated evidence can be correlated or duplicated, so confidence is an observation count heuristic, not a probability. Presence claims report their exact occurrence counts. Conflicts are labelled conflicting and unknown claims explain the missing evidence. Evidence IDs hash normalized record content, relative source path, and record position or line number.

## Endpoint catalogue

The fixture run discovers `GET /orders`, `GET /orders/{param_2}`, `POST /orders`, and `GET /inventory`. It captures the planted order identifier parameter, the once-used `include_archived` query parameter, observed 200/201/404 statuses, and bearer auth observations. The generated reference includes every endpoint, all schema details, and local evidence anchors resolving to the normalized original records.

## Conflict list

`GET /inventory` has incompatible boolean and string `available` response fields at status 200. Both shapes and their source evidence remain in the schema and reports. Generated clients make no response-shape promise. Replay passing cannot resolve this conflict.

## Unknown list

Reports catalogue unknown bodies, auth requirements, query necessity, and unobserved behavior. Unknowns also appear in individual schema claims and the reference. Unknown fields in generated builders use optional types and explanatory comments; caller-supplied query and header dictionaries allow observed values without inventing defaults. Request object fields use typed optional keys because observed presence does not prove a real requirement.

## HONESTY BOUNDARY

Inferred is not verified. Reports distinguish inferred, conflicting, and unknown items and never present an inference as a confirmed contract. Client stubs are generated from inference and explicitly say so. All bundled fixtures are synthetic and labelled. Every report carries: `INFERRED, NOT VERIFIED. Schema is inferred from synthetic fixtures; unknowns are marked, not filled in.` Input records lacking a synthetic label have unverified provenance, reflected by `synthetic: false`; the standard banner refers to the bundled demonstration. Nothing here was verified against a real API.

Replay tests compare builder output with fixture request shapes. They do not send traffic, validate responses against a server, or establish a confirmed contract. Generated schema self-consistency checks verify evidence references. Input headers and bodies remain in local evidence and generated documentation, so use appropriately sanitized captures when sharing artifacts.

## Determinism and validation

Fixtures use no randomness, so no seed is needed. Sorted input traversal, stable hash IDs, sorted keys, fixed endpoint order, and UTF-8 writes produce byte-identical artifacts for identical input content and relative paths. Moving a file within the input directory changes its source identity. Generated tests load the sibling client and schema independently of the working directory.

The full pytest suite covers ingestors and named errors, code extraction, parameters, optional counts, auth, conflicts, docs, typed client imports, replay, generated tests, deterministic fixtures and artifacts, CLI end-to-end execution, report banners, and the ban on em dash characters. The checked-in `demo` directory contains a complete synthetic run. GitHub publication is handled separately and is not performed by this build.
