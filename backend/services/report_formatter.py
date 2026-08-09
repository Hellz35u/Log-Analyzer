def format_analysis_result(analysis_result):
    print("\n===== LOG ANALYSIS =====")
    print(f"Total requests: {analysis_result['total_requests']}")
    print(f"Unique IPs: {analysis_result['unique_ips']}")
    print(f"Average response size: {analysis_result['average_response_size']}")
    print(f"Total response size: {analysis_result['total_response_size']}")

    print("\nStatus groups:")
    for group, count in analysis_result["status"]["status_groups"].items():
        print(f"{group}: {count}")

    print("\nHTTP methods:")
    for method, count in analysis_result["http_methods"].items():
        print(f"{method}: {count}")