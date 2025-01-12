# GCF Knowledge Graph
Knowledge Graph representation of United Nations Global Climate Fund project/programme data

## Tabular DB schema

![GCF_schema](https://github.com/user-attachments/assets/1fd4e56f-af93-4fb2-a9c0-3a6e65b0e35d)

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

 Although the `Size` column seems to refer to the sizes of the projects carried out by the entity, referring to the project export, we see that the `DOE_ATG` entity has 2 projects in rows 53 and 120, both with the size `Small`:

![image](https://github.com/user-attachments/assets/441180e0-e315-46e2-ad0a-b4b679f57391)

To reconcile the data inconsistency, I have manually removed the value `Medium` from the `Size` column of row 49, so that the `DOE_ATG` entity only has the `Small` value in the column `Size`.
