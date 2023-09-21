
import argparse

from query_analysis.explain_renderer import ExplainContext, decode_json


def render(json_data: str, output_path: str):
    ctx = ExplainContext(decode_json(json_data), None)
    ctx.init_canvas(None, None, lambda x, y, w, h: None)
    ctx.layout()
    ctx.export_to_png(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Convert MySQL FORMAT=JSON EXPLAIN to PNG file.')
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input JSON file (Use - for stdin)')
    parser.add_argument('outfile', help='Output PNG file path')
    args = parser.parse_args()

    with args.infile as file:
        json_data = file.read().replace('\n', '')
        render(json_data, args.outfile)


if __name__ == '__main__':
    main()
