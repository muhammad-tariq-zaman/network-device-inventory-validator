"""Validate a network-device inventory CSV: IPs, models, firmware.

Usage: python3 main.py devices.csv
CSV columns: device,ip,model,firmware
Checks: IP parses, model is in the known list, firmware is at least the
minimum for that model. Each row gets VALID or a list of problems.
"""
import argparse, csv, sys, ipaddress

MIN_FIRMWARE = {"Cisco-2960": (15, 2), "Cisco-9200": (17, 3),
                "HP-2530": (16, 10), "Juniper-EX2300": (21, 2)}


def parse_version(text):
    parts = text.strip().split(".")
    if len(parts) < 2 or not all(p.isdigit() for p in parts[:2]):
        return None
    return (int(parts[0]), int(parts[1]))


def validate(row):
    problems = []
    try:
        ipaddress.ip_address(row["ip"].strip())
    except ValueError:
        problems.append("invalid IP")
    model = row["model"].strip()
    if model not in MIN_FIRMWARE:
        problems.append("unknown model")
    else:
        version = parse_version(row["firmware"])
        if version is None:
            problems.append("unparsable firmware")
        elif version < MIN_FIRMWARE[model]:
            problems.append(f"firmware below minimum {'.'.join(map(str, MIN_FIRMWARE[model]))}")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    invalid = 0
    with open(args.path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            problems = validate(row)
            if problems:
                invalid += 1
            print(f"{row['device']}: {'VALID' if not problems else 'INVALID: ' + '; '.join(problems)}")
    print(f"{invalid} invalid device(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
