import pandas as pd
import numpy as np

emails_csv = pd.read_csv("with_email.csv")
list1 = emails_csv["Last Name"].values.tolist()
list2 = emails_csv["First Name"].values.tolist()
print(' '.join([str(a) + b for a,b in zip(list1,list2)]))