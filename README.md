# GCF Knowledge Graph
Knowledge Graph representation of United Nations Global Climate Fund project/programme data

## Methodology

The GCF Knowledge Graph uses Python to transcribe and visualize publicly available GCF data from the GCF Open Data Library into a knowledge graph, powered by a Neo4j graph database.
My methodology in doing so was as follows:

1. Download publicly available data exports from the GCF Open Data Library
2. Reverse-engineer required data dictionaries mostly using the downloaded datasets, but also sometimes referring to external sources, such as the ISO standard
3. Design a tabular database schema to host the data dictionaries and data tables
4. Implement the tabular database schema into a SQLite .DB database file using the sqlalchemy Python library
5. Conduct data cleaning, standardization, and processing using Python
6. Populate the tabular database file using Python
7. Design a graph data model for the knowledge graph
8. Populate the graph database using the graph data model using the neo4j Python library

## Data sources

The data sources used to populate the tabular and graph databases were:
* Publicly available data sources from the GCF Open Data Library, all downloaded on 2025-01-12
   * Funded activities ([link](https://data.greenclimate.fund/public/data/projects))
   * Countries ([link](https://data.greenclimate.fund/public/data/countries))
   * Entities ([link](https://data.greenclimate.fund/public/data/entities))
   * Readiness ([link](https://data.greenclimate.fund/public/data/readiness))
* Publicly available ISO 3166 country codes ([link](https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv))
* GCF’s boardroom web page for the range of board meeting numbers ([link](https://www.greenclimate.fund/boardroom/meetings)) 

## Tabular DB schema

The schema for the SQLite tabular database was designed as follows:

![GCF_schema](https://github.com/user-attachments/assets/0181d080-e724-4d83-8da5-7ba61bfbef10)

Points to note:

* The data dictionaries were reverse-engineered from the GCF data export files, with the exception of `country_dict`
* I took some liberties with the table and column names, mainly to adhere to RDBMS naming convention best practices
* Columns with multiple values in a single cell (ex: `Countries` column from the Funded Activities export file) were dropped from the original tables. Then, join tables with one value per cell were reverse-engineered using Python (ex: `table project_country`).
* Any calculation values (ex: number of readiness projects per country in the Country export file) were dropped to keep only raw data in the files
* Row 49 of the `Entity` export file seemed to contain a data inconsistency where the single Entity had multiple size values and was manually reconciled (details below)

### Manual data inconsistency reconciliation

Row 49 of the entity export seemed to contain a data inconsistency, where it is the only record within the entity export file that contains multiple values in the `Size` column:

| field        | value                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------ |
| Entity       | DOE_ATG                                                                                          |
| Name         | Department of Environment, Ministry of Health and Environment, Government of Antigua and Barbuda |
| Country      | Antigua and Barbuda                                                                              |
| DAE          | TRUE                                                                                             |
| Type         | National                                                                                         |
| Stage        | Effectiveness                                                                                    |
| BM           | B.18                                                                                             |
| Size         | Medium, Small                                                                                    |
| Sector       | Public                                                                                           |
| \# Approved  | 2                                                                                                |
| FA Financing | 52706595                                                                                         |

Since it is unreasonable to assume that a single entity will have multiple sizes, it is more reasonable to assume that the `Size` column refers to the sizes of the projects carried out by the entity. However, when referring to the project export file, we see that the `DOE_ATG` entity has 2 projects in rows 53 and 120, both with the size `Small`, which is inconsistent with the values of the `Size` column in row 49 of the entity export:

![image](https://github.com/user-attachments/assets/441180e0-e315-46e2-ad0a-b4b679f57391)

To reconcile the data inconsistency, I have manually removed the value `Medium` from the `Size` column of row 49, so that the `DOE_ATG` entity only has the `Small` value in the column `Size`.

## Graph data model

I created a graph data model to represent the GCF domain ontology to the best of my understanding as follows:

![GCF graph data model](https://github.com/user-attachments/assets/79a365cf-d20e-4a39-ad15-621f3e0d8cdf)

Points to note:

* The relationship labels may not be adequate to describe the relationships between the concepts (ex: a Readiness programme involves a Country)
* Given the efficient relationship traversals of graph databases, many metadata points were converted into nodes instead of node properties (ex: size of a project)
* There are more concepts and relationships that can be modeled out, provided access to a more comprehensive data taxonomy and domain knowledge

## Analysis

The biggest advantages of a knowledge graph representation of data over a tabular representation of the same data are:

1. The data is easy to understand, because:
   * A graph representation more closely resembles our mental models compared to rows and columns
   * A graph is visual in nature
2. Knowledge graphs excels at finding hidden connections between concepts
3. An intuitive GQL (Graph Query Language), Cypher, can be utilized to query the graph database 

For example, we can query all unique nodes and relationships that are connected to the Benin country node with the following Cypher query:

```cypher
MATCH (r:Region)<-[:IS_IN]-(ben:Country {iso3: "BEN"})<-[*]-(n)
RETURN DISTINCT r, ben, n
```

Running the Cypher query on the graph, we can extract the following subgraph that shows the core concepts related to the Benin Country node:

![image](https://github.com/user-attachments/assets/e0843928-a85a-4886-ba48-3ade58b3ab20)

From this single subgraph, we can draw many insights, but an insight about GCF’s involvement with Benin that is not immediately obvious when working with tables is:

_There have been 5 board meetings (B.10, B.12, B.14, B.17, and B.22) that have covered Entities that fund projects involved with Benin._

Another interesting application of the knowledge graph is using graph algorithms to find how two seemingly-unrelated concepts relate to each other. For example, if we want to see how Benin and Japan are related to each other, we can use the following Cypher query:

```cypher
MATCH p = shortestPath((ben:Country {iso3: "BEN"})-[*..10]-(jpn:Country {iso3: "JPN"}))
RETURN p
```

This returns the following graph:

![image](https://github.com/user-attachments/assets/69506f8b-451e-480a-b50d-a2ef02c337f7)

From the graph, we can see that the entity MUFG Bank, Ltd is in Japan, and the entity funds Project GAIA, which in turn, involves Benin.

Zooming out from Benin, we can analyze larger subgraphs involving multiple concepts spanning countries, regions, projects, and programmes, such as this Cypher query that explores any concepts that are related to Least Developed Countries (LDC) in some way:

```cypher
MATCH (c:Country)<-[]-(n)
WHERE c.isLdc = True
RETURN c, n 
```

![image](https://github.com/user-attachments/assets/74883afd-54ad-4744-ad41-c282944aa999)

## Conclusion

The next steps for the GCF Knowledge Graph would be to:

1. Obtain a comprehensive data catalog and master taxonomy that covers all GCF concepts
2. Meet with domain experts and design a comprehensive domain ontology, ideally in an OWL format using a dedicated ontology editor
3. Use the domain ontology and master taxonomy to fully flesh out all possible concepts of the knowledge graph

Once the graph is complete, it could then be used as an alternative dashboard with which GCF can explore its portfolio impacts that can be shared internally or externally. Having such a knowledge graph will enable enhanced monitoring, evaluation and learning of GCF’s portfolio, allowing the organization to further effectively channel investments and help build the capacity of developing countries to take climate action.
