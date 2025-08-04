package commonCode

import org.apache.spark.sql._

object saveTable {

    def savetoDelta(df: DataFrame, mode: String, savePath: String): Unit = {
    df.write
      .format("delta")
      .mode(mode)
      .save(savePath)
  }
}