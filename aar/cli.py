"""Command line entry point."""
import argparse
import json
from pathlib import Path
from .core import BANNER, EvidenceError, dump, fixtures, infer, ingest, write
from .generate import client, markdown, report, test_bundle


def main(argv=None):
    parser = argparse.ArgumentParser(description=BANNER)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('fixtures')
    p.add_argument('--out', required=True)
    p = sub.add_parser('ingest')
    p.add_argument('directory')
    p.add_argument('--out', default='evidence.json')
    p = sub.add_parser('infer')
    p.add_argument('--evidence', default='evidence.json')
    p.add_argument('--out', default='schema.json')
    for command in ['docs', 'client', 'tests', 'report']:
        p = sub.add_parser(command)
        p.add_argument('--schema', default='schema.json')
        p.add_argument('--out', default={'docs': 'reference.md', 'client': 'client.py', 'tests': 'replay', 'report': 'report.md'}[command])
        if command == 'client':
            p.add_argument('--lang', choices=['python'], default='python')
        if command == 'report':
            p.add_argument('--format', choices=['md', 'json'], default='md')
    args = parser.parse_args(argv)
    try:
        if args.command == 'fixtures':
            fixtures(args.out)
        elif args.command == 'ingest':
            write(args.out, dump(ingest(args.directory)))
        elif args.command == 'infer':
            write(args.out, dump(infer(json.loads(Path(args.evidence).read_text(encoding='utf-8')))))
        else:
            schema = json.loads(Path(args.schema).read_text(encoding='utf-8'))
            if args.command == 'tests':
                test_bundle(schema, args.out)
            else:
                content = markdown(schema) if args.command == 'docs' else client(schema) if args.command == 'client' else report(schema, args.format)
                write(args.out, content)
    except (EvidenceError, OSError, ValueError, KeyError) as exc:
        parser.exit(2, f'{type(exc).__name__}: {exc}\n')
    print(BANNER)
    return 0
