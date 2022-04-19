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

### Pre-hackathon deployment steps
1. Deploy a FHIR server - TBD: Deploy locally or in the cloud
2. Generate Sythea population
3. Load sythetic FHIR population bundle into the FHIR server
4. Test simple query with CQL IDE

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
