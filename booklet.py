#!/bin/env python3
# Original https://github.com/Nimdraug/booklet
# Updated by k0

import os
import PyPDF2.utils
import math


def iter_pages(pages):
    if pages % 4:
        pages = pages + 4 - pages % 4

    for output_page in range(int(pages / 4)):
        first = output_page * 2
        last = pages - 1 - first

        # Front
        yield first, -90, 1, .5
        yield last, -90, 1, 0

        # Back
        yield first + 1, 90, 0, 1
        yield last - 1, 90, 0, .5


def translation_matrix(x, y=None):
    if y is None:
        y = x

    return [
        [1, 0, 0],
        [0, 1, 0],
        [x, y, 1]
    ]


def scale_matix(scale_x, scale_y=None):
    if scale_y is None:
        scale_y = scale_x

    return [
        [scale_x, 0, 0],
        [0, scale_y, 0],
        [0, 0, 1]
    ]


def rotation_matrix(angle, rad=False):
    if not rad:
        angle = math.radians(angle)

    return [
        [math.cos(angle), math.sin(angle), 0],
        [-math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ]


def merge_matrix(translation_matrix):
    return [
        translation_matrix[0][0], translation_matrix[0][1],
        translation_matrix[1][0], translation_matrix[1][1],
        translation_matrix[2][0], translation_matrix[2][1]
    ]


def del_empty_pages(py_obj):
    # Get rid of empty pages
    keep = []
    for page in range(py_obj.getNumPages()):
        if py_obj.getPage(page).getContents() is not None:
            keep.append(page)
    fixed = PyPDF2.PdfFileWriter()
    for i in keep:
        p = py_obj.getPage(i)
        fixed.addPage(p)
    return fixed


def build_doc(in_file, out_file):
    if isinstance(in_file, list):
        merger = PyPDF2.PdfFileMerger()
        for pdf in in_file:
            merger.append(pdf)
        merger.write("result.pdf")
        merger.close()
        src = PyPDF2.PdfFileReader('result.pdf')
        os.remove('result.pdf')
    else:
        src = PyPDF2.PdfFileReader(in_file)

    src = del_empty_pages(src)

    out = PyPDF2.PdfFileWriter()

    size = src.getPage(0).mediaBox.upperRight
    aspect = size[0] / size[1]

    outpage = out.addBlankPage(*size)

    for i, v in enumerate(iter_pages(src.getNumPages())):
        p, r, x, y = v
        if p < src.getNumPages():
            srcpage = src.getPage(p)

            tm = PyPDF2.utils.matrixMultiply(scale_matix(aspect), rotation_matrix(-r))
            tm = PyPDF2.utils.matrixMultiply(tm, translation_matrix(float(size[0]) * x, float(size[1]) * y))

            outpage.mergeTransformedPage(srcpage, merge_matrix(tm))

        if i < src.getNumPages() and i % 2:
            outpage = out.addBlankPage(*size)

    out_fixed = del_empty_pages(out)

    with open(out_file, 'wb') as outfile:
        out_fixed.write(outfile)


def main():
    import argparse

    p = argparse.ArgumentParser(description='create a booklet pdf from source document')
    p.add_argument('-s', '--source', help='the document to turn into a booklet', dest='source')
    p.add_argument('-t', '--target', help='the file to output the booklet to', default='out.pdf', dest='target')
    p.add_argument('-m', '--merge', nargs='+', dest='merge')

    args = p.parse_args()

    if args.source:
        build_doc(args.source, args.target)
    else:
        build_doc(args.merge, args.target)


if __name__ == '__main__':
    main()
