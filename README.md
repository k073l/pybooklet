# pybooklet
Python script that creates pdf booklets printable on a printer capable of double sided printing

## Usage
```sh
booklet.py -s input.pdf -t output.pdf
booklet.py -m input1.pdf input2.pdf -t output.pdf
```
Reads in `input.pdf` and outputs the booklet pdf to `output.pdf`

Merge multiple pdfs (`input1.pdf`, `input2.pdf`) and output booklet pdf to `output.pdf`

Output defaults to `out.pdf`

## Requirements
- [python3](https://www.python.org/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
