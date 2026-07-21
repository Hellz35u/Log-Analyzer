
def read_log_file(file_path, parser):
    parsed_logs = []

    with open(file_path,"r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                parsed_log = parser.parse(line)
                parsed_logs.append(parsed_log)

            except ValueError as error:
                print(f"Error in line {line_number}: {error}")
            
    return parsed_logs