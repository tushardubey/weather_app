# Technical Documentation & Runbook

## What I Achieved
- Dockerized Flask weather app behind Nginx + Gunicorn
- Multi-Region DR: Route 53 failover (ap-south-1 -> us-east-1)
- S3 Cross-Region Replication for data durability
- Jenkins CI/CD deploying to both regions via SSH + docker compose
- Validated DR by stopping primary; backup continued serving

## Step-by-Step (How It Was Done)

### 1) App & Docker
- Built Flask app with OpenWeather API.
- `gunicorn -w 3 -b 0.0.0.0:8000 app:app`
- Nginx reverse proxy listens on :80, proxies to :8000.
- Docker Compose defines `app` and `nginx` services with restart policies.

### 2) Primary Region (ap-south-1)
- EC2 (Ubuntu) with Docker & docker-compose.
- Security Groups: 22 (SSH), 80 (HTTP), 443 (if TLS), health checks.
- Optional ALB in front of EC2; target group health for R53 health check.
- S3 primary bucket for data; versioning enabled.

### 3) Backup Region (us-east-1)
- EC2 (Ubuntu) with Docker & docker-compose.
- S3 backup bucket with versioning.
- CRR rule set up from primary to backup bucket.

### 4) Jenkins CI/CD (weather-cicd)
- Checkout from `tushardubey/weather_app` (fixed Git installation issue).
- Build + Test stage.
- Deploy via `sshagent` -> run `docker compose up -d --build` on both EC2s.
- API keys via Jenkins credentials or environment variables.

### 5) DNS Failover (Route 53)
- Primary record (ALB/EC2) with health check to `/` endpoint.
- Secondary record points to backup EC2.
- Simulated outage by stopping primary -> observed failover.

### 6) Observability & Logs
- `docker logs weather_app`
- Nginx access/error logs
- CloudWatch metrics/alarms (optional but recommended).

## Issues Faced & Fixes

- **Nginx 502/504**: Upstream mis-bind. Ensured app listens on 0.0.0.0:8000 and Nginx proxy to that address. Increased proxy timeouts.
- **S3 AccessDenied**: Missing permissions. Attached replication role, verified bucket policies, enabled versioning before CRR.
- **Jenkins Git SCM**: "Selected Git installation does not exist" -> Installed Git on Jenkins, configured Global Tool.
- **SSH Blocked**: Security group changes removed port 22 -> Re-added inbound rule for SSH.
- **Service on Reboot**: Use Docker restart=always; previously also tried `systemd` for Gunicorn on host.

## DR Drill Checklist
1. Confirm health checks GREEN in Route 53.
2. Stop primary EC2 or break health check.
3. Verify DNS resolves to backup and app is reachable.
4. Validate S3 replication continues.
5. Restore primary; watch traffic revert on GREEN.

## Future Enhancements
- IaC: Terraform modules for VPC, EC2, Route53, S3, CRR.
- Container Registry: Amazon ECR + image digest pinning.
- Orchestration: ECS/EKS with multi-AZ/multi-region.
- TLS: ACM certs on ALB (or Nginx) + HTTP->HTTPS redirect.
- CDN + WAF: CloudFront in front of Route 53/ALB with WAF rules.
- Monitoring: CloudWatch alarms, Grafana dashboards, synthetic canaries.
