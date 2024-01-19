import pycozmo

def main():
    with pycozmo.connect() as cli:
        # ... other setup code ...

        # Get the battery voltage
        battery_voltage = cli.battery_voltage
        print(f"Battery Voltage: {battery_voltage:.2f}V")

        # ... the rest of your main function ...
if __name__== '__main__':
    main()
    