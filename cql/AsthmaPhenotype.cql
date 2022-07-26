library "AsthmaPhenotype" version '1.0.0'

using FHIR version '4.0.1'

include FHIRHelpers version '4.0.1'

codesystem "SNOMED": 'http://snomed.info/sct'

code "Asthma": '195967001' from "SNOMED"

context Patient

define "Asthma Diagnosis":
    [Condition: "Asthma"]

define "Has Asthma Diagnosis":
    exists("Asthma Diagnosis")