import argparse

from query_analysis import explain_renderer


def render(json_data, output_path):
    ctx = explain_renderer.ExplainContext(explain_renderer.decode_json(json_data), None)
    ctx.init_canvas(None, None, lambda x, y, w, h: None)
    ctx.layout()
    ctx.export_to_png(output_path)

def main():
    parser = argparse.ArgumentParser(description="CLI to convert MySQL JSON EXPLAIN to PNG file.")
    parser.add_argument('infile', type=argparse.FileType('r'), help="Input file (must be JSON)")
    parser.add_argument('outfile', help="Output file path (output is PNG)")
    args = parser.parse_args()

    with args.infile as f:
        json_data = f.read().replace('\n','')
        render(json_data, args.outfile)

if __name__ == '__main__':
    main()
