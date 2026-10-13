# Databricks notebook source
# MAGIC %md
# MAGIC # Databricks vs Snowflake Funding History
# MAGIC
# MAGIC This demo notebook creates a small dataset with the funding history of **Databricks** and **Snowflake**.  
# MAGIC We will apply a simple transformation to calculate the **cumulative funding raised over time** for each company.

# COMMAND ----------


from pyspark.sql import Row

# Publicly available funding data (simplified, USD millions)
funding_data = [
    # Databricks funding rounds
    Row(company="Databricks", round="Seed",      year=2013, amount_million=13.9),
    Row(company="Databricks", round="Series A",  year=2014, amount_million=33.0),
    Row(company="Databricks", round="Series B",  year=2015, amount_million=60.0),
    Row(company="Databricks", round="Series C",  year=2016, amount_million=140.0),
    Row(company="Databricks", round="Series D",  year=2017, amount_million=140.0),
    Row(company="Databricks", round="Series E",  year=2019, amount_million=250.0),
    Row(company="Databricks", round="Series F",  year=2021, amount_million=1000.0),
    Row(company="Databricks", round="Series G",  year=2022, amount_million=1600.0),

    # Snowflake funding rounds
    Row(company="Snowflake", round="Series A",   year=2012, amount_million=5.0),
    Row(company="Snowflake", round="Series B",   year=2014, amount_million=26.0),
    Row(company="Snowflake", round="Series C",   year=2015, amount_million=80.0),
    Row(company="Snowflake", round="Series D",   year=2017, amount_million=100.0),
    Row(company="Snowflake", round="Series E",   year=2018, amount_million=263.0),
    Row(company="Snowflake", round="Series F",   year=2020, amount_million=479.0),
]

df = spark.createDataFrame(funding_data)

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Calculate Cumulative Funding
# MAGIC
# MAGIC Now we calculate the **cumulative funding raised** over time for each company.  
# MAGIC This will let us see how the total funding grew year by year.
# MAGIC

# COMMAND ----------

from pyspark.sql import Window
from pyspark.sql import functions as F

df_transformed = (
    df.orderBy("company", "year")
      .withColumn(
          "cumulative_million",
          F.sum("amount_million").over(
              Window.partitionBy("company").orderBy("year").rowsBetween(Window.unboundedPreceding, Window.currentRow)
          )
      )
)

display(df_transformed)