from parsers.combined_parser import CombinedParser
from parsers.common_parser import CommonParser
from controller.analysis_controller import analyze_log_file
from services.report_formatter import format_analysis_result

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

        analysis_result = analyze_log_file(file_path, parser)

        print("Analysis completed successfully.")
        format_analysis_result(analysis_result)

    except FileNotFoundError:
        print("Log file was not found.")

    except PermissionError:
        print("You do not have permission to read this file.")

    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()