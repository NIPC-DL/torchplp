# -*- coding: utf-8 -*-
from . import utils
from . import loader
from .constants import NODE_FILTER


class Parser:
    """"Super class of Parser"""
    pass


class Parser_cc(Parser):
    """C/C++ parser"""

    def __init__(self, path):
        self._path = path
        self._entry = loader.loader_cc(path).cursor

    def slice(self):
        """extract program slice from function call"""
        slice_list = list()
        user_func = utils.walker(self._entry, utils.is_user_func)
        for func in user_func:
            func_call = utils.walker(func, utils.is_func_call)
            func_call = filter(self._node_filter, func_call)
            for call in func_call:
                # node_list record main func and called func to range slice
                node_list = [func, ]
                for f in user_func:
                    if call.spelling == f.spelling:
                        node_list.append(f)
                slice_line = list()
                para = self._get_param(call)
                for p in para:
                    # is a struct member
                    if isinstance(p, list):
                        for i in p:
                            line = self._trace_param(i, node_list)
                            slice_line.extend(line)
                    # or not
                    else:
                        line = self._trace_param(p, node_list)
                        slice_line.extend(line)
                lines = utils.file_slice(self._path, sorted(slice_line))
                # filter only one line slices
                if len(lines) > 1:
                    slice_list.append({
                        'func': func,
                        'call': call,
                        'slice': lines,
                    })
        ded_list = self._deduplic(slice_list)
        return ded_list

    def _node_filter(self, node):
        """ filter node by NODE_FILTER"""
        flag = True
        for i in NODE_FILTER:
            if i in node.spelling:
                flag = False
        return flag

    def _get_param(self, node):
        """
        extract parameter from function call
        """
        para = []
        for child in node.get_children():
            if child.spelling != node.spelling:
                # if found struct member
                if utils.walker(child, utils.is_member_ref):
                    mem = utils.walker(child, utils.is_member_ref)[0]
                    para.append([mem, list(mem.get_children())[0]])
                # else just normal
                elif utils.walker(child, utils.is_decl_ref):
                    para.append(utils.walker(child, utils.is_decl_ref)[-1])
                else:
                    pass
        return para

    def _trace_param(self, p, node_list):
        """trace parameter in node_list and return corresponding line number
        """
        line = []
        for node in node_list:
            rel = utils.walker(node, lambda x: p.spelling == x.spelling)
            line.extend([x.location.line for x in rel])
        return set(line)

    def _deduplic(self, slice_list):
        ded_list = []
        for s in slice_list:
            if s['slice'] not in [x['slice'] for x in ded_list]:
                ded_list.append(s)
        return ded_list

    def vector(self):
        pass
