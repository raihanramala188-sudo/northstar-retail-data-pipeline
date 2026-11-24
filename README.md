\# Northstar – Retail Sales ETL Pipeline



\## Project Overview



This project implements a retail sales data engineering pipeline using PySpark, Spark SQL, and Delta Lake on Databricks.



The objective is to ingest raw sales data, clean and validate records, enrich transactions with product and store information, and generate aggregated business insights.



The pipeline follows the Medallion Architecture: Bronze, Silver, and Gold.



\## Architecture



```text

Source CSV Files

&#x20;      |

&#x20;      v

Bronze Layer

Raw sales ingestion

&#x20;      |

&#x20;      v

Silver Layer

Deduplication

Data type conversion

Invalid record filtering

&#x20;      |

&#x20;      v

Data Enrichment

Product and store joins

&#x20;      |

&#x20;      v

Gold Layer

Revenue aggregation

Store and regional analysis

&#x20;      |

&#x20;      v

Business Insights

```



\## Technologies Used



\- Python

\- PySpark

\- Apache Spark

\- Spark SQL

\- Delta Lake

\- Databricks

\- Jupyter Notebook



\## Project Structure



```text

day03-northstar/

├── data/

│   ├── sales.csv

│   ├── products.csv

│   └── stores.csv

├── docs/

│   └── TP\_Day\_03.pdf

├── notebooks/

│   └── Day\_03.ipynb

├── scripts/

│   └── Validate\_Day\_03.py

├── expected\_results.json

└── README.md

```



\## Pipeline Implementation



\### 1. Bronze Layer – Data Ingestion



\- Read raw sales data from CSV files.

\- Apply an explicit schema.

\- Store the original sales records as a Delta table.



\*\*Result:\*\* 112 records ingested.



\### 2. Silver Layer – Data Cleaning



\- Remove duplicate records.

\- Convert dates, quantities, and prices into appropriate data types.

\- Filter records containing invalid or missing values.

\- Store the cleaned dataset as a Delta table.



\*\*Result:\*\* 96 valid records retained.



\### 3. Data Enrichment



\- Join cleaned sales data with product information.

\- Join sales data with store information.

\- Check for unmatched product and store identifiers.



\*\*Result:\*\* 96 enriched records, with no unmatched product or store keys.



\### 4. Gold Layer – Business Aggregation



\- Calculate revenue for each transaction.

\- Aggregate transaction counts and quantities.

\- Calculate total revenue by store.

\- Generate regional revenue summaries.

\- Store the aggregated results in a Delta table.



\*\*Result:\*\* 4 store-level records generated.



\## Historical Saved Results



| Metric | Result |

|---|---:|

| Bronze records | 112 |

| Silver records | 96 |

| Enriched records | 96 |

| Gold store records | 4 |

| Total transactions | 96 |

| Total quantity | 289 |

| Total revenue | €2,680.90 |



\### Revenue by Store



| Store | Revenue |

|---|---:|

| Grenoble | €686.65 |

| Versailles | €680.00 |

| Paris Centre | €671.30 |

| Lyon Centre | €642.95 |



\## Data Validation



The project includes a validation script that checks:



\- Source CSV file integrity using SHA-256 hashes.

\- Delta table formats.

\- Table schemas.

\- Expected row counts.

\- Dataset content and aggregated business results.



The recovered notebook contains historical saved validation outputs showing successful checks.



\*\*Note:\*\* These are preserved outputs from the original practical, not a fresh execution performed for this GitHub publication.



\## Running the Project



1\. Set up a Databricks environment with PySpark and Delta Lake support.

2\. Create or identify a catalog and personal schema.

3\. Create a volume named `source\_files`.

4\. Upload the three CSV files, `expected\_results.json`, and the validation script into the `day03` directory of the volume.

5\. Update the catalog and schema configuration in the notebook.

6\. Run the notebook cells in order, from Bronze through Gold.

7\. Execute the final validation cell.



\## Learning Outcomes



Through this project, I practised:



\- Building ETL pipelines with PySpark.

\- Implementing Bronze, Silver, and Gold data layers.

\- Handling duplicate and invalid records.

\- Applying explicit schemas and data type conversions.

\- Joining multiple datasets.

\- Working with Delta tables.

\- Performing aggregations using Spark SQL.

\- Validating data quality and pipeline results.



\---



\*\*Project:\*\* Northstar Retail Sales ETL

\*\*Focus:\*\* Data Engineering | Big Data Processing | ETL | Databricks</
