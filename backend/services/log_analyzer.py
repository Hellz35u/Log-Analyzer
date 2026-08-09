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
            total_response_size += log["response_size"]
    
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
        user_agent = log.get("user_agent")

        if user_agent is None:
            continue

        if user_agent not in requests_per_user_agent:
            requests_per_user_agent[user_agent] = 1
        else:
            requests_per_user_agent[user_agent] += 1

    return requests_per_user_agent

def calculate_success_failure_rate(read_result):
    success = 0
    failure = 0

    for log in read_result["logs"]:
        status_code = int(log["status_code"])
        group = status_code // 100

        if group in (2, 3):
            success += 1
        elif group in (4, 5):
            failure += 1

    total = success + failure

    if total == 0:
        return {
            "success": 0,
            "failure": 0,
            "success_rate": 0,
            "failure_rate": 0
        }

    success_rate = round((success / total) * 100, 2)
    failure_rate = round((failure / total) * 100, 2)

    return {
        "success": success,
        "failure": failure,
        "success_rate": success_rate,
        "failure_rate": failure_rate
    }

def count_errors_per_endpoint(read_result):
    errors_per_endpoint = {}

    for log in read_result["logs"]:
        status_code = int(log["status_code"])

        if 400 <= status_code < 600:
            endpoint = log["path"]
            if endpoint not in errors_per_endpoint:
                errors_per_endpoint[endpoint] = 1
            else:
                errors_per_endpoint[endpoint] += 1

    return errors_per_endpoint

def count_errors_per_ip(read_result):
    errors_per_ip = {}

    for log in read_result["logs"]:
        status_code = int(log["status_code"])

        if 400 <= status_code < 600:
            ip = log["ip"]
            if ip not in errors_per_ip:
                errors_per_ip[ip] = 1
            else:
                errors_per_ip[ip] += 1

    return errors_per_ip

def get_top_items(data, limit=10):
    sorted_items = sorted(data.items(), key=lambda item: item[1], reverse=True)
    return dict(sorted_items[:limit])

def analyze_logs(read_result):
    return {
        "total_requests": count_total_requests(read_result),
        "status": count_status_code(read_result),
        "http_methods": count_http_methods(read_result),
        "unique_ips": count_unique_ips(read_result),
        "requests_per_ip": count_request_per_ip(read_result),
        "requests_per_endpoint": count_request_per_endpoint(read_result),
        "average_response_size": calculate_average_response_size(read_result),
        "total_response_size": calculate_total_response_size(read_result),
        "requests_per_hour": count_requests_per_hour(read_result),
        "user_agents": count_requests_per_user_agent(read_result),
        "success_failure": calculate_success_failure_rate(read_result),
        "errors_per_endpoint": count_errors_per_endpoint(read_result),
        "errors_per_ip": count_errors_per_ip(read_result)
    }
