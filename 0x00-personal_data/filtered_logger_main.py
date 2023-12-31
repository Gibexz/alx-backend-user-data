#!/usr/bin/env python3
"""
module: filtered_logger.py
"""
import re

import re

def filter_datum(fields, redaction, message, separator):
    regex = '|'.join([re.escape(field) for field in fields])
    return re.sub(f'({regex})=[^{separator}]*', f'\\1={redaction}', message)