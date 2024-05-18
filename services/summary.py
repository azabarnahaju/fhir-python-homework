from datetime import datetime, timezone


def create_summary(data):
    """Creates summary of an individual observation"""
    summary_info = data["resource"]
    summary = {
        "observationId": summary_info.get("id"),
        "patientId": get_patient_id(summary_info),
        "performerId": get_performer_id(summary_info),
        "measurementCoding": list(get_measurement_coding(summary_info)),
        "measurementValue": get_measurement_information(summary_info, "value"),
        "measurementUnit": get_measurement_information(summary_info, "unit"),
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


def get_measurement_information(summary_info, data_type):
    """Return measurement information for an individual observation based on the data type given (value | unit)"""
    if "valueQuantity" in summary_info:
        if data_type in summary_info["valueQuantity"]:
            return [summary_info["valueQuantity"][data_type]]

    if "component" in summary_info:
        values = []
        for component in summary_info["component"]:
            if "valueQuantity" in component and data_type in component["valueQuantity"]:
                values.append(component["valueQuantity"][data_type])
        return values

    return None
