# -*- coding: utf-8 -*-
import os
import covec

file_list = []
for root, dirname, filename in os.walk("/home/verf/WorkSpace/Data/Test/julie_api_func"):
    for name in filename:
        file_list.append(os.path.join(root, name))

for file_path in file_list[:50]:
    if file_path.split(".")[-1] not in ['c', 'cpp']:
        continue
    pr = covec.parse(file_path)
    call_slice = pr.slice()
    with open("ni_api_slice.txt", 'a') as f:
        file_name = file_path.split('/')[-1]
        for call in call_slice:
            call_name = call["call"].spelling
            call_line = call["call"].location.line
            code_lines = call['slice']
            f.writelines(f'{file_name} {call_name} {call_line}\n')
            for l in code_lines:
                f.writelines(l + '\n')
            f.writelines('-'*30 + '\n')
print('done')
