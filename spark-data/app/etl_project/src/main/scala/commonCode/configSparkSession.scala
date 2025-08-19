package commonCode

import org.apache.spark.sql._

object configSparkSession {

  private var spark: Option[SparkSession] = None

  def createSparkSession(appName: String, extraConfigs: Map[String, String] = Map()): SparkSession = {
    if (spark.isEmpty) {
      val builder = SparkSession.builder()
        .appName(appName)
        .master("spark://spark-master:7077")


      extraConfigs.foreach {
        case (key, value) => builder.config(key, value)
      }

      spark = Some(builder.getOrCreate())
    }

    spark.get
  }

  def stopSparkSession(): Unit = {
    spark.foreach(_.stop())
    spark = None
  }
}
