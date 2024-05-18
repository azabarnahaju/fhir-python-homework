from datetime import datetime, timezone
from utils.unit_converter import convert


def create_summary(data, multiple_units):
    """Creates summary of an individual observation"""
    summary_info = data["resource"]

    units_to_convert = get_list_of_units(multiple_units.values())
    measurement_information = get_measurement_information(summary_info, units_to_convert)

    summary = {
        "observationId": summary_info.get("id"),
        "patientId": get_patient_id(summary_info),
        "performerId": get_performer_id(summary_info),
        "measurementCoding": list(get_measurement_coding(summary_info)),
        "measurementValue": [measurement[0] for measurement in measurement_information],
        "measurementUnit": [measurement[1] for measurement in measurement_information],
        "measurementDate": summary_info.get("effectiveDateTime"),
        "dataFetched": get_formatted_current_utc_datetime()
    }

    return summary


def get_patient_id(summary_info):
    """Return Patient ID"""
    if "subject" in summary_info:
        return summary_info["subject"]["reference"].replace("Patient/", "")
    return None


def get_formatted_current_utc_datetime():
    """Return current UTC time formatted according to ISO"""
    return str(datetime.now(timezone.utc).isoformat()).split(".", 1)[0]+"Z"


def get_performer_id(summary_info):
    """Return Performer ID"""
    if "performer" in summary_info:
        return summary_info["performer"][0]["reference"].replace("Practitioner/", "")
    return None


def get_measurement_coding(summary_info):
    """Return measurement codings with LOINC system for an individual observation"""
    if "code" in summary_info and "coding" in summary_info["code"]:
        for coding in summary_info["code"]["coding"]:
            if "system" in coding and "http://loinc.org" in coding["system"]:
                yield coding


def get_measurement_information(summary_info, units_to_convert):
    """Return tuple(s) with measurement value(s) and unit(s) for an individual observation"""
    measurement_info = []

    if "component" in summary_info:
        for component in summary_info["component"]:
            add_measurement_info(component, measurement_info)
    else:
        add_measurement_info(summary_info, measurement_info)

    for i, measurement in enumerate(measurement_info):
        if measurement[1] in units_to_convert:
            converted = convert(measurement[0], measurement[1])
            if converted is not None:
                measurement_info[i] = converted

    return measurement_info


def add_measurement_info(parent, measurement_info):
    """Update list of measurement information with value and unit if they exist"""
    if "valueQuantity" in parent:
        value, unit = None, None
        if "value" in parent["valueQuantity"]:
            value = parent["valueQuantity"]["value"]
        if "unit" in parent["valueQuantity"]:
            unit = parent["valueQuantity"]["unit"]
        measurement_info.append((value, unit))


def get_list_of_units(sets_of_units):
    """Convert list of sets of units to list of units"""
    units_to_convert_lists = []
    for unit in sets_of_units:
        units_to_convert_lists.append(list(unit))
    return sum(units_to_convert_lists, [])
