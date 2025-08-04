package commonCode

import org.apache.spark.sql._

object readFile {

  def read_data(fileType: String, sourcePath: String, extraConfigs: Map[String, String] = Map())(implicit spark: SparkSession): DataFrame = {
    val reader = spark.read.format(fileType)
    extraConfigs.foreach { case (key, value) => reader.option(key, value) }

    reader.load(sourcePath)
  }
}