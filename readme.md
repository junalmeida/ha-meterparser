

# Home Assistant - Meter Parser Integration

This is a custom component to allow parse of dial utility meters to provide energy consumption information to home assistant using a regular ip camera.

### Highlights of what **Meter Parser** can do

* Parse Meters
* Provide a consumption sensor
* Cheap IP or PoE cameras must do

### Potential Downsides

* Positioning a camera and getting a good image could be difficult.
* Could be hard to setup calibration parameters

## Installation (HACS) - Highly Recommended

1. Have HACS installed, this will allow you to easily update
2. Add [https://github.com/junalmeida/ha-meterparser](https://github.com/junalmeida/ha-meterparser) as a custom
   repository as Type: Integration
3. Click install under "Meter Parser Integration" in the Integration tab
4. Restart HA
5. Navigate to _Integrations_ in the config interface.
6. Click _ADD INTEGRATION_
7. Search for _Meter Parser Integration_
8. Put the email for wyze in the first box and your password in the second
9. Click _SUBMIT_ and profit!

## Usage

* Entities will show up as `sensor.<friendly name>`, for example (`sensor.watermeter`).

## Support

If you need help with anything then please connect with the community!

* For bugs or feature requests create an issue

## Reporting an Issue

1. Setup your logger to print debug messages for this component by adding this to your `configuration.yaml`:
    ```yaml
    logger:
     default: warning
     logs:
       custom_components.meterparser: debug
       meterparser: debug
    ```
2. Restart HA
3. Verify you're still having the issue
4. File an issue in this Github Repository (being sure to fill out every provided field)
