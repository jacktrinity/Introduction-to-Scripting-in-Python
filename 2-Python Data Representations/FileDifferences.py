"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

CodeSkulptor: https://py3.codeskulptor.org/#save3_RvkzYOZaAv.py
"""

IDENTICAL = -1


def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """

    if len(line1) > len(line2):
        short_line = line2
        long_line = line1
    else:
        short_line = line1
        long_line = line2

    index_start = 0
    index_end = len(short_line)

    while index_start < index_end:
        if short_line[index_start] is not long_line[index_start]:
            return index_start

        index_start += 1

    if len(short_line) == len(long_line):
        return IDENTICAL
    else:
        return index_start


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """

    # Check to see if there is any newline or return in line1 and line2.
    if ("\n" in line1) or ("\n" in line2) or ("\r" in line1) or ("\r" in line2):
        return ""

    # If the idx is correct, form the format of the return.
    if 0 <= idx <= min(len(line1), len(line2)):
        difference_format_string = ""

        num_in_idx = 0
        while num_in_idx < idx:
            difference_format_string += "="
            num_in_idx += 1
        difference_format_string += "^"

        format_string = line1 + "\n" + difference_format_string + "\n" + line2 + "\n"
        return format_string
    # If the idx is incorrect.
    else:
        return ""


def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """

    start_index = 0
    end_index = min(len(lines1), len(lines2))

    # Return the first difference
    while start_index < end_index:
        diff_index = singleline_diff(lines1[start_index], lines2[start_index])

        if diff_index > -1:
            return (start_index, diff_index)
        else:
            start_index += 1

    # Return if identical.
    if len(lines1) == len(lines2):
        return (IDENTICAL, IDENTICAL)
    # Return if identical short.
    else:
        return (start_index, 0)


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """

    openfile = open(filename, "rt")

    list_of_lines = openfile.readlines()
    list_of_lines_without_newline = []

    for newline in list_of_lines:
        #  Getting rid of any new line.
        if ("\n" in newline) or ("\r" in newline):
            list_of_lines_without_newline.append(newline[:-1])
        else:
            list_of_lines_without_newline.append(newline)

    openfile.close()

    return list_of_lines_without_newline


def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """

    list_line1 = get_file_lines(filename1)
    list_line2 = get_file_lines(filename2)

    index_diff = multiline_diff(list_line1, list_line2)

    # If the list of lines are the same.
    if index_diff == (IDENTICAL, IDENTICAL):
        return "No differences\n"
    else:
        diff_line = index_diff[0]
        diff_idx = index_diff[1]

        intro_string = "Line {}:".format(str(diff_line))

        #  General Case
        if (diff_line < len(list_line1)) and (diff_line < len(list_line2)):
            first_list = list_line1[diff_line]
            second_list = list_line2[diff_line]

            format_str = singleline_diff_format(first_list, second_list, diff_idx)
            final_string = intro_string + "\n" + format_str
            return final_string
        # If the list are the same, but one is shorter.
        else:
            if len(list_line1) > len(list_line2):
                first_list = list_line1[diff_line]
                final_string = intro_string + "\n" + first_list + "\n^\n" + "\n"
            else:
                second_list = list_line2[diff_line]
                final_string = intro_string + "\n\n^\n" + second_list + "\n"
        return final_string
