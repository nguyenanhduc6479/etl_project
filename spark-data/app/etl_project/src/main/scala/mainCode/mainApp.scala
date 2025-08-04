package mainCode

import commonCode._
import org.apache.spark.sql.{SparkSession, DataFrame}

object mainApp {
  def main(args: Array[String]): Unit = {
//    val sourcePath: String = "C:/Study_DE/etl_project/data/log_content/20220402.json"
//
//    val savePath: String = "C:/Study_DE/etl_project/data/log_result/20220402"

    if(args.length < 2)
      {
        println("sourcePath and savePath are invalid")

        sys.exit(1)
      }

    val sourcePath = args(0)

    val savePath = args(1)

    implicit val spark: SparkSession = configSparkSession.createSparkSession(
      appName = "project",
      extraConfigs = Map(
        "spark.sql.extensions" -> "io.delta.sql.DeltaSparkSessionExtension",
        "spark.sql.catalog.spark_catalog" -> "org.apache.spark.sql.delta.catalog.DeltaCatalog"
      )
    )

    try{
      val df = readFile.readData(
        sourcePath = sourcePath,
        fileType = "json")

      val selectDF = df.select("_source.*")

      saveTable.savetoDelta(
        df = selectDF,
        mode = "overwrite",
        savePath = savePath
      )

      println("Successes")
    }

    catch {
      case e: Exception =>
        println(s"Failed: ${e.getMessage}")
        e.printStackTrace()
        throw e
    }

    finally {
      configSparkSession.stopSparkSession()
    }
  }
}
