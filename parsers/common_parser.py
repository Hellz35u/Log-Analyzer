from parsers import LogParser
import re

class CommonParser(LogParser):
    
    pattern = re.compile(
            r'^(\S+) \S+ \S+ \[(.*?)\] '
            r'"(\S+) (\S+) (\S+)" '
            r'(\d{3}) (\S+) '
        )


    def parse(self, line):

        match = self.pattern.match(line)
        
        if not match:
            raise ValueError("Invalid Common Log format.")

        ip = match.group(1)
        timestamp = match.group(2)
        method = match.group(3)
        path = match.group(4)
        http_version = match.group(5)
        status_code = int(match.group(6))
        response_size = match.group(7)
        if response_size == "-":
            response_size = None
        else:
            response_size = int(match.group(7))

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