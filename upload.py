import os
import json
import requests

class FhirBatchUploader(object):
    
    def __init__(self, fhir_dir, fhir_server_url, model):
        self.fhir_dir = fhir_dir
        self.fhir_server_url = fhir_server_url
        self.model = model
    
    def batch_upload(self):
        status_code_counts = {}
        ndjson_file = os.path.join(self.fhir_dir, self.model + ".ndjson")
        for record in open(ndjson_file, "r"):
            payload = record.strip()
            fhir_instance_uploader = FhirInstanceUploader(self.fhir_server_url, self.model, payload)
            status_code = fhir_instance_uploader.upload()
            if status_code not in status_code_counts.keys():
                status_code_counts[status_code] = 0
            status_code_counts[status_code] += 1
        print("%s batch upload complete, operation counts: %s" % (self.model, str(status_code_counts)))

class FhirInstanceUploader(object):
    
    def __init__(self, fhir_server_url, model, payload):
        self.fhir_server_url = fhir_server_url
        self.model = model
        self.payload = payload
    
    def upload(self):
        payload_json = json.loads(self.payload)
        object_id = payload_json["id"]
        url = "%sfhir/%s/%s" % (self.fhir_server_url, self.model, object_id)
        response = requests.put(url, json=payload_json)

        if response.status_code != 200 and response.status_code != 201:
            print("failed to upload %s %s" % (self.model, object_id))
            print(response.status_code)
            print(response.text)
            print("---")

        return response.status_code

def upload_from_json_list_file(input_filename, fhir_dir, fhir_server_url):
    input_file = open(os.path.join(fhir_dir, input_filename + ".json"), "r")
    all_json = json.load(input_file)
    counts_d = {}
    for entry_json in all_json["entry"]:
        resource_json = entry_json["resource"]
        resource_type = resource_json["resourceType"]
        resource_id = resource_json["id"]
        url = "%sfhir/%s/%s" % (fhir_server_url, resource_type, resource_id)
        response = requests.put(url, json=resource_json)
        if response.status_code not in counts_d.keys():
            counts_d[response.status_code] = 0
        counts_d[response.status_code] += 1
    print(input_filename + " upload attempt finished: " + str(counts_d))

def main():

    # parse program inputs from environment
    default_fhir_dir = os.path.join("output", "synthea", "filtered", "fhir")
    custom_fhir_dir = os.getenv("GA4GH_DEMO_FHIR_DIR")
    fhir_dir = custom_fhir_dir if custom_fhir_dir else default_fhir_dir

    default_fhir_server_url = "http://localhost:8080/"
    custom_fhir_server_url = os.getenv("GA4GH_DEMO_FHIR_SERVER_URL")
    fhir_server_url = custom_fhir_server_url if custom_fhir_server_url else default_fhir_server_url
    if fhir_server_url.endswith("/") == False:
        fhir_server_url += "/"
    
    # upload Practitioner and Hospital Information
    upload_from_json_list_file("PractitionerInformation", fhir_dir, fhir_server_url)
    upload_from_json_list_file("HospitalInformation", fhir_dir, fhir_server_url)

    # run the upload in the correct sequence
    ordered_models = [
        "Patient",
        "Encounter",
        "Condition",
        "Immunization",
        "Observation",
        "DiagnosticReport",
        "DocumentReference",
        "Procedure"
    ]

    for model in ordered_models:
        fhir_batch_uploader = FhirBatchUploader(fhir_dir, fhir_server_url, model)
        fhir_batch_uploader.batch_upload()

if __name__ == "__main__":
    main()
