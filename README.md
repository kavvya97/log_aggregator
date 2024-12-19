# Log Aggregator

<p align="center">
A distributed message-based Log aggregator developed with Python, RabbitMQ, Flask, and MongoDB.  
A Log Aggregator enables you to gather logs from disparate sources into a single system for search, analysis, and actionable insights.
</p>

## Architecture Overview

The log aggregator consists of the following key components:

1. **Log Sources**: 
   - Services generate logs in the format: `<timestamp> <service_name> <severity> <log_message>`.
   - Publishes logs to RabbitMQ with routing keys based on log severity and service name.

2. **RabbitMQ Exchange**:
   - Configured for topic-based routing.
   - Routes logs to appropriate queues: `LogQueue` (for storage) and `MonitoringQueue` (for real-time analysis).

3. **Log Collector Service**:
   - Consumes logs from `LogQueue` and stores them in MongoDB.

4. **Monitoring Service**:
   - Consumes logs from `MonitoringQueue` and performs real-time analysis.
   - Detects high error rates and triggers alerts.

5. **Log Search Service**:
   - Provides  RESTful APIs to query logs in mongodb based on parameters like severity and severity

6. **Log Retention Scheduler**:
   - Periodically removes logs older than 10 days from database to maintain storage efficiency.


## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/log_aggregator.git
   cd log_aggregator
