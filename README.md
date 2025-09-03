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

1. 502/504 Gateway errors → fixed Gunicorn/Nginx config

2. S3 access denied → fixed IAM & bucket policy

3. Jenkins Git error → installed Git on server

4. SSH failures → corrected Security Group inbound rules

## 🔮 Future Enhancements

Infrastructure as Code (Terraform)

CloudFront + WAF for global availability & security

Automated monitoring with Grafana, Prometheus
