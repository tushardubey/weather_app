# 🌦 Weather App – Multi-Region Disaster Recovery on AWS

## 📌 Overview
This project demonstrates a **Flask-based Weather App** deployed on **AWS** with a focus on **High Availability** and **Disaster Recovery (DR)** across multiple regions.

The application fetches live weather data from OpenWeather API and stores results in **S3**. Using **Route 53 failover**, the app automatically redirects traffic to a **backup region** if the primary region goes down.

---

## 🚀 Architecture
- **Frontend & Backend**: Flask (Python) + HTML templates
- **Web Server**: Nginx + Gunicorn
- **Primary Region**: ap-south-1
- **Backup Region**: us-east-1
- **Storage**: S3 with Cross-Region Replication
- **Database**: RDS Multi-AZ
- **DNS Management**: Route 53 Failover
- **CI/CD**: Jenkins Pipeline
- **Load Balancing**: Application Load Balancer + Auto Scaling

---

## 🏆 Achievements
- ✅ Flask app deployed in multi-region AWS setup
- ✅ Automated failover with Route 53
- ✅ Cross-region S3 replication
- ✅ CI/CD pipeline using Jenkins
- ✅ High availability with ALB + Auto Scaling
- ✅ Disaster recovery tested successfully

---

## ⚙️ Setup Instructions
1. Clone repo:
   ```bash
   git clone https://github.com/tushardubey/weather_app.git
   cd weather_app

2. Create virtual environment & install requirements:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Configure environment variables:
   export API_KEY="your_openweather_api_key"

4. Run locally:
   flask run

5. Deployment handled via Jenkins CI/CD → EC2 → Nginx + Gunicorn.

---

## 🛠 Issues Faced & Fixes

1. Container-Nginx-Gunicorn Integration Issues

Challenge: Flask app containers were running, but Nginx wasn’t forwarding requests correctly, resulting in gateway errors.

Resolution: Reconfigured Nginx reverse proxy and Gunicorn socket binding inside Docker Compose, tested with health checks, and validated end-to-end communication.

2. Cross-Region S3 Replication Not Triggering

Challenge: Data wasn’t appearing in the backup region bucket despite replication rules being configured.

Resolution: Debugged IAM replication role, enabled bucket versioning, and applied correct replication policy. After fixing, replication worked as expected.

3. DNS Failover Delay

Challenge: Route 53 failover was not instant — traffic continued hitting the unhealthy primary region.

Resolution: Tuned DNS TTL values and configured Route 53 health checks with proper ALB endpoints to reduce propagation time during failover.

4. Jenkins Deployment Pipeline Failures

Challenge: Jenkins pipeline was failing while building and deploying Docker containers due to permission and workspace issues on EC2.

Resolution: Configured Jenkins with proper SSH keys, installed Docker on Jenkins agents, and used docker-compose in pipeline stages to standardize deployment.

5. Auto Scaling Health Check Mismatches

Challenge: Auto Scaling was terminating healthy containers because the ALB health check path wasn’t aligned with the Flask route.

Resolution: Adjusted ALB health check to /health endpoint and added a lightweight health-check route in the Flask app.

6. Application Downtime After EC2 Reboot

Challenge: After EC2 restarts, the app wasn’t auto-starting, causing service downtime.

Resolution: Configured systemd services with Restart=always for Docker Compose stack, ensuring containers auto-start on reboot.

## 🔮 Future Enhancements

Infrastructure as Code (Terraform)

CloudFront + WAF for global availability & security

Automated monitoring with Grafana, Prometheus
