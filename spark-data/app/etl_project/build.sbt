ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.20"

val sparkVersion = "3.5.1"

lazy val root = (project in file("."))
  .settings(
    name := "etl_project",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-sql" % sparkVersion % "provided",
      "org.apache.spark" %% "spark-core" % sparkVersion % "provided",
      "org.postgresql" % "postgresql" % "42.6.0",
      "io.delta" %% "delta-spark" % "3.1.0"
    )
  )