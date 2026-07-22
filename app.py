from parsers.combined_parser import CombinedParser
from parsers.common_parser import CommonParser
from services.log_reader import read_log_file


def choose_parser(parser_type):
    if parser_type == "common":
        return CommonParser()
    
    elif parser_type == "combined":
        return CombinedParser()
    
    else:
        raise ValueError("Unsupported parser_type!")

    
def main():
    parser_type = input("Enter parser type (common/combined): ").lower()
    file_path = input("Enter file path: ")

    try:
        parser = choose_parser(parser_type)
        parsed_logs = read_log_file(file_path,parser)

        print(f"Successfully parsed {len(parsed_logs)} log lines")

        for log in parsed_logs:
            print(log)

    except FileNotFoundError:
        print("Log file was not found.")
    
    except PermissionError:
        print("you do not have permission to read this file.")
    
    except ValueError as error:
        print(f"{error}")

if __name__ == "__main__":
    main()
