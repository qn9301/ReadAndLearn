

Source Configuring Source Plugin
To customize the plugin, you can change its configuration parameters in your POM, as shown below:
<project>
  ...
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-source-plugin</artifactId>
        <version>2.2</version>
        <configuration>
          <outputDirectory>/absolute/path/to/the/output/directory</outputDirectory>
          <finalName>filename-of-generated-jar-file</finalName>
          <attach>false</attach>
        </configuration>
      </plugin>
    </plugins>
  </build>
  ...
</project>
The generated jar file will be named by the value of the finalName plus "-sources" if it is the main sources. Otherwise, it would be finalName plus "-test-sources" if it is the test sources. It will be generated in the specified outputDirectory. The attach parameter specifies whether the java sources will be attached to the artifact list of the project.
