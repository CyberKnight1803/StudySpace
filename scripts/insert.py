import uuid
import argparse


def insertCustomers(file):
  pass

def insertEmployees(file):
  pass 

def insertAuthors(file):
  pass 

def insertBooks(file):
  pass 

def insertPaymentTransactions(file):
  pass 

def insertSubscriptions(file):
  pass 

def insertSections(file):
  pass 

def insertPublishers(file):
  pass 

def insertPublished_by(file):
  pass 

def insertClassified_by(file):
 pass 

def insertWritten_by(file):
  pass 

def insertSubscribe(file):
  pass 

def insertAccessed_by(file):
  pass 

def insertPayments(file):
  pass 

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

  RUN_MAPPER = {
    "Customers": insertCustomers, 
    "Employees": insertEmployees, 
    "Authors": insertAuthors, 
    "Books": insertBooks, 
    "PaymentTransactions": insertPaymentTransactions, 
    "Subscriptions": insertSubscriptions, 
    "Sections": insertSections,
    "Publishers": insertPublishers, 
    "Published_by": insertPublished_by, 
    "Classified_by": insertClassified_by, 
    "Written_by": insertWritten_by, 
    "Subscribe": insertSubscribe, 
    "Accessed_by": insertAccessed_by, 
    "Payments": insertPayments
  }

  # Parse args
  parser = argparse.ArgumentParser()  
  parser.add_argument("--table", type=str, choices=TABLE_CHOICES, required=True, help="Set table for which insert script is needed.")
  parser.add_argument("--file", type=str, required=True, help="Set the path to csv file from where data will be taken.")
  args = parser.parse_args()

  # Run corresponding method
  RUN_MAPPER[args.table](args.file)
