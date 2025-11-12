"""
Time Parser Module for Clip Assassin Resolve
Converts various time formats to seconds
"""

import re


def parse_time_range(range_string):
    """
    Parse a time range string like "1m57-2m08" or "1:57-2:08"

    Args:
        range_string: String in format "start-end"

    Returns:
        tuple: (start_seconds, end_seconds) or None if invalid
    """
    # Replace different dash types with standard hyphen
    range_string = range_string.replace('\u2013', '-')  # en dash
    range_string = range_string.replace('\u2014', '-')  # em dash

    # Remove spaces
    range_string = range_string.strip().replace(' ', '')

    # Split by hyphen
    parts = range_string.split('-')

    if len(parts) < 2:
        return None

    # Parse start and end times
    start = parse_time(parts[0])
    end = parse_time(parts[-1])

    if start is None or end is None:
        return None

    if end <= start:
        return None

    return (start, end)


def parse_time(time_string):
    """
    Parse a single time string like "1m57", "1:57", "0:02:25", "1h30m45"

    Supported formats:
    - 1m57s or 1m57 (minutes and seconds with 'm')
    - 1:57 (MM:SS)
    - 0:02:25 (HH:MM:SS)
    - 1h30m45s or 1h30m (hours, minutes, seconds with 'h', 'm', 's')
    - 90 (just seconds as number)

    Args:
        time_string: Time string to parse

    Returns:
        float: Time in seconds, or None if invalid
    """
    if not time_string:
        return None

    time_string = time_string.strip().lower()

    hours = 0
    minutes = 0
    seconds = 0

    # Format: 1h30m45s or 1h30m or combinations with "h", "m", "s"
    if 'h' in time_string:
        h_parts = time_string.split('h')
        try:
            hours = int(h_parts[0])
        except ValueError:
            return None

        if len(h_parts) > 1 and h_parts[1]:
            rest = h_parts[1]
            if 'm' in rest:
                m_parts = rest.split('m')
                try:
                    minutes = int(m_parts[0])
                except ValueError:
                    return None
                if len(m_parts) > 1 and m_parts[1]:
                    try:
                        seconds = int(m_parts[1].replace('s', ''))
                    except ValueError:
                        return None
            else:
                try:
                    seconds = int(rest.replace('s', ''))
                except ValueError:
                    return None

    # Format: 1m57s or 1m57
    elif 'm' in time_string:
        m_parts = time_string.split('m')
        try:
            minutes = int(m_parts[0])
        except ValueError:
            return None

        if len(m_parts) > 1 and m_parts[1]:
            try:
                seconds = int(m_parts[1].replace('s', ''))
            except ValueError:
                return None

    # Format: 0:02:25 or 1:57:30 or 1:57
    elif ':' in time_string:
        colon_parts = time_string.split(':')

        try:
            if len(colon_parts) == 2:
                # MM:SS
                minutes = int(colon_parts[0])
                seconds = int(colon_parts[1])
            elif len(colon_parts) == 3:
                # HH:MM:SS
                hours = int(colon_parts[0])
                minutes = int(colon_parts[1])
                seconds = int(colon_parts[2])
            elif len(colon_parts) == 1:
                # Just a number
                seconds = int(colon_parts[0])
        except ValueError:
            return None

    # Just a number = seconds
    else:
        try:
            seconds = int(time_string.replace('s', ''))
        except ValueError:
            return None

    # Validate non-negative
    if hours < 0 or minutes < 0 or seconds < 0:
        return None

    return hours * 3600 + minutes * 60 + seconds


def parse_timecodes(timecodes_text):
    """
    Parse multiple time ranges from text (one per line)

    Args:
        timecodes_text: Multi-line string with time ranges

    Returns:
        list: List of tuples [(start, end), ...] sorted by start time
    """
    lines = timecodes_text.strip().split('\n')
    ranges = []
    errors = []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        parsed = parse_time_range(line)
        if parsed:
            ranges.append(parsed)
        else:
            errors.append(f"Line {i+1}: '{line}' - invalid format")

    # Sort by start time
    ranges.sort(key=lambda x: x[0])

    return ranges, errors


def format_seconds(seconds):
    """
    Convert seconds to readable format HH:MM:SS

    Args:
        seconds: Time in seconds

    Returns:
        str: Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


# Testing
if __name__ == "__main__":
    test_cases = [
        "1m57-2m08",
        "1:57-2:08",
        "0:02:25-0:02:45",
        "1h15m30-1h16m00",
        "1m57 - 2m08",
        "1m57–2m08",
        "90-120",
    ]

    print("Testing time parser:")
    print("-" * 50)
    for test in test_cases:
        result = parse_time_range(test)
        if result:
            start, end = result
            print(f"[OK] '{test}' -> {format_seconds(start)} to {format_seconds(end)}")
        else:
            print(f"[FAIL] '{test}' -> FAILED")
