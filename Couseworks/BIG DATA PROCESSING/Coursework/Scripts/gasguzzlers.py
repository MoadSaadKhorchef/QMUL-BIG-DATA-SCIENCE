#http://andromeda.eecs.qmul.ac.uk:8088/cluster/app/application_1607539937312_9141

# TRANSACTIONS
# | block_number| from_address| to_address| value| gas| gas_price| block_timestamp|


# CONTRACTS
# | address| is_erc20| is_erc721| block_number| block_timestamp|


# BLOCKS
# | number| hash| miner| difficulty| size| gas_limit| gas_used| timestamp| transaction_count|



import pyspark
import time
import re 


#WORD_REGEX = re.compile(r"\b\w+\b")


# This function checks good lines of transactions

sc = pyspark.SparkContext()

def is_good_line(line):

    try:

        fields = line.split(',')

        if(len(fields)==7):

            fields=line.split(',')
            float(fields[5])
            float(fields[6])
            return True


        elif(len(fields)==5):

           
            fields=line.split(',')
            float(fields[3]) 
            return True


        elif(len(fields)==9):

	        
            fields=line.split(',')
            float(fields[0])
            float(fields[3])
            float(fields[7])
            return True
        
        else:

            return False

    except:

        return False



# Load the dataset, filter the values

blocks = sc.textFile("/data/ethereum/transactions")

good_blocks = blocks.filter( is_good_line )


time_epoch_price = good_blocks.map(lambda l: ( time.strftime("%Y %b", time.gmtime( float(l.split(',')[6]) )), (float(l.split(',')[5]), 1 )  ))

yearly_agg_price = time_epoch_price.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))

yearly_average_price = yearly_agg_price.map(lambda x: (x[0], (x[1][0] / x[1][1])))


collectedData = yearly_average_price.coalesce(1)


collectedData.saveAsTextFile("avggaspriceOutTest")


#yearly_average_price.saveAsTextFile('avggasOutTest')


blocks2 = sc.textFile("/data/ethereum/contracts")

good_blocks2 = blocks2.filter( is_good_line )

features2 = good_blocks2.map(lambda l: (l.split(',')[3], 1))

table2 = features2



blocks3 = sc.textFile('/data/ethereum/blocks')

good_blocks3 = blocks3.filter( is_good_line )

features3 = good_blocks3.map(lambda l: (l.split(',')[0], (float(l.split(',')[3]), float(l.split(',')[6]), time.strftime("%Y %b", time.gmtime(float(l.split(',')[7]))))))

table3 = features3

 

joinedTable = table3.join(table2)

filteredTable = joinedTable.filter(lambda x: None not in x[1])


mappedTable = filteredTable.map(lambda x: ( x[1][0][2] ,((x[1][0][0], x[1][0][1]), x[1][1]) )  )


tempfinal = mappedTable.reduceByKey(lambda x, y : ( (x[0][0]+y[0][0] , x[0][1] + y[0][1] ), x[1] + y[1]) )

final = tempfinal.map(lambda x: (x[0], (float(x[1][0][0] / x[1][1]), x[1][0][1] / x[1][1]) ))


#print(filteredTable.collect())


collectedData1 = final.coalesce(1)


collectedData1.saveAsTextFile("contractscomplicatedOutTest")

