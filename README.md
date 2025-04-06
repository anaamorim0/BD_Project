# BD_Project

# Part 1 — UML & Relational Data Modeling

The goal was to design the data model for a real-world scenario, including:

- A **UML class diagram** with at least 3 classes and several associations;
- A **relational schema** derived from the UML diagram;
- Consistent mapping of relationships, including 1:N and M:N cardinalities.

## Objectives

- Describe a real-world universe using real datasets;
- Design a UML class diagram with meaningful relationships and attributes;
- Translate the UML into a relational model, defining primary and foreign keys.

## Notes

- This part does not include implementation — it's focused on design.
- The model created here is used as the basis for Part 2 of the project.


# Part 2 — SQLite Database and Python Web App

This part consists of implementing the model proposed in Part 1 using **SQLite** and building a web-based application in **Python** to interact with it.

## Objectives

- Implement a database schema in SQLite using the relational model from Part 1.
- Populate it with real data from referenced sources.
- Develop a Python-based web application that includes:
  - Entry page (`/`)
  - Listing and detail views for each table
  - At least 3 additional custom endpoints:
    - One with a grouped aggregation
    - One with a join involving 3+ tables
    - One search-based endpoint


## How to Run

```bash
python app/app.py