#http://andromeda.eecs.qmul.ac.uk:8088/cluster/app/application_1607539937312_9133

# TRANSACTIONS
# | block_number| from_address| to_address| value| gas| gas_price| block_timestamp|

# CONTRACTS
# | address| is_erc20| is_erc721| block_number| block_timestamp|

# BLOCKS
# | number| hash| miner| difficulty| size| gas_limit| gas_used| timestamp| transaction_count|


from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import re
import time
import pandas as pd
from datetime import datetime
from  pyspark.sql.functions import abs


def is_good_line(line):
    try:
	
        fields = line.split(',')
		
        if (len(fields)==6):
		
            fields=line.split(',')
            float(fields[2])
            return True			
				
        else:
            return False
		        		

    except:
        return False

spark = SparkSession.builder.getOrCreate()

sc = spark.sparkContext

blocks3 = sc.textFile("input/Prices.csv")
blocks2 = sc.textFile("input/Prices_After_June_2019.csv")


# Load training data
#dataset = spark.read.csv('/data/ethereum/ETH_USD_2015-08-09_2020-11-01-CoinDesk.csv',header= True)
#dataset.show()

good_blocks3 = blocks3.filter( is_good_line )
good_blocks2 = blocks2.filter( is_good_line )


features3 = good_blocks3.map(lambda l: ( ( float(l.split(',')[3]) ), ( float(l.split(',')[4]) ), ( float(l.split(',')[5]) ), ( float(l.split(',')[2]) ) ))
features2 = good_blocks2.map(lambda l: ( ( float(l.split(',')[3]) ), ( float(l.split(',')[4]) ), ( float(l.split(',')[5]) ), ( float(l.split(',')[2]) ) ))

#print(features3.collect())

Columns = ["Open (USD)" ,  "High (USD)" , "Low (USD)", "Closing Price (USD)"]

df = features3.toDF(Columns)
df2 = features2.toDF(Columns)

#df.printSchema()
#df.show(truncate=False)

feature_columns = df.columns[:-1] # here we omit the final column
feature_column2 = df2.columns[:-1] # here we omit the final column


assembler = VectorAssembler(inputCols=feature_columns,outputCol="features")


data_2 = assembler.transform(df)
data_3 = assembler.transform(df2)

#data_2.show()

train, test = data_2.randomSplit([0.7, 0.3])

algo = LinearRegression(featuresCol="features", labelCol="Closing Price (USD)")

model = algo.fit(train)

evaluation_summary = model.evaluate(test)
#evaluation_summary.meanAbsoluteError
#evaluation_summary.rootMeanSquaredError
#evaluation_summary.r2

predictions = model.transform(data_3)


x =((predictions['Closing Price (USD)']-predictions['prediction'])/predictions['Closing Price (USD)'])*100

predictions = predictions.withColumn('MAPE Accuracy',(100 - abs(x)))

dfOut = predictions.select("prediction" , "Closing Price (USD)","MAPE Accuracy", "features" )#.show()

dfOut.describe('MAPE Accuracy').show()

#print ( dfOut.select(sum("Closing Price (USD)")).collect()[0][0] - dfOut.select(sum("prediction")).collect()[0][0]  )

print("MAPE total accuracy")
print(100 - (((dfOut.select(sum("Closing Price (USD)")).collect()[0][0] - dfOut.select(sum("prediction")).collect()[0][0] )/dfOut.select(sum("Closing Price (USD)")).collect()[0][0])*100))


rdd = dfOut.rdd.map(list)

collectedData = rdd.coalesce(1)

collectedData.saveAsTextFile("machineOut")





