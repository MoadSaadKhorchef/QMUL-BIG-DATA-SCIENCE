#http://andromeda.eecs.qmul.ac.uk:8088/cluster/app/application_1607539937312_8978

# TRANSACTIONS
# |block_number| from_address| to_address| value| gas| gas_price| block_timestamp|

# CONTRACTS
#| address| is_erc20| is_erc721| block_number| block_timestamp|

# BLOCKS
#| number| hash| miner| difficulty| size| gas_limit| gas_used| timestamp| transaction_count|


import pyspark
import re

sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")


def is_good_line(line):
    try:
	
        fields = line.split(',')

		
		if(len(fields)==9):
		
			fields=line.split(',')
            float(fields[4])
			return True
				
        else:
            return False
		        		

    except:
        return False
		

blocks = sc.textFile("/data/ethereum/blocks")

good_blocks = blocks.filter( is_good_line )


features = good_blocks.map(lambda l: (l.split(',')[2] , float(l.split(',')[4]) ))

results = features.reduceByKey(lambda a,b: a+b)


top10 = results.takeOrdered(10, key=lambda x: -x[1])

rdd = sc.parallelize(top10)

#collectedData = rdd.coalesce(1)

#collectedData.saveAsTextFile("toptenmostactiveminersOut")

print(rdd.collect())

