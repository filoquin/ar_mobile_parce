

<h1>Argentina mobile parce</h1>
<p>Obtain mobiles number from strings</p>
<p>Example</p>
<pre>
import csv
from ar_mobile_parce import ar_mobile_parce
parcer = ar_mobile_parce()
parcer.set_default_indicativo('299')

with open('sms/phones.csv', 'r') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in spamreader:
         print "%s,%s,%s"%(row[6],row[4], parcer.get_phones(row[4],row[6]))
</pre>