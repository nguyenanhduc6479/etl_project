package commonCode

import org.apache.spark.sql._

object readFile {

  def readData(fileType: String, sourcePath: String, extraConfigs: Map[String, String] = Map())(implicit spark: SparkSession): DataFrame = {

    if (sourcePath.isEmpty) {
      sys.exit(1)
    }
    else {
      val reader = spark.read.format(fileType)
      extraConfigs.foreach { case (key, value) => reader.option(key, value) }

      reader.load(sourcePath)
    }
  }
}