from pint import UnitRegistry

# 2 solutions for unit conversion
# pint conversion -> considerably slower, but more precise (~5.5s)
# manual conversion -> much faster, but less precise (~14ms)


def convert(value, unit):
    """Return a tuple with the manually converted value and the unit it is converted to"""
    if unit == "cm":
        return round(value / 100, 2), "m"
    if unit == "lb":
        return round(value / 2.2, 1), "kg"
    if unit == "g/dl":
        return value, "g/dL"


def convert_pint(value, unit):
    """Return a tuple with the converted value and the unit it is converted to using pint"""
    ureg = UnitRegistry()
    if unit == "cm":
        height = value * ureg.centimeters
        converted_value = height.to(ureg.meters)
        return round(converted_value.magnitude, 2), "m"
    if unit == "lb":
        weight = value * ureg.pounds
        converted_value = weight.to(ureg.kilograms)
        return round(converted_value.magnitude), "kg"
    if unit == "g/dl":
        return value, "g/dL"


def get_multiple_units(data):
    """Print and return a dictionary with all the observation types that use multiple units."""
    units = {}

    for observation in data:
        if "code" in observation["resource"] and "text" in observation['resource']['code']:
            observation_type = observation['resource']['code']['text'].strip().lower()
            if observation_type not in units.keys():
                units[observation_type] = set()

            if "valueQuantity" in observation["resource"] and "unit" in observation["resource"]["valueQuantity"]:
                units[observation_type].add(observation["resource"]["valueQuantity"]["unit"])
            elif "component" in observation["resource"]:
                for component in observation["resource"]["component"]:
                    if "valueQuantity" in component and "unit" in component["valueQuantity"]:
                        units[observation_type].add(component["valueQuantity"]["unit"])

    multiple_units = dict(filter(unit_filtering_function, units.items()))
    print(multiple_units)
    return multiple_units


def unit_filtering_function(pair):
    """Return True if there's more than 1 unit"""
    key, value = pair
    if len(value) > 1:
        return True
    return False
