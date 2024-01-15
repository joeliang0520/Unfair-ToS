from io import StringIO
import os
csvString = """Spark,25000,50 Days,2000
Pandas,20000,35 Days,1000
Java,15000,,800
Python,15000,30 Days,500
PHP,18000,30 Days,800"""

# Convert String into StringIO
from io import StringIO
csvStringIO = StringIO(csvString)
df = pd.read_csv(csvStringIO, sep=",", header=None)