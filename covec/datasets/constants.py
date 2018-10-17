# -*- coding: utf-8 -*-
"""
constants.py - The constant variable defined for datasets

Author: Verf
Email: verf@protonmail.com
License: MIT
"""

DOWNLOAD_URL = {
    "juliet":
    "https://samate.nist.gov/SRD/testsuites/juliet/Juliet_Test_Suite_v1.3_for_C_Cpp.zip",
    "sysevr":
    "https://github.com/SySeVR/SySeVR.git",
}
# AE: Arithmetic Expression, AF: API Function Call, AU: Array Usage, PU: Pointer Usage
JULIET_CATEGORY = {
    "AE": [
        'CWE114', 'CWE134', 'CWE190', 'CWE196', 'CWE319', 'CWE369', 'CWE398',
        'CWE416', 'CWE427', 'CWE469', 'CWE506', 'CWE605', 'CWE606', 'CWE666',
        'CWE680', 'CWE761', 'CWE789'
    ],
    "AF": [
        'CWE114', 'CWE121', 'CWE122', 'CWE123', 'CWE124', 'CWE126', 'CWE127',
        'CWE134', 'CWE190', 'CWE191', 'CWE194', 'CWE195', 'CWE196', 'CWE197',
        'CWE222', 'CWE223', 'CWE226', 'CWE242', 'CWE244', 'CWE252', 'CWE253',
        'CWE256', 'CWE259', 'CWE319', 'CWE321', 'CWE325', 'CWE327', 'CWE328',
        'CWE338', 'CWE364', 'CWE367', 'CWE369', 'CWE377', 'CWE390', 'CWE396',
        'CWE398', 'CWE400', 'CWE401', 'CWE404', 'CWE415', 'CWE416', 'CWE426',
        'CWE427', 'CWE457', 'CWE459', 'CWE464', 'CWE467', 'CWE469', 'CWE475',
        'CWE476', 'CWE478', 'CWE479', 'CWE481', 'CWE484', 'CWE506', 'CWE510',
        'CWE511', 'CWE526', 'CWE534', 'CWE535', 'CWE563', 'CWE571', 'CWE590',
        'CWE591', 'CWE605', 'CWE606', 'CWE617', 'CWE665', 'CWE666', 'CWE675',
        'CWE680', 'CWE681', 'CWE685', 'CWE688', 'CWE690', 'CWE758', 'CWE761',
        'CWE762', 'CWE773', 'CWE775', 'CWE780', 'CWE785', 'CWE789'
    ],
    "AU": [
        'CWE114', 'CWE121', 'CWE122', 'CWE124', 'CWE126', 'CWE127', 'CWE134',
        'CWE176', 'CWE190', 'CWE191', 'CWE194', 'CWE195', 'CWE197', 'CWE223',
        'CWE226', 'CWE242', 'CWE252', 'CWE253', 'CWE256', 'CWE259', 'CWE319',
        'CWE321', 'CWE325', 'CWE327', 'CWE328', 'CWE367', 'CWE369', 'CWE377',
        'CWE391', 'CWE400', 'CWE401', 'CWE404', 'CWE415', 'CWE426', 'CWE427',
        'CWE457', 'CWE464', 'CWE468', 'CWE469', 'CWE475', 'CWE476', 'CWE506',
        'CWE510', 'CWE534', 'CWE535', 'CWE562', 'CWE590', 'CWE591', 'CWE605',
        'CWE606', 'CWE617', 'CWE620', 'CWE665', 'CWE666', 'CWE672', 'CWE676',
        'CWE680', 'CWE681', 'CWE685', 'CWE688', 'CWE690', 'CWE761', 'CWE762',
        'CWE775', 'CWE780', 'CWE785', 'CWE789'
    ],
    "PU": [
        'CWE114', 'CWE121', 'CWE122', 'CWE123', 'CWE124', 'CWE126', 'CWE127',
        'CWE134', 'CWE176', 'CWE188', 'CWE190', 'CWE191', 'CWE194', 'CWE195',
        'CWE197', 'CWE226', 'CWE242', 'CWE244', 'CWE252', 'CWE253', 'CWE256',
        'CWE259', 'CWE272', 'CWE284', 'CWE319', 'CWE321', 'CWE327', 'CWE328',
        'CWE364', 'CWE366', 'CWE369', 'CWE377', 'CWE390', 'CWE400', 'CWE401',
        'CWE404', 'CWE415', 'CWE416', 'CWE426', 'CWE427', 'CWE457', 'CWE459',
        'CWE464', 'CWE467', 'CWE468', 'CWE469', 'CWE475', 'CWE476', 'CWE478',
        'CWE506', 'CWE534', 'CWE535', 'CWE562', 'CWE587', 'CWE588', 'CWE590',
        'CWE591', 'CWE605', 'CWE606', 'CWE615', 'CWE617', 'CWE665', 'CWE666',
        'CWE675', 'CWE680', 'CWE690', 'CWE758', 'CWE761', 'CWE762', 'CWE773',
        'CWE775', 'CWE789', 'CWE843'
    ],
}

SYSEVR_CATEGORY = {
    "AE": 'Arithmetic expression.txt',
    "AF": 'API function call.txt',
    "AU": 'Array usage.txt',
    "PU": 'Pointer usage.txt',
}
