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
3. Load sythetic FHIR population bundle into the FHIR server via Postman
4. Test simple query with CQL IDE
5. ...

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

In this example, we will be generating two small, synthetic datasets for the hackathon demo:
1. A general/random patient dataset which may or may not have any asthma patients (~100 patients)
2. A dataset containing only asthma patients (~10 patients)

We will eventually upload both synthetic datasets to the HAPI FHIR server.

### Generate 100 patient random dataset

To generate the general/random patient dataset, run synthea using the config file in this repo to export bulk FHIR and CSV data:
```
java -jar synthea-with-dependencies.jar \
    -p 1000 \
    -c synthea/config/synthea.properties \
    --exporter.baseDirectory "./output/general/01"
```

The output data will be in the `./output/general/00` directory. You may rerun the data generation, in which case you can use separate directories for each attempt. (e.g. `./output/general/01`, `./output/general/02`, `./output/general/03`, etc.)

### Generate 10 patient asthma dataset

To generate the asthma patient dataset, run synthea using the config file in this repo to export bulk FHIR and CSV data:
```
java -jar synthea-with-dependencies.jar \
    -p 10 \
    -m Asthma \
    -c synthea/config/synthea.properties \
    --exporter.baseDirectory "./output/asthma/00"
```

The output data will be in the `./output/asthma/00` directory. You may rerun the data generation, in which case you can use separate directories for each attempt. (e.g. `./output/asthma/01`, `./output/asthma/02`, `./output/asthma/03`, etc.)

