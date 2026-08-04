from datetime import datetime

def count_total_requests(read_result):
    return len(read_result["logs"])

def count_status_code(read_result):
    status_codes = {}
    status_groups = {
        "1xx": 0,
        "2xx": 0,
        "3xx": 0,
        "4xx": 0,
        "5xx": 0
    }

    for log in read_result["logs"]:
        status_code = log["status_code"]
        group = int(status_code) // 100
        group_name = f"{group}xx"

        if group_name in status_groups:
            status_groups[group_name] +=1

        if status_code in status_codes:
            status_codes[status_code] += 1
        else:
            status_codes[status_code] = 1

    status_analysis = {
        "status_codes": status_codes,
        "status_groups": status_groups
    }
    
    return status_analysis

def count_http_methods(read_result):
    http_methods = {
        "GET": 0,
        "POST": 0,
        "PUT": 0,
        "DELETE": 0,
        "PATCH": 0,
        "HEAD": 0,
        "OPTIONS": 0,
        "CONNECT": 0,
        "TRACE": 0
    }

    for log in read_result["logs"]:
        method = log["method"]
        
        if method in http_methods:
            http_methods[method] += 1
    
    return http_methods


def count_unique_ips(read_result):
    unique_ips = set()

    for log in read_result["logs"]:
        ip = log["ip"]
        unique_ips.add(ip)

    return len(unique_ips)    

def count_request_per_ip(read_result):
    requests_per_ip = {}
    
    for log in read_result["logs"]:
        ip = log["ip"]
        if ip not in requests_per_ip:
            requests_per_ip[ip] = 1
        else:
            requests_per_ip[ip] += 1
    
    return requests_per_ip

def count_request_per_endpoint(read_result):
    request_per_endpoint = {}
    for log in read_result["logs"]:
        endpoint = log["path"]
        if endpoint not in request_per_endpoint:
            request_per_endpoint[endpoint] = 1
        else:
            request_per_endpoint[endpoint] += 1
    
    return request_per_endpoint

def calculate_average_response_size(read_result):
    total_response_size = 0
    count = 0
    for log in read_result["logs"]:
        
        if log["response_size"] is not None:
            total_response_size += log["response_size"]
            count += 1

        if count == 0:
            return 0

    return total_response_size / count

def calculate_total_response_size(read_result):
    total_response_size = 0
    for log in read_result["logs"]:
        if log["response_size"] is not None:
            total_response_size += 1
    
    return total_response_size

def count_requests_per_hour(read_result):
    requests_per_hour = {}
    for log in read_result["logs"]:
        timestamp = log["timestamp"]
        dt = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
        hour = dt.hour
        if hour not in requests_per_hour:
            requests_per_hour[hour] = 1
        else:
            requests_per_hour[hour] += 1
    
    return requests_per_hour

#not in common log format only in combined log format
def count_requests_per_user_agent(read_result):
    requests_per_user_agent = {}
    for log in read_result["logs"]:
        user_agent = log["user_agent"]
        if user_agent not in requests_per_user_agent:
            requests_per_user_agent[user_agent] = 1
        else:
            requests_per_user_agent[user_agent] += 1
    
    return requests_per_user_agent
        
