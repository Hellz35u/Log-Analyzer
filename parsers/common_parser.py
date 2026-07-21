from parsers import LogParser
import re

class CommonParser(LogParser):
    
    def parse(self, line):

        ip = None
        timestamp = None
        method = None
        path = None
        http_version = None
        status_code = None
        response_size = None

        match = re.match(r"^(\S+)", line)
        if match is not None:
            ip = match.group(1)

        match = re.search(r"\[(.*?)\]", line)
        if match is not None:
            timestamp = match.group(1)

        match = re.search(r'"(\S+)\s', line)
        if match is not None:
            method = match.group(1)

        # Path
        match = re.search(r'"\S+\s(\S+)\sHTTP/\S+"', line)
        if match is not None:
            path = match.group(1)

        match = re.search(r'(HTTP/\S+)', line)
        if match is not None:
            http_version = match.group(1)

        match = re.search(r'"\s(\d{3})\s', line)
        if match is not None:
            status_code = int(match.group(1))

        match = re.search(r'"\s\d{3}\s(\d+|-)', line)
        if match is not None:
            value = match.group(1)

            if value == "-":
                response_size = None
            else:
                response_size = int(value)

        result = {
            "ip": ip,
            "timestamp": timestamp,
            "method": method,
            "path": path,
            "http_version": http_version,
            "status_code": status_code,
            "response_size": response_size,
        }

        return result