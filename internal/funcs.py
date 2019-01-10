#
#    Copyright (C) Codeplay Software Limited. All Rights Reserved.
#
import subprocess


def get_space_count(line):
    """Gets number of spaces at start of line to preserve indenting"""
    return len(line) - len(line.lstrip())


def add_spaces_to_lines(count, string):
    """Adds a number of spaces to the start of each line
    Doesn't add spaces to the first line, as it should already be
    fully indented"""
    all_lines = string.splitlines(True)
    new_string = all_lines[0]
    for i in range(1, len(all_lines)):
        new_string += ' ' * count + all_lines[i]
    return new_string


def read_from_file(file_name):
    """Reads from the given file name with .in appended
    Returns the read file"""
    with open(file_name, 'r') as input_file:
        return input_file.read()


def insert_in_source(file_source, insertion_point, replacement_string):
    """Replaces insertion_point with replacement_string in the str file_source
    Returns the updated str"""
    # Get the number of spaces before insertion_point
    space_count = 0
    for line in file_source.splitlines(True):
        if insertion_point in line:
            space_count = get_space_count(line)
    # Add spaces to each line in replacement_string to keep it in line with the
    # other code in the source
    replacement_string = add_spaces_to_lines(space_count, replacement_string)
    # Replace insertion_point with the formatted replacement_string and return
    return file_source.replace(insertion_point, replacement_string)


def write_to_file(file_name, file_source):
    """Discard writes file_source to file_name"""
    with open(file_name, 'w') as output_file:
        output_file.write(file_source)


def clang_format(file_name, clang_format_script):
    """Calls the input clang formatting script in a subprocess shell call.
    Provides the input filename as the only arguement to the script."""
    try:
        subprocess.check_call(
            clang_format_script + " " + str(file_name), shell=True)
    except subprocess.CalledProcessError as cperror:
        print("Call to " + clang_format_script + " failed")
        print("Exit code: " + str(cperror.returncode))
