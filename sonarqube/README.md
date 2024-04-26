1. 先提前安装好 pgsql 数据库，并创建好 sonarqube用户和对应的数据库。
2. 切记文件夹的权限，绝对不能有 root 用户的,为了统一，最好使用 sonarqube，所有权限必须都为它。
3. 一般可以观察 es.log 日志或者 web.log 日志，这两个日志中容易出问题
4. 适当增大 es  jvm 启动参数，默认 512 太小
5. sonar-scanner 扫描示例：
sonar-scanner   -Dsonar.projectKey=test-butler   -Dsonar.sources=.   -Dsonar.host.url=http://10.33.12.209:9000   -Dsonar.login=6d2e82fd913e1b2abe1525ec0cfc51504236cbbe -Dsonar.java.binaries=/mnt/butler-service/butler-register/target/classes

6. sonar-scanner 有jdk 版本的限制，具体请参阅官网 sonar-scanner 章节