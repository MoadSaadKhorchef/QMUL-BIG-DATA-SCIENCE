#http://andromeda.eecs.qmul.ac.uk:8088/cluster/app/application_1607539937312_8954

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

		
		if(len(fields)==7):
		
			fields=line.split(',')
            float(fields[3])
			return True

        elif(len(fields)==5):
		
            fields=line.split(',')
			return True
				
        else:
            return False
		        		

    except:
        return False


blocks1 = sc.textFile("/data/ethereum/transactions")

blocks2 = sc.textFile("/data/ethereum/contracts")


good_blocks1 = blocks1.filter( is_good_line )

good_blocks2 = blocks2.filter( is_good_line )


features1 = good_blocks1.map(lambda l: (l.split(',')[2], float(l.split(',')[3]) ))

features2 = good_blocks2.map(lambda l: (l.split(',')[0] , 1 ))


table1 = features1.reduceByKey(lambda x, y: ( x + y ))

table2 = features2


joinedTable = table2.leftOuterJoin(table1)

filteredTable = joinedTable.filter(lambda x: None not in x[1])

finalTable = filteredTable.map (lambda x: ( x[0] , x[1][1] ))


top10 = finalTable.takeOrdered( 10, key=lambda x: -x[1] )


rdd = sc.parallelize(top10)

collectedData = rdd.coalesce(1)

collectedData.saveAsTextFile("toptenpopularservicesOut")


#for record in top10:
#    print("{}: {}".format(record[0],record[1]))
	
	
	
	
	
	
	
