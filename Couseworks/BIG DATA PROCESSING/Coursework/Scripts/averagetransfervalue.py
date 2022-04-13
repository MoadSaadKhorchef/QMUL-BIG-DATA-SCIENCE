#http://andromeda.eecs.qmul.ac.uk:8088/cluster/app/application_1607539937312_8895

# TRANSACTIONS
# |block_number| from_address| to_address| value| gas| gas_price| block_timestamp|

# CONTRACTS
#| address| is_erc20| is_erc721| block_number| block_timestamp|

# BLOCKS
#| number| hash| miner| difficulty| size| gas_limit| gas_used| timestamp| transaction_count|


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
            float(fields[6])
            return True
				
        else:
            return False

    except:
        return False


blocks = sc.textFile("/data/ethereum/transactions")

good_blocks = blocks.filter( is_good_line )


features = good_blocks.map(lambda l: ( time.strftime("%Y %b", time.gmtime( float(l.split(',')[6]) )), (float(l.split(',')[3]), 1)))


totalsByTransferValue = features.reduceByKey(lambda x, y: (x[0]+y[0],x[1]+y[1]))

avgByTransferValue = totalsByTransferValue.mapValues(lambda x:(x[0]/x[1]))


#collectedData = results.coalesce(1)

#collectedData.saveAsSingleTextFile("numberoftransactionsOut")

#collectedData.saveAsTextFile("numberoftransactionsOut")


print(avgByTransferValue.collect())




