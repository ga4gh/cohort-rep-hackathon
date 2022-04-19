"""
This script filters a Synthea dataset to create a filtered dataset of all asthma
patients, plus 100 non-asthma patients
"""

import os
import json

def copy_json_file(filename_start, output_filename, input_dir, output_dir):
    input_file = [a for a in os.listdir(input_dir) if a.startswith(filename_start)][0]
    open(os.path.join(output_dir, output_filename + ".json"), "w").write(
        open(os.path.join(input_dir, input_file), "r").read()
    )

def output_filtered_records(fhir_model, input_dir, output_dir, all_patient_ids, subject_key="subject"):
    filtered_records = []
    for record in open(os.path.join(input_dir, fhir_model + ".ndjson")):
        record_json = json.loads(record)
        patient_id = record_json[subject_key]["reference"].split("/")[-1]
        if patient_id in all_patient_ids:
            filtered_records.append(record)
    open(os.path.join(output_dir, fhir_model + ".ndjson"), "w").write("".join(filtered_records))

def main():
    ##################################################
    # PARSE PROGRAM INPUTS
    ##################################################
    default_input_dir = os.path.join("output", "synthea", "raw", "fhir")
    custom_input_dir = os.getenv("GA4GH_DEMO_INPUT_DIR")
    input_dir = custom_input_dir if custom_input_dir else default_input_dir

    default_output_dir = os.path.join("output", "synthea", "filtered", "fhir")
    custom_output_dir = os.getenv("GA4GH_DEMO_OUTPUT_DIR")
    output_dir = custom_output_dir if custom_output_dir else default_output_dir

    ##################################################
    # DATA WRANGLING
    ##################################################

    total_non_asthma_patients = 100
    n_non_asthma = 0

    patient_conditions = {} # maps patient id to condition json
    patient_patients = {} # maps patient id to patient json

    asthma_patient_ids = set()
    non_asthma_patient_ids = set()

    # iterate through "Conditions" file
    # get all patient ids for patients with asthma
    # get map of patient id to condition
    for condition in open(os.path.join(input_dir, "Condition.ndjson")):
        condition_json = json.loads(condition)

        condition_code_text = condition_json["code"]["text"]
        patient_text = condition_json["subject"]["reference"]
        patient_id = patient_text.split("/")[-1]

        if patient_id not in patient_conditions.keys():
            patient_conditions[patient_id] = []

        patient_conditions[patient_id].append(condition)

        if "asthma" in condition_code_text.lower():
            asthma_patient_ids.add(patient_id)
    
    # iterate through "Patients" file
    # get all asthma patients
    # get first 100 non asthma patients
    for patient in open(os.path.join(input_dir, "Patient.ndjson")):
        patient_json = json.loads(patient)
        patient_id = patient_json["id"]
        if patient_id in asthma_patient_ids:
            patient_patients[patient_id] = patient
        else:
            if n_non_asthma < total_non_asthma_patients:
                patient_patients[patient_id] = patient
                non_asthma_patient_ids.add(patient_id)
                n_non_asthma += 1
    
    sorted_asthma_patient_ids = sorted(list(asthma_patient_ids))
    sorted_non_asthma_patient_ids = sorted(list(non_asthma_patient_ids))
    sorted_patient_ids = sorted_asthma_patient_ids + sorted_non_asthma_patient_ids
    all_patient_ids = set(sorted_patient_ids)

    ##################################################
    # OUTPUT
    ##################################################

    # copy all practitioner and hospital JSON 
    copy_json_file("practitionerInformation", "PractitionerInformation", input_dir, output_dir)
    copy_json_file("hospitalInformation", "HospitalInformation", input_dir, output_dir)

    # output filtered patients
    filtered_patients = [patient_patients[patient_id] for patient_id in sorted_patient_ids]
    open(os.path.join(output_dir, "Patient.ndjson"), "w").write("".join(filtered_patients))

    # output filtered conditions
    filtered_conditions = []
    for patient_id in sorted_patient_ids:
        if patient_id in patient_conditions.keys():
            filtered_conditions += patient_conditions[patient_id]
    open(os.path.join(output_dir, "Condition.ndjson"), "w").write("".join(filtered_conditions))

    output_filtered_records("Encounter", input_dir, output_dir, all_patient_ids)
    output_filtered_records("Immunization", input_dir, output_dir, all_patient_ids, subject_key="patient")
    output_filtered_records("Observation", input_dir, output_dir, all_patient_ids)
    output_filtered_records("DiagnosticReport", input_dir, output_dir, all_patient_ids)
    output_filtered_records("DocumentReference", input_dir, output_dir, all_patient_ids)
    output_filtered_records("Procedure", input_dir, output_dir, all_patient_ids)

if __name__ == "__main__":
    main()
