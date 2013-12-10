name := "homework-for-FPinScala"

version := "0.1"

scalaVersion := "2.10.3"

resolvers ++= Seq(
  "Sonatype Releases" at "http://oss.sonatype.org/content/repositories/releases"
)

libraryDependencies ++= Seq(
  "org.scalacheck" %% "scalacheck" % "1.11.0" % "test"
)
