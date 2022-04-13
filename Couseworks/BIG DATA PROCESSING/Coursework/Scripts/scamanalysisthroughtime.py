#http://andromeda.eecs.qmul.ac.uk:8088/cluster/app/application_1607539937312_9014

# TRANSACTIONS
# | block_number| from_address| to_address| value| gas| gas_price| block_timestamp|

# CONTRACTS
# | address| is_erc20| is_erc721| block_number| block_timestamp|

# BLOCKS
# | number| hash| miner| difficulty| size| gas_limit| gas_used| timestamp| transaction_count|


import pyspark
import re
import time


sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")


def is_good_line(line):
    try:
	
        fields = line.split(',')
		
        if(len(fields)==7):
		
            fields=line.split(',')
            float(fields[3])
            return True
				
        else:
            return False
		        		
    except:
        return False

		
blocks1 = sc.textFile("/data/ethereum/transactions")
blocks2 = sc.textFile("input/scams.csv")


good_blocks1 = blocks1.filter( is_good_line )


features1 = good_blocks1.map(lambda l: ( l.split(',')[2], (float(l.split(',')[3]), time.strftime("%Y %b", time.gmtime( float(l.split(',')[6]) ) ) )))

blocks2mapped = blocks2.map(lambda l:  ( l.split(',')[0], l.split(',')[2:] ))

blocks2FlatMapped = blocks2mapped.flatMapValues(lambda x: x)

tempfeatures2 = blocks2FlatMapped.map (lambda x: ( x[1] ,(x[0]) ))

features2 = tempfeatures2.distinct()


table1 = features1

table2 = features2

joinedTable = table2.leftOuterJoin(table1)


filteredTable = joinedTable.filter(lambda x: None not in x[1])

tempfinalTable = filteredTable.map (lambda x: (  (str(x[1][0]) , x[1][1][1]),  float(x[1][1][0])  ))


finalTable = tempfinalTable.reduceByKey(lambda x, y: ( x + y ))

#collectedData = finalTable.coalesce(1)

#collectedData.saveAsTextFile("scamsanalysisthroughtimeOut")

print(finalTable.collect())


