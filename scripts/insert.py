import uuid
import csv
import pandas as pd
import numpy as np
import argparse


def createInsertQueries(table: str, file: str) -> None:
  """
    Args:
      table: Name of the relation
      file: path to csv file
  """

  with open(file, "r") as inFile:
    row = inFile.readline().split(',')
    attributes = ", ".join(row)[:-1]

    datareader = csv.reader(inFile)
    with open(f"./sql/{table}_insert.sql", 'w') as F:
      for row in datareader:
        for i in range(len(row)):
          if row[i] not in ["NULL", "TRUE", "FALSE"]:
            row[i] = f"'{row[i]}'"

        values = ", ".join(v for v in row)
        query = f"INSERT INTO {table} ({attributes}) VALUES ({values});"

        F.write(query)
        F.write("\n\n")

  F.close()

if __name__=="__main__":
  
  TABLE_CHOICES = [
    "Customers", 
    "Employees", 
    "Authors", 
    "Books", 
    "PaymentTransactions", 
    "Subscriptions", 
    "Sections",
    "Publishers", 
    "Published_by", 
    "Classified_by", 
    "Written_by", 
    "Subscribe", 
    "Accessed_by", 
    "Payments"
  ]

  # Parse args
  parser = argparse.ArgumentParser()  
  parser.add_argument("--table", type=str, choices=TABLE_CHOICES, required=True, help="Set table for which insert script is needed.")
  parser.add_argument("--file", type=str, required=True, help="Set the path to csv file from where data will be taken.")
  args = parser.parse_args()

  # Generate Insert Queries
  createInsertQueries(args.table, args.file)
