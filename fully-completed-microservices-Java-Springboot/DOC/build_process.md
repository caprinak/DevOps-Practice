# Microservices Build and Debugging Process

This document provides a detailed step-by-step guide on how we built, debugged, and ran the microservices project.

## 1. Building Steps

### Step 1: Base Build
We started by building all services to ensure dependencies were resolved.
```powershell
# From the root directory
cd services
# Build all services (skipping tests for speed)
mvn clean install -DskipTests
```

### Step 2: Infrastructure Setup
We used Docker Compose to spin up supporting services.
```powershell
docker-compose up -d
```

### Step 2.1: Initialize Databases
**CRITICAL**: If this is a fresh install or you wiped volumes, you must create the databases manually:
```powershell
docker exec -i ms_pg_sql psql -U alibou -d postgres -c "CREATE DATABASE customer; CREATE DATABASE product; CREATE DATABASE \"order\"; CREATE DATABASE payment;"
```

### Step 3: Service Startup Sequence
Microservices must be started in a specific order:
1.  **Config Server (Port 8888)**: The heart of the system.
2.  **Discovery Service (Port 8761)**: Eureka dashboard.
3.  **Application Services**: Customer, Product, Order, Payment (8060), Notification.
4.  **Gateway Service (Port 8222)**: The entry point.

---

## 2. Issues Encountered & Debugging Steps

### Issue 1: PostgreSQL Port Conflict
**Problem**: The `postgresql` container failed to start (or was inaccessible) because port `5432` was already taken by a native PostgreSQL service on the host.
**Debugging**: Used `netstat -ano | findstr :5432` to find the blocking PID.
**Fix**:
1.  Asked the user to stop the native service OR
2.  Temporarily mapped the container port to `5433` in `docker-compose.yml`.
3.  Updated service configurations (`product-service.yml`, etc.) in the Config Server to use `jdbc:postgresql://localhost:5433/`.
4.  *Final Resolution*: User stopped the native service; we reverted back to `5432`.

### Issue 2: Missing "Order" Database
**Problem**: The `order-service` failed to start because the `order` database did not exist in PostgreSQL.
**Debugging**: Checked `ms_pg_sql` logs; confirmed database connection failed.
**Fix**:
1.  Created a SQL script `create_order_db.sql`.
2.  Executed it inside the container:
```powershell
docker cp create_order_db.sql ms_pg_sql:/create_order_db.sql
docker exec -it ms_pg_sql psql -U alibou -f /create_order_db.sql
```

### Issue 3: Authentication Failure (FATAL: password authentication failed)
**Problem**: Services could not connect to PostgreSQL despite correct credentials (`alibou`/`alibou`).
**Debugging**: PostgreSQL's default `pg_hba.conf` was too restrictive for Docker bridge networking.
**Fix**:
1.  Created a custom `pg_hba.conf` with `trust` for local connections.
2.  Mounted it into the container via `docker-compose.yml`.
3.  Restarted PostgreSQL.

### Issue 4: Kafka Connectivity & Crashing
**Problem**: `order-service` and `payment-service` timed out connecting to Kafka (`localhost:9092`). `ms_kafka` container kept exiting.
**Debugging**: Checked container logs with `docker logs ms_kafka`. Found "KAFKA_PROCESS_ROLES is not set" (KRaft vs Zookeeper conflict in newer images).
**Fix**:
1.  Pinned Kafka image to `confluentinc/cp-kafka:6.2.1` to ensure stable Zookeeper compatibility.
2.  Simplified listeners in `docker-compose.yml` to use `PLAINTEXT://localhost:9092`.
3.  Forced a recreate: `docker-compose up -d --force-recreate kafka`.

### Issue 5: Port Conflicts (8090, 8040, 8222)
**Problem**: `customer-service` and others failed with "Port already in use".
**Debugging**: Identified rogue processes using `netstat -ano | findstr :<port>`.
**Fix**:
1.  Killed blocking processes: `taskkill /F /PID <PID>`.
2.  Alternatively, ran services on different ports using Maven arguments:
```powershell
mvn spring-boot:run "-Dspring-boot.run.arguments=--server.port=8091"
```

### Issue 6: Discovery Service Config Server Import
**Problem**: The `discovery-service` failed to start because it couldn't locate configurations.
**Debugging**: Logs showed a failure to bootstrap because it wasn't fetching from the Config Server correctly.
**Fix**: Added/corrected the `spring.config.import` property in `discovery-service`'s local `application.yml` to point to `http://localhost:8888`.

### Issue 7: Payment Service Port Misalignment
**Problem**: We initially expected `payment-service` to be on port `8080`, but it wouldn't respond.
**Debugging**: Checked `payment-service.yml` in the Config Server.
**Fix**: Discovered the service is configured to run on port `8060`. Updated all documentation and client references accordingly.

### Issue 8: Database Authentication Failure & Missing Databases
**Problem**: Services failed with `FATAL: password authentication failed` even with correct credentials.
**Debugging**: Realized the PostgreSQL container was missing the specific databases (`order`, `customer`, etc.), causing connection rejections that masqueraded as auth failures.
**Fix**:
1.  Wiped old volumes: `docker compose down -v`.
2.  Recreated infra: `docker compose up -d`.
3.  Manually created DBs using `docker exec -U postgres`.

---

## 3. CLI Commands Summary

### Build Commands
```powershell
mvn clean install -DskipTests
```

### Run Commands (Individual Services)
```powershell
# In service directory
mvn spring-boot:run
# Or with port override
mvn spring-boot:run "-Dspring-boot.run.arguments=--server.port=8091"
```

### Debug & Infrastructure Commands
```powershell
# View running containers
docker ps
# View all containers (including exited)
docker ps -a
# View container logs
docker logs <container_name> --tail 50
# Find port blockers
netstat -ano | findstr :8090
# Kill a process
taskkill /F /PID 12345
# Restart specific infra
docker-compose up -d --force-recreate kafka
```

### Verification
- **Eureka UI**: [http://localhost:8761](http://localhost:8761)
- **Eureka Registry API**: `curl -H "Accept: application/json" http://localhost:8761/eureka/apps`
- **Config Server Check**: [http://localhost:8888/product-service/default](http://localhost:8888/product-service/default)
- **Zipkin**: [http://localhost:9411](http://localhost:9411)
- **MailDev**: [http://localhost:1080](http://localhost:1080)
