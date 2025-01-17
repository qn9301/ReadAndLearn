http://camel.apache.org/logeip.html

Log
How can I log the processing of a Message?
Camel provides many ways to log the fact that you are processing a message. Here are just a few examples:
You can use the Log component which logs the Message content.
You can use the Tracer which trace logs message flow.
You can also use a Processor or Bean and log from Java code.
You can use the log DSL.
Using log DSL
In Camel 2.2 you can use the log DSL which allows you to use Simple language to construct a dynamic message which gets logged.
For example you can do
from("direct:start").log("Processing ${id}").to("bean:foo");
Which will construct a String message at runtime using the Simple language. The log message will by logged at INFO level using the route id as the log name. By default a route is named route-1, route-2 etc. But you can use the routeId("myCoolRoute") to set a route name of choice.
Difference between log in the DSL and [Log] component
The log DSL is much lighter and meant for logging human logs such as Starting to do ... etc. It can only log a message based on the Simple language. On the other hand Log component is a full fledged component which involves using endpoints and etc. The Log component is meant for logging the Message itself and you have many URI options to control what you would like to be logged.
Using Logger instance from the the Registry
As of Camel 2.12.4/2.13.1, if no logger name or logger instance is passed to log DSL, there is a Registry lookup performed to find single instance of org.slf4j.Logger. If such an instance is found, it is used instead of creating a new logger instance. If more instances are found, the behavior defaults to creating a new instance of logger.
Logging message body with streamed messages
If the message body is stream based, then logging the message body, may cause the message body to be empty afterwards. See this FAQ. For streamed messages you can use Stream caching to allow logging the message body and be able to read the message body afterwards again.
The log DSL have overloaded methods to set the logging level and/or name as well.
from("direct:start").log(LoggingLevel.DEBUG, "Processing ${id}").to("bean:foo");
and to set a logger name
from("direct:start").log(LoggingLevel.DEBUG, "com.mycompany.MyCoolRoute", "Processing ${id}").to("bean:foo");
Since Camel 2.12.4/2.13.1 the logger instance may be used as well:
from("direct:start").log(LoggingLeven.DEBUG, org.slf4j.LoggerFactory.getLogger("com.mycompany.mylogger"), "Processing ${id}").to("bean:foo");
For example you can use this to log the file name being processed if you consume files.
from("file://target/files").log(LoggingLevel.DEBUG, "Processing file ${file:name}").to("bean:foo");
Using log DSL from Spring
In Spring DSL it is also easy to use log DSL as shown below:
<route id="foo">
    <from uri="direct:foo"/>
    <log message="Got ${body}"/>
    <to uri="mock:foo"/>
</route>
The log tag has attributes to set the message, loggingLevel and logName. For example:
<route id="baz">
    <from uri="direct:baz"/>
    <log message="Me Got ${body}" loggingLevel="FATAL" logName="com.mycompany.MyCoolRoute"/>
    <to uri="mock:baz"/>
</route>
Since Camel 2.12.4/2.13.1 it is possible to reference logger instance. For example:
<bean id="myLogger" class="org.slf4j.LoggerFactory" factory-method="getLogger" xmlns="http://www.springframework.org/schema/beans">
    <constructor-arg value="com.mycompany.mylogger" />
</bean>
 
<route id="moo" xmlns="http://camel.apache.org/schema/spring">
    <from uri="direct:moo"/>
    <log message="Me Got ${body}" loggingLevel="INFO" loggerRef="myLogger"/>
    <to uri="mock:baz"/>
</route>
Configuring log name globally
Available as of Camel 2.17
By default the log name is the route id. If you want to use a different log name, you would need to configure the logName option. However if you have many logs and you want all of them to use the same log name, then you would need to set that logName option on all of them.
With Camel 2.17 onwards you can configure a global log name that is used instead of the route id, eg
CamelContext context = ...
context.getProperties().put(Exchange.LOG_EIP_NAME, "com.foo.myapp");
And in XML
<camelContext ...>
  <properties>
    <property key="CamelLogEipName" value="com.foo.myapp"/>
  </properties>
 
Using slf4j Marker
Available as of Camel 2.9
You can specify a marker name in the DSL
<route id="baz">
    <from uri="direct:baz"/>
    <log message="Me Got ${body}" loggingLevel="FATAL" logName="com.mycompany.MyCoolRoute" marker="myMarker"/>
    <to uri="mock:baz"/>
</route>
Using log DSL in OSGi
Improvement as of Camel 2.12.4/2.13.1
When using log DSL inside OSGi (e.g., in Karaf), the underlying logging mechanisms are provided by PAX logging. It searches for a bundle which invokes org.slf4j.LoggerFactory.getLogger() method and associates the bundle with the logger instance. Passing only logger name to log DSL results in associating camel-core bundle with the logger instance created.
In some scenarios it is required that the bundle associated with logger should be the bundle which contains route definition. This is possible using provided logger instance both for Java DSL and Spring DSL (see the examples above).
Using This Pattern
If you would like to use this EIP Pattern then please read the Getting Started, you may also find the Architecture useful particularly the description of Endpoint and URIs. Then you could try out some of the Examples first before trying this pattern out.