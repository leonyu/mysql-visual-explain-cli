# MySQL Visual Explain CLI

[MySQL Workbench](https://github.com/mysql/mysql-workbench/) comes with a Visual Explain feature that is written in Python using [Cairo](https://www.cairographics.org/). This project simply extracts that code and provides a minimal CLI for it.

Since Cairo supports both PNG and SVG, with only a few line changes, I was able to add support for SVG. However, due to the fact that underlying code vectorizes input text, the SVG output is generally larger than PNG output.

## Usages

### Install

```sh
sudo apt-get install python3-cairocffi

curl -L https://github.com/leonyu/mysql-visual-explain-cli/releases/latest/download/mysql_visual_explain_cli.pyz -o ./mysql_visual_explain_cli
chmod +x ./mysql_visual_explain_cli
```

### Convert JSON Explain file to PNG/SVG

```sh
./mysql_visual_explain_cli explain.json explain.png
./mysql_visual_explain_cli explain.json explain.svg
```

### Pipe EXPLAIN Output from MySQL

```sh
mysql --raw --skip-column-names -e "EXPLAIN FORMAT=JSON SELECT * FROM INFORMATION_SCHEMA.COLUMNS;" | ./mysql_visual_explain_cli - columns_explained.png
```

## Example Outputs

| PNG                                   | SVG                                   |
| ------------------------------------- | ------------------------------------- |
| ![PNG example](examples/mysql_doc.png) | ![SVG example](examples/mysql_doc.svg) |

## Notes

The MySQL Workbench Python code calls Cairo C directly via [FFI](https://en.wikipedia.org/wiki/Foreign_function_interface) instead of the more common [Pycairo](https://pypi.org/project/pycairo/) library, thus this project depends on [CairoCFFI](https://pypi.org/project/cairocffi/)

The following C functions appear to have been patched compared to what is distributed with modern Debian distributions.

* `cairo.cairo_text_extents()`
* `cairo.cairo_set_dash()`

The version of Python bundled with MySQL Workbench also seems to perform implicit `str` to `byte` conversion.

## License

This project is a derivative work of MySQL Workbench which is GPLv2. Meaning unless I have money for a lawyer, it will forever be GPLv2 as well.
