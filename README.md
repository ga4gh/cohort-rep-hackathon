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

## 2. Generate Synthea population

### via JAR file

Requires Java on your local machine (tested with Java 11.0.6)

First, download the v3.0.0 Synthea JAR file via a command line download tool, e.g. `wget`:
```
wget https://github.com/synthetichealth/synthea/releases/download/v3.0.0/synthea-with-dependencies.jar
```

Next, run synthea using the config file in this repo to export bulk FHIR and CSV data:
```
java -jar synthea-with-dependencies.jar -c synthea/config/synthea.properties -p 1000
```

The output data will be in the `./output` directory
