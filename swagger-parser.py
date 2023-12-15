import json
import os
import argparse

def parse_openapi_json(file_path):
    """
    Parses an OpenAPI JSON file to extract API endpoints and other relevant details.
    """
    try:
        with open(file_path, 'r') as file:
            api_data = json.load(file)
    except Exception as e:
        return f"Error reading {file_path}: {e}\n"

    output = []

    if 'paths' in api_data:
        for path, methods in api_data['paths'].items():
            for method, details in methods.items():
                summary = details.get('summary', 'No summary')
                parameters = details.get('parameters', [])
                responses = details.get('responses', {})

                output.append(f"File: {file_path}\nEndpoint: {path}\n  Method: {method.upper()}\n  Summary: {summary}\n")

                if parameters:
                    output.append("  Parameters:\n")
                    for param in parameters:
                        output.append(f"    - {param.get('name')} ({param.get('in')}): {param.get('description', 'No description')}\n")

                output.append("  Responses:\n")
                for status_code, response in responses.items():
                    output.append(f"    - {status_code}: {response.get('description', 'No description')}\n")

                output.append("\n")
    else:
        output.append(f"No paths found in {file_path}.\n")

    return ''.join(output)


def parse_json_files_in_directory(directory):
    """
    Searches for all .json files in a given directory and parses them.
    """
    combined_output = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            combined_output.append(parse_openapi_json(file_path))
    return ''.join(combined_output)


def main():
    parser = argparse.ArgumentParser(description='Parse OpenAPI JSON files in a specified directory.')
    parser.add_argument('directory', type=str, help='Directory containing JSON files to parse')
    args = parser.parse_args()

    parsed_output = parse_json_files_in_directory(args.directory)
    print(parsed_output)


if __name__ == "__main__":
    main()

