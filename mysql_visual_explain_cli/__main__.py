
import argparse
import pathlib
from cairocffi import cairo

from query_analysis.explain_renderer import ExplainContext, decode_json
from graphics.cairo_utils import ImageSurface, Context, Surface


class SVGSurface(Surface):
    def __init__(self, filename: str, width=None, height=None):
        Surface.__init__(self)
        self.s = cairo.cairo_svg_surface_create(filename.encode(), width, height)


def export_to_svg(ec: ExplainContext, path: str):
    img = SVGSurface(path, width=ec.size[0], height=ec.size[1])
    cr = Context(img)
    ec._canvas.repaint(cr, 0, 0, ec.size[0], ec.size[1])


def render(json_str: str, output_path: str):
    json_data = decode_json(json_str)
    if 'query_block' not in json_data:
        raise ValueError('Input file does not contain a MySQL EXPLAIN JSON')
    ctx = ExplainContext(json_data, None)
    ctx.init_canvas(None, None, lambda x, y, w, h: None)
    ctx.layout()
    extension = pathlib.Path(output_path).suffix
    if extension == '.png':
        ctx.export_to_png(output_path)
    elif extension == '.svg':
        export_to_svg(ctx, output_path)
    else:
        raise ValueError(f'Unsupported extension: {extension}')


def main():
    parser = argparse.ArgumentParser(
        description='Convert MySQL FORMAT=JSON EXPLAIN to PNG or SVG file.')
    parser.add_argument('infile',
                        type=argparse.FileType('r'),
                        help='Input JSON file (Use - for stdin)')
    parser.add_argument('outfile', help='Output PNG or SVG file path')
    args = parser.parse_args()

    with args.infile as file:
        json_data = file.read().replace('\n', '')
        render(json_data, args.outfile)


if __name__ == '__main__':
    main()
