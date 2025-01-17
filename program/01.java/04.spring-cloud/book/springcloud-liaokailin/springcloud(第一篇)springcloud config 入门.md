

springcloud(第一篇)springcloud config 入门 - CSDN博客 http://blog.csdn.net/liaokailin/article/details/51307215

spring cloud config 入门

简介

Spring cloud config 分为两部分 server client 
config-server 配置服务端，服务管理配置信息
config-client 客户端，客户端调用server端暴露接口获取配置信息
config-server

创建config-server

首先创建config-server工程.

文件结构：

├── config-server.iml
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   │   └── com
    │   │       └── lkl
    │   │           └── springcloud
    │   │               └── config
    │   │                   └── server
    │   │                       └── Application.java
    │   └── resources
    │       ├── application.properties
    │       └── bootstrap.properties
    └── test
        └── java

pom.xml内容：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.2.3.RELEASE</version>
        <relativePath /> <!-- lookup parent from repository -->
    </parent>

    <groupId>com.lkl.springcloud</groupId>
    <artifactId>spring-cloud-config-server</artifactId>
    <version>1.0-SNAPSHOT</version>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-config</artifactId>
                <version>1.0.4.RELEASE</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-config</artifactId>
        </dependency>

        <!--表示为web工程-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!--暴露各种指标-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-config-server</artifactId>
        </dependency>

    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

创建启动类 
Application.java

```java
package com.lkl.springcloud.config.server;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.cloud.config.server.EnableConfigServer;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created by liaokailin on 16/4/28.
 */
@Configuration
@EnableAutoConfiguration
@RestController
@EnableConfigServer
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

其中 @EnableConfigServer为关键注解

在resources文件下创建application.properties

server.port=8888
配置工程监听端口8888，默认情况下client通过读取http://localhost:8888获取配置信息

创建bootstrap.properties

spring.cloud.config.server.git.uri: https://github.com/liaokailin/config-repo
该配置信息通过fork https://github.com/spring-cloud-samples/config-repo 得到 
通过spring.cloud.config.server.git.uri指定配置信息存储的git地址

运行config-server

spring boot工程很方便启动，运行Application.java即可

获取git上的资源信息遵循如下规则：

/{application}/{profile}[/{label}]
/{application}-{profile}.yml
/{label}/{application}-{profile}.yml
/{application}-{profile}.properties
/{label}/{application}-{profile}.properties

application:表示应用名称,在client中通过spring.config.name配置
profile:表示获取指定环境下配置，例如开发环境、测试环境、生产环境 默认值default，实际开发中可以是 dev、test、demo、production等
label: git标签，默认值master
如果application名称为foo，则可以采用如下方式访问：

http://localhost:8888/foo/default 
http://localhost:8888/foo/development

只要是按照上面的规则配置即可访问.

config-client

创建config-client

目录结构如下：

├── pom.xml
├── spring-cloud-config-client.iml
└── src
    ├── main
    │   ├── java
    │   │   └── com
    │   │       └── lkl
    │   │           └── springcloud
    │   │               └── config
    │   │                   └── client
    │   │                       └── Application.java
    │   └── resources
    │       └── bootstrap.yml
    └── test
        └── java

pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.lkl.springcloud</groupId>
    <artifactId>spring-cloud-config-client</artifactId>
    <version>1.0-SNAPSHOT</version>


    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.2.3.RELEASE</version>
        <relativePath /> <!-- lookup parent from repository -->
    </parent>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-starter-parent</artifactId>
                <version>1.0.1.RELEASE</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>


    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-config-client</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>http://repo.spring.io/milestone</url>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </repository>
    </repositories>
    <pluginRepositories>
        <pluginRepository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>http://repo.spring.io/milestone</url>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </pluginRepository>
    </pluginRepositories>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

创建启动类Application.java

```java
package com.lkl.springcloud.config.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created by liaokailin on 16/4/28.
 */
@SpringBootApplication
@RestController
public class Application {
    @Value("${name:World!}")
    String bar;

    @RequestMapping("/")
    String hello() {
        return "Hello " + bar + "!";
    }

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

创建bootstrap.properties文件，其内容如下：

spring.application.name: foo
spring.cloud.config.env:default
spring.cloud.config.label:master
spring.cloud.config.uri:http://localhost:8888

其中 spring.application.name 为应用名称，spring.cloud.config.uri 配置config-server暴露的获取配置接口,其默认值为http://localhost:8888 
第二三项配置在前面已经提到过，配置的都为默认值，因此bootstrap.properties只需要配置应用名即可.

运行config-client

访问 http://localhost 得到 `Hello liaokailin` 获取到git上的配置信息
访问 http://localhost/env 得到所有的配置信息，可以发现获取配置信息成功.
{
profiles: [ ],
configService:https://github.com/liaokailin/config-repo/foo.properties: {
name: "liaokailin",
foo: "devoxxfr"
},
configService:https://github.com/liaokailin/config-repo/application.yml: {
info.description: "Spring Cloud Samples--lkl",
info.url: "https://github.com/spring-cloud-samples",
eureka.client.serviceUrl.defaultZone: "http://localhost:8761/eureka/"
},
commandLineArgs: {
spring.output.ansi.enabled: "always"
},
servletContextInitParams: { },
...}
ok ~ it’s work ! more about is here 
转载请注明 
http://blog.csdn.net/liaokailin/article/details/51307215

欢迎关注，您的肯定是对我最大的支持