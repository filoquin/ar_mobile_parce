

<h1>Argentina mobile parce</h1>
<p>Obtain mobiles number from strings</p>
<pre>
example 
parcer = ar_mobile_parce()
parcer.set_default_indicativo('299')

with open('SMSAPROC_1.csv', 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in spamreader:
         print  parcer.get_phones(row[4],row[6])
</pre>