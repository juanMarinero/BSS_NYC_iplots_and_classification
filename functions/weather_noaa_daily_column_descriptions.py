#  vim: set foldmethod=indent foldcolumn=8 :
#!/usr/bin/env python3

import re
import urllib.request

# URL of the readme.txt file
URL = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt"


def main(url=URL):
    # Fetch the content of the text file
    with urllib.request.urlopen(url) as response:
        text = response.read().decode("utf-8")

    # Find the starting index of the variable definitions section
    start_index = text.find("These variables have the following definitions:")

    # Ensure start_index is found
    if start_index == -1:
        raise ValueError("Start index not found.")

    # Cut the text before start_index
    text = text[start_index:]

    # Use regular expression to find the end index
    end_match = re.search(r"VALUE1(.*)", text)
    if end_match:
        end_index = end_match.start()
    else:
        raise ValueError("End index not found.")

    # Extract the variable definitions section
    definitions_text = text[:end_index].strip()

    # Initialize a dictionary
    column_definitions = dict()

    # Extract individual variable blocks
    variable_blocks = definitions_text.split("\n\n")

    # Iterate over each variable block
    for block in variable_blocks:
        # Split the block by lines
        lines = block.split("\n")

        # Initialize variables to store the column name and definition
        column_name = None
        column_name_non_num = ""
        definition_lines = []

        # Extract the variable name and its definition
        for line in lines:
            if "=" in line:
                # Check if the string before the equal sign is not just numeric
                parts = line.split("=")
                var_name = parts[0].strip()
                if not var_name.isdigit() or (
                    var_name.isdigit()
                    and (
                        column_name_non_num.startswith("WT")
                        or column_name_non_num.startswith("WV")
                    )
                ):
                    # Store the previous column's definition (if any)
                    if column_name is not None:
                        definition = " ".join(definition_lines).strip()
                        column_definitions[column_name] = definition

                    # Extract the column name from the current line
                    column_name = var_name
                    if not var_name.isdigit():
                        column_name_non_num = var_name
                    else:
                        if column_name_non_num.startswith("WT"):
                            column_name = "WT" + column_name
                        elif column_name_non_num.startswith("WV"):
                            column_name = "WV" + column_name

                    # Start a new list for the definition lines
                    definition_lines = [parts[1].strip()]
                else:
                    # Append the line to the definition lines
                    definition_lines.append(parts[1].strip())
            elif column_name is not None:
                # Collect lines of the definition
                definition_lines.append(line.strip())

        # Store the last column's definition (if any)
        if column_name is not None:
            definition = " ".join(definition_lines).strip()
            column_definitions[column_name] = definition

    return column_definitions


if __name__ == "__main__":

    column_definitions = main()

    # Print the extracted column definitions
    for column, definition in column_definitions.items():
        print(f"{column}: {definition}")
