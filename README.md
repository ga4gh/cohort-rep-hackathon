# cohort-rep-hackathon
Project tracking for GA4GH Computable Cohort Representation Hackathons

### References

#### Industry Standards
- [FHIR](https://www.hl7.org/fhir/) - Standard to represent EHR data and transmit this information between system
- [CQL](https://cql.hl7.org/) - Query language for FHIR originally used to determine the quality of life of a patient
- [OMOP](https://www.ohdsi.org/data-standardization/the-common-data-model/) - Similar to HL7 FHIR used primariliy in research and observational study settings

#### Community Phenotypes
- [HDR UK AsthmaPhenotypes](https://phenotypes.healthdatagateway.org/phenotypes/?search=Asthma&tagids=&search_form=basic-form&page=1) - Example phenotypes from the HDR UK Phenotype library
- [PheKB Asthma Phenotype](https://phekb.org/phenotype/asthma) - Asthma phenotype from PheKB - slightly dated

#### Tools
- [hapi-fhir-jpaserver-starter](https://github.com/hapifhir/hapi-fhir-jpaserver-starter) - Non-production FHIR server
- [microsoft/fhir-server](https://github.com/microsoft/fhir-server) - production quality FHIRR server
- [Synthea](https://github.com/synthetichealth/synthea) - Synthetic population generator
- [CQL IDE](https://cql-runner.dataphoria.org/) - CQL IDE user interface uses [CQL Engine](https://github.com/DBCG/cql_engine)
- [CQL-to-ELM Translator](https://github.com/cqframework/clinical_quality_language/blob/master/Src/java/cql-to-elm/OVERVIEW.md)
- [CQL Testing Framework](https://github.com/AHRQ-CDS/CQL-Testing-Framework)
- [Phenoflow](https://kclhi.org/phenoflow/) - Python/Js generator from the HDR UK Phenotype Library

----

# Pre-hackathon deployment steps

## FHIR

1. Deploy a FHIR server - TBD: Deploy locally or in the cloud
2. Generate Sythea population
3. Load sythetic FHIR population bundle into the FHIR server via Postman
4. Test simple query with CQL IDE
<<<<<<< Updated upstream
5. ...
=======

## Data Connect

1. Deploy Data Connect Server from https://github.com/ianfore/data-connect-trino

The instructions to deploy the above fork of  data-connect-trino are identical with one exception, to those described in Try a Reference Implementation [here](https://ga4gh-discovery.github.io/data-connect/docs/getting-started/provision-data/),. The container should mount a volume at /models which contains json schema files for data tables. The following example shows how to run the container via docker, with the schemas files in a local folder called  /yourpath/data-connect-models.

```bash
docker run --rm --name dnastack-data-connect -p 8089:8089 -v /yourpath/data-connect-models:/models -e TRINO_DATASOURCE_URL=https://trino-public.prod.dnastack.com -e SPRING_DATASOURCE_URL=jdbc:postgresql://host.docker.internal:15432/dataconnecttrino -e SPRING_PROFILES_ACTIVE=no-auth dnastack/data-connect-trino
```

2. Generate dbGaP and Synthea datasets
3. Load datasets to Data Connect
4. Deploy table schema file for each table locally in  /yourpath/data-connect-models. The naming convention for each schema file should be <catalog>.<schema>.<table_name>.data_dict.json
5. Query via Data Connect API 

## FHIR Detailed Instructions

## 1. Deploy a FHIR server

### Deploy HAPI FHIR server locally

Using the HAPI FHIR server definition in [`docker-compose.yml`](./docker-compose.yml), we can spin up the server using:
```
docker-compose up -d
```

Wait a few minutes for the server setup process to complete. Once this is done, you should confirm the service is available by visiting the following URLs via web browser:
* http://localhost:8080/ - Landing page
* http://localhost:8080/fhir/swagger-ui/index.html - OpenAPI definition of the FHIR web API 

**Note:** This requires `docker` and `docker-compose` to be installed on your local machine.

### Cloud deployment

For the hackathon, the GA4GH tech team has spun up a web-accessible HAPI FHIR instance via Amazon Web Services (AWS). This service is available at https://cohort.ga4gh-demo.org/ . For example:
* https://cohort.ga4gh-demo.org/ - Landing page
* https://cohort.ga4gh-demo.org/fhir/swagger-ui/index.html - OpenAPI definition of the FHIR web API

The cloud-based instance has already been populated with a synthetic asthma dataset for the purpose of the hackathon. See the next sections for how the synthetic data was generated and uploaded.

## 2. Generate Synthea population

Requires Java on your local machine (tested with Java 11.0.6)

First, download the v3.0.0 Synthea JAR file via a command line download tool, e.g. `wget`:
```
wget https://github.com/synthetichealth/synthea/releases/download/v3.0.0/synthea-with-dependencies.jar
```

In this example, we will be generating a small, synthetic dataset containing asthma patients and patients without asthma. We will then perform a filter step so that only a mini dataset that is enriched for asthma is uploaded to the FHIR server.

### Generate 1000 patient random dataset

First, create the raw output directory that synthea will write to:
```
mkdir -p output/synthea/raw
```

Next, run synthea using the config file in this repo to generate the random patient dataset, exporting it as both bulk FHIR and CSV data:
```
java -jar synthea-with-dependencies.jar \
    -p 1000 \
    -c synthea/config/synthea.properties \
    --exporter.baseDirectory "./output/synthea/raw/"
```

The output data will be in the `./output/synthea/raw` directory.

### Filter random dataset for enriched asthma dataset

A custom python script [`filter.py`](./filter.py) has been included in the repo. This script produces a mini dataset of 100+ patients that are enriched for asthma incidences. The resulting mini dataset will contain all patients with asthma from the original synthetic dataset, plus 100 patients without asthma.

The enriched mini-dataset uploaded to the AWS instance has been included in the repository at [`output/synthea/filtered/fhir`](./output/synthea/filtered/fhir), so you do not need to run the filter step. However, the filter step can be run with:
```
python filter.py
```

assuming that Python 3 has been installed on your system.

## 3. Load synthetic population into the FHIR server

Now, we will load the asthma enriched dataset into the local FHIR server we started in step 1. There is a custom python script [`upload.py`](./upload.py) that will handle the upload of the relevant records. The upload script leverages the FHIR REST API documented at http://localhost:8080/fhir/swagger-ui/index.html. Specifcally, the script makes HTTP requests to the `PUT /fhir/{model}/{id}` REST endpoint for each model and record in the dataset.

The upload step can simply be run be executing:
```
python upload.py
```

### Explore data using FHIR REST API

Now that the data has been ingested, we can now explore it by making HTTP requests to the FHIR REST API. Using your preferred HTTP client tool (such as Postman), you can now browse instances of the FHIR models you uploaded, including:
* `Patient`
* `Condition`
* `Encounter`
* `Observation`
* `DiagnosticReport`
* `DocumentReference`
* `Immunization`
* `Procedure`
* `Practitioner`
* `PractitionerRole`
* `Organization`
* `Location`

The URL template for viewing these instances is:
```
GET http://{serverBaseUrl}/fhir/{model}/{id}
```

For example, to view a `Patient` with id `02dade42-9887-12c3-979e-5df8f35319f7`, you would make a request to
```
GET http://localhost:8080/fhir/Patient/02dade42-9887-12c3-979e-5df8f35319f7
```
for the local FHIR server, or

```
GET https://cohort.ga4gh-demo.org/fhir/Patient/02dade42-9887-12c3-979e-5df8f35319f7
```

for the web-accessible server

A full list of patient IDs is available [here](./PATIENT_IDS.md)

## 4. CQL Example: Check for Asthma Patients

This is a simple example on how to use CQL to identify whether a patient has a certain phenotype.

### 1. Define CQL based on a phenotype definition
Let's say we want to know if a patient was diagnosed with asthma as defined by the SNOMED CT code 195967001 (Asthma (disorder)). In CQL, that would look something like this:
```
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
```
On the first line we name our CQL library, a library in CQL is the high-level container in which the logic is stored. We then say that we use FHIR as our data model and specify the version (R4, 4.0.1). FHIRHelpers is another CQL library that is added as a dependency, this library enables the conversion between FHIR data types and CQL primatives, and enables the use of FHIRPath (like XPath, but for FHIR). Then, we define a code system (SNOMED CT in this case) and a code (the SNOMED asthma code as mentioned before). The next line 'context Patient' defines that all statements that follow this line have a FHIR Patient as their overall context. The statement "Asthma Diagnosis" returns any Condition resources that contain the specified SNOMED code for a given Patient. Lastly, "Has Asthma Diagnosis" returns either true or false, depending on if any Conditions with the specified code were found.

### 2. Package the CQL as a FHIR Library (optional)
This step is optional but allows for storing any CQL library embedded in a FHIR Library on a FHIR server, and evaluate the statements using FHIR's Clinical Reasoning module. Packaging the CQL can be done using the [CQF Tooling](https://github.com/cqframework/cqf-tooling).

The Library with the embedded 'AsthmaPhenotype' CQL is included in the `/cql` folder [here](https://github.com/ga4gh/cohort-rep-hackathon/blob/main/cql/Library-AsthmaPhenotype.json).

### 3. Evaluate the Library/CQL
This is where we actually run our CQL statements for a specific Patient to get the result (asthma/no asthma). To evaluate a FHIR Library with an embedded CQL quality measure (like this example), you need a FHIR server that supports FHIR's Clinical Reasoning module. Here we can use the [CQF Ruler](https://github.com/DBCG/cqf-ruler) which is a HAPI FHIR server with some additional plugins. It can be easily run from a Docker container and the instructions above can be used to load synthetic Synthea data onto the server.

Once the data and the Library are loaded onto the server you can run [$evaluate](http://build.fhir.org/ig/HL7/cqf-recommendations/OperationDefinition-cpg-library-evaluate.html)
```
GET http://localhost:8080/fhir/Library/AsthmaPhenotype/$evaluate?subject=Patient/54a0dc8e-5c3c-e294-6619-486afc4f9444
```
specifying Patient with ID `54a0dc8e-5c3c-e294-6619-486afc4f9444` as subject (an asthma patient according to our definition). 

The server will then return the output of the CQL evaluation as a Parameters resource. For this example, the last part of the [output](https://github.com/ga4gh/cohort-rep-hackathon/blob/main/cql/Response-%24evaluate-example-patient.json) should look like:
```
        {
            "name": "Has Asthma Diagnosis",
            "valueBoolean": true
        }
```
Which confirms that Patient `54a0dc8e-5c3c-e294-6619-486afc4f9444` is indeed an asthma patient (has a Condition resource with SNOMED CT code 195967001).

>>>>>>> Stashed changes
