# -*- coding: utf-8 -*-
import clang.cindex as cc


def loader_cc(path):
    """load c/c++ file from path, return entry node

    :param path: path of parsed file :string
    :return entry: return entry(file) node :cc.TranslationUnit
    """
    cindex = cc.Index.create()
    entry = cindex.parse(path)
    return entry
