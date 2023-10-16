# Scripts

The scripts here generate SQL insert queries to augment our dataset with synthetic data initially before our application is loaded.

## How to run?

Make sure you have the synthetic data in a csv file. Each will correspond to a tuple with attributes in same order.

To get the SQL insert script of the corresponding table do the following -

Command: `python insert.py --table <TABLE_NAME> --file <FILE_PATH>`

The corresponding SQL file will be generated at path: `<WORKSPACE_FOLDER>/sql/<FILE_NAME>.sql`

### Note

Some table require CHAR(32) unique strings.
To create synthetic data for it in csv use the following code snippet

```
import uuid
unique_identifier = uuid.uuid4().hex

# Unique 32 character string on each run!
print(unique_identifier)
```
