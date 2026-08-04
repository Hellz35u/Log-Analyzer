
def read_log_file(file_path, parser):
    parsed_logs = []
    
    failed_lines = 0
    total_lines = 0
    parsed_lines = 0

    with open(file_path,"r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            
            total_lines += 1

            try:
                parsed_log = parser.parse(line)
                parsed_logs.append(parsed_log)
                parsed_lines += 1

            except ValueError as error:
                failed_lines += 1
                print(f"Error in line {line_number}: {error}")
    
    read_result = {
        "logs": parsed_logs,
        "total_lines": total_lines,
        "parsed_lines": parsed_lines,
        "failed_lines": failed_lines
    }

    return read_result