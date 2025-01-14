# GCF Knowledge Graph
Knowledge Graph representation of United Nations Global Climate Fund project/programme data

## Tabular DB schema

![GCF_schema](https://github.com/user-attachments/assets/86831552-51c2-4cda-938d-a41314833a31)

## Graph data model

![GCF graph data model](https://github.com/user-attachments/assets/988f1654-cb8e-40d1-aa13-7b94d020df78)

## Manual data inconsistency reconciliation

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
