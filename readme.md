## Introduction
Script to convert IBM DB2 Load Files to SQL Format Files. This is helpful to bulk import data exported from a DB2 database.

## Usage
1. Run Script with IBM DB2 Load Into File as Parameter
2. Copy generated Create Table Statement and execute in SQL
3. Copy generated BULK INSERT Statement and execute in SQL
4. Adjust datatypes in SQL (all columns are loaded as varchar)
5. Edit Relationships
6. Be Happy