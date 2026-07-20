import re
from datetime import datetime
from sqlite3.dbapi2 import Timestamp

def parser(line):
    match = re.match(r"^(\S+)", line)
    if match is not None:
        ip = match.group(1)

    match = re.search(r"\[(.*?)\]",line)
    if match is not None:
        timestamp = match.group(1)
    
    match = re.search(r'"(\S+)\s', line)
    if match is not None:
        method = match.group(1)
    
    match = re.search(r'/(\S*)', line)
    if match is not None:
        path = match.group(1)
    
    match = re.search(r'(HTTP/\S+)', line)
    if match is None:
        http_version = match.group(1)