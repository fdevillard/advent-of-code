import sys


def replace_string_digit(s: str) -> str:
    if not s:
        return ""

    if s[0].isdigit():
        return s[0] + replace_string_digit(s[1:])

    numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for i, numberInString in enumerate(numbers, start=1):
        if s.startswith(numberInString):
            return str(i) + replace_string_digit(s[1:])

    return replace_string_digit(s[1:])


def sum_calibration_values(lines):
    total_sum = 0

    for line in lines:
        # for case two, sub string to digit:
        initial = line
        line = replace_string_digit(line)

        # Filter out non-digit characters and extract the first and last digits
        digits = [char for char in line if char.isdigit()]
        first_digit, last_digit = digits[0], digits[-1]

        # Calculate the calibration value and add it to the total sum
        calibration_value = int(first_digit + last_digit)
        total_sum += calibration_value

    return total_sum


if __name__ == "__main__":
    print(sum_calibration_values(sys.stdin))
