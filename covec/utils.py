# -*- coding: utf-8 -*-
import re
import clang.cindex as cc


def walker(root, selector=lambda x: True):
    """
    BFS every child of root and return selected node,
    if selector not given, return list of all node.

    :param root: root node of tree
    :param selector: select which node you want
    :return selected: list of selected node
    """
    selected = list()
    queue = list()
    queue.append(root)
    while queue:
        node = queue.pop(0)
        for child in node.get_children():
            if child.hash not in [x.hash for x in queue]:
                queue.append(child)
        if selector(node):
            selected.append(node)
    return selected


def is_user_func(node):
    """is user defined function?"""
    return node.kind == cc.CursorKind.FUNCTION_DECL and node.is_definition()


def is_func_call(node):
    """return node is function call or not"""
    return node.kind == cc.CursorKind.CALL_EXPR


def is_decl_ref(node):
    """is reference of variable declaration?"""
    return node.kind == cc.CursorKind.DECL_REF_EXPR


def is_member_ref(node):
    """"is reference of struct member?"""
    return node.kind == cc.CursorKind.MEMBER_REF_EXPR


def file_slice(path, lines):
    """file slice by line numbers
    """
    sline = []
    with open(path, 'r') as f:
        for i, l in enumerate(f):
            if i+1 in lines:
                # remove space and \n
                sline.append(l.strip())
    return sline

def remove_comment(text):
    """remove c/c++ style comments
    """
    return re.sub('//.*?\n|/\*.*?\*/', '', text, flags=re.S)


def deduplication(slice_set):
    res = []
    flag = True
    while slice_set:
        tmp = slice_set.pop(0)
        for i in slice_set:
            if tmp['slice'][1:] == i['slice'][1:]:
                flag = False
        if flag:
            res.append(tmp)
    return res
