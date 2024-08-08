import argparse
from cairocffi import cairo, SVG_UNIT_USER

from mysql_visual_explain_cli.query_analysis.explain_renderer import (
    ExplainContext,
    decode_json,
)
from mysql_visual_explain_cli.graphics.cairo_utils import Context, Surface


class SVGSurface(Surface):
    def __init__(self, filename: str, width=None, height=None):
        Surface.__init__(self)
        self.s = cairo.cairo_svg_surface_create(filename.encode(), width, height)
        cairo.cairo_svg_surface_set_document_unit(self.s, SVG_UNIT_USER)


def export_to_svg(ec: ExplainContext, path: str):
    img = SVGSurface(path, width=ec.size[0], height=ec.size[1])
    cr = Context(img)
    ec._canvas.repaint(cr, 0, 0, ec.size[0], ec.size[1])


def render(json_str: str, output_path: str):
    json_data = decode_json(json_str)
    if not isinstance(json_data, dict) or not isinstance(
        json_data.get("query_block"), dict
    ):
        raise ValueError("Input file does not contain a MySQL EXPLAIN JSON")
    ctx = ExplainContext(json_data, None)
    ctx.init_canvas(None, None, lambda x, y, w, h: None)
    ctx.layout()
    if output_path.endswith(".png"):
        ctx.export_to_png(output_path)
    elif output_path.endswith(".svg"):
        export_to_svg(ctx, output_path)
    else:
        raise ValueError(f"Unsupported extension: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert MySQL FORMAT=JSON EXPLAIN to PNG or SVG file."
    )
    parser.add_argument(
        "infile", type=argparse.FileType("r"), help="Input JSON file (Use - for stdin)"
    )
    parser.add_argument("outfile", help="Output PNG or SVG file path")
    args = parser.parse_args()

    with args.infile as file:
        render(file.read(), args.outfile)


if __name__ == "__main__":
    main()
