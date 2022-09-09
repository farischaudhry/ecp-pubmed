# imports
import eutils
import datetime as dt
import csv
import pandas as pd
import os


# eutils client
ec = eutils.Client()

# last week date
past_week_date = (dt.datetime.now() - dt.timedelta(days=7)).strftime("%Y/%m/%d")


# find all entries published or updated in the past week relating to ECP
esr = ec.esearch(db="pubmed", term=f'({past_week_date}:3000/12/31[Date - Publication] OR {past_week_date}:3000/12/31[Date - Modification]) AND "extracorporeal photopheresis"[Title/Abstract]')
paset = ec.efetch(db="pubmed", id=esr.ids)

# create text file with all outputs
with open('ecp_papers.txt', 'w') as txtfile:
    writer = csv.writer(txtfile)
    writer.writerow(["Title", "Lead Author", "PMID", "DOI"])
    for pa in paset:
        writer.writerow([pa.title, pa.authors[0], pa.pmid, pa.doi])
txtfile.close()

# tabulate text with pandas
df = pd.read_csv('ecp_papers.txt', on_bad_lines='skip')
with open('ecp_papers.txt', 'w') as txtfile:
    txtfile.write(df.to_string())
txtfile.close()

# open file
os.startfile('ecp_papers.txt')
