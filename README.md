# MySQL Visual Explain CLI

[MySQL Workbench](https://github.com/mysql/mysql-workbench/) comes with a Visual Explain feature that is written in Python using [Cairo](https://www.cairographics.org/). This project is simply extracts that code and provides a minimal CLI for it.

## Usages

### Install

```sh
sudo apt-get install python3-cairocffi

curl -LO --output-dir ~ https://github.com/leonyu/mysql-visual-explain-cli/releases/latest/download/mysql_visual_explain_cli.pyz
```

### Convert JSON Explain file to PNG
```
python3 ~/mysql_visual_explain_cli.pyz explain.json explain.png
```

### Pipe EXPLAIN Output from MySQL to CLI

```
mysql example.com -ABN --raw -e "EXPLAIN FORMAT=JSON SELECT * FROM HelloWorld;" | python3 ~/mysql_visual_explain_cli.pyz - hello_world_explained.png
```

### Development (Poetry)

```sh
poetry install
poetry run python ./mysql_visual_explain_cli explain.json explain.png
```

## Notes

The MySQL Workbench Python code calls Cairo C directly via [FFI](https://en.wikipedia.org/wiki/Foreign_function_interface) instead of the more common [Pycairo](https://pypi.org/project/pycairo/) library, thus this project depeneds on [CairoCFFI](https://pypi.org/project/cairocffi/)

The following C functions appear to have been patched or used a different version compare to what is distrubted with modern Debian distributions.

* `cairo.cairo_text_extents()`
* `cairo.cairo_set_dash()`

The version of Python bundled with MySQL Workbench also seems to perform implicit `str` to `byte` conversion.

## License

This project is a derivative work of MySQL Workbench which is GPLv2. Meaning unless I have money for a lawyer, it will forever be GPLv2 as well.
