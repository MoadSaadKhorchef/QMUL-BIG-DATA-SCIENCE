#http://andromeda.eecs.qmul.ac.uk:8088/cluster/app/application_1607539937312_8833

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
		
        if len(fields)!=7:
            return False
		        
        float(fields[6])

        return True

    except:
        return False


blocks = sc.textFile("/data/ethereum/transactions")

good_blocks = blocks.filter( is_good_line )


time_epoch = good_blocks.map(lambda b: b.split(',')[6] )

year = time_epoch.map ( lambda t: (time.strftime("%Y %b", time.gmtime( float(t) )), 1 ) )


results = year.reduceByKey(lambda a,b: a+b)


#collectedData = results.coalesce(1)

#collectedData.saveAsSingleTextFile("numberoftransactionsOut")

#collectedData.saveAsTextFile("numberoftransactionsOut")


print(results.collect())




