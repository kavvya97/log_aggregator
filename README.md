# log_aggregator


Service/Request flow: 
- Log sources
  - Different service, generate independent logs. These can include error logs, access logs, info logs and debug-level logs.
  Log format: <timestamp> <service_name> <severity> <log> 
  - Each source pushes logs into rabbitmq Exchange, producer that is responsible for sending the logs messges
- Rabbitmq Exchange
  - The Exchange is configured for Topic-based routing. Logs are published to RabbitMQ with a routing key that identifies the type or severity of the log. For example:
    - ServiceA.error  "some error log"
    - ServiceB.info  "some warning log"
  - distributes this log into multiple queues based on routing key
  - 2 main queues: LogQueue(for raw logs) and MonitoringQueue(Real-time analysis)
- Log collector service
  - consumer of LogQueue.
  - collects all raw log and stores them in MongoDb
- Monitoring service
  - consumer of MonitoringQueue
  - processes specific logs such as error and info and performs real-time processing
- LogSearch Service  
    - supports restAPI to search and filter logs based on params
      - severity(error, info, warning)
      - source(service A, B, C)
      - Time range
    - Query the logs stored in MongoDB or indexed files (utilizing elastic search)
- AlertService
  - Consumer of MonitoringQueue
  - Detect specific conditions in real-time logs(more than 10 errors in last minute)
- LogRetention Scheduler
  - background task/Cron Job which automatically filters logs which are very old(based on TTL value)



Features to be implemented