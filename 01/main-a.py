import sys

def sum_calibration_values(lines):
    total_sum = 0

    for line in lines:
        # Filter out non-digit characters and extract the first and last digits
        digits = [char for char in line if char.isdigit()]
        first_digit, last_digit = digits[0], digits[-1]

        # Calculate the calibration value and add it to the total sum
        calibration_value = int(first_digit + last_digit)
        total_sum += calibration_value

    return total_sum

if __name__ == "__main__":
    print(sum_calibration_values(sys.stdin))