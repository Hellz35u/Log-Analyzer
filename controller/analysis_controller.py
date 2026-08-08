from services.log_reader import read_log_file
from services.log_analyzer import analyze_logs

def analyze_log_file(file_path, parser):
    read_result = read_log_file(file_path, parser)
    analysis_result = analyze_log_file(read_result)

    return analysis_result
