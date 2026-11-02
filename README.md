# network-device-inventory-validator

Validate a switch/router inventory: every IP must parse, every model must be known, and firmware must meet that model's minimum version.

## How to run

```sh
python3 main.py devices.csv
```

## Example output

```
sw1: VALID
sw2: INVALID: firmware below minimum 15.2
1 invalid device(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
