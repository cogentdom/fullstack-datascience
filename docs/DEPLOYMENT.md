# Deployment Guide

Comprehensive deployment instructions for the Financial Time Series Analytics Platform.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Local Deployment](#docker-local-deployment)
- [AWS EC2 Deployment](#aws-ec2-deployment)
- [Custom Domain Setup](#custom-domain-setup)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 2 GB
- Storage: 5 GB
- Python: 3.8 or higher
- Docker: 20.10 or higher (if using Docker)

**Recommended:**
- CPU: 4 cores
- RAM: 4 GB
- Storage: 10 GB
- Python: 3.9+
- Docker: Latest stable version

### Required Software

```bash
# Check versions
python --version  # Should be 3.8+
docker --version  # Should be 20.10+
docker-compose --version  # Should be 1.29+
```

## 🏠 Local Development

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/architecture-fullstack.git
cd architecture-fullstack
```

### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Streamlit

The `.streamlit/config.toml` file is already configured with a dark theme. To customize:

```toml
[theme]
primaryColor="#03fca5"
backgroundColor="#242b29"
secondaryBackgroundColor="#4d4d4d"
textColor="#e8e8e8"
font="sans serif"
```

### Step 5: Run the Application

```bash
streamlit run main.py
```

The dashboard will open at: `http://localhost:8501`

### Development Tips

1. **Auto-reload**: Streamlit automatically reloads when you save files
2. **Clear cache**: Use the menu (☰) → "Clear cache" to reset cached data
3. **Debug mode**: Add `?debug=true` to the URL for additional info

## 🐳 Docker Local Deployment

### Step 1: Build Docker Image

**Option A: Using Makefile**
```bash
make build_new
```

**Option B: Using Docker directly**
```bash
docker build -t dashboard:v0 .
```

### Step 2: Run with Docker Compose

```bash
docker-compose up -d
```

This starts the container:
- **streamlit** (dashboard-report): Port 8501

### Step 3: Access the Application

- Dashboard: http://localhost:8501

### Step 4: View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f dashboard-report
```

### Step 5: Stop the Application

```bash
docker-compose down

# Remove volumes as well
docker-compose down -v
```

### Docker Management Commands

```bash
# List running containers
docker ps

# Stop a specific container
docker stop dashboard-report

# Remove a container
docker rm dashboard-report

# Remove an image
docker rmi dashboard:v0

# Prune unused resources
docker system prune -a
```

## ☁️ AWS EC2 Deployment

### Step 1: Launch EC2 Instance

1. **Sign in to AWS Console**
2. **Navigate to EC2 Dashboard**
3. **Click "Launch Instance"**

**Instance Configuration:**
- **AMI**: Ubuntu 20.04 LTS (free tier eligible)
- **Instance Type**: t2.micro (1 vCPU, 1 GB RAM) for testing
  - For production: t3.small or larger
- **Storage**: 20 GB gp2 (general purpose SSD)

**Network Settings:**
- Enable Auto-assign Public IP
- Create new security group or use existing

**Security Group Rules:**

| Type  | Protocol | Port Range | Source    | Description          |
|-------|----------|------------|-----------|----------------------|
| SSH   | TCP      | 22         | Your IP   | SSH access           |
| Custom| TCP      | 8501       | 0.0.0.0/0 | Streamlit access     |

4. **Create/Select Key Pair** for SSH access
5. **Launch Instance**

### Step 2: Connect to Instance

```bash
# Replace with your key pair and instance IP
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@your-instance-public-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose
sudo apt install docker-compose -y

# Add user to docker group
sudo usermod -aG docker ubuntu

# Log out and back in for group changes to take effect
exit
```

Reconnect to the instance.

### Step 4: Deploy Application

```bash
# Clone repository
git clone https://github.com/yourusername/architecture-fullstack.git
cd architecture-fullstack

# Start application
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs
```

### Step 5: Verify Deployment

```bash
# Test locally on EC2
curl http://localhost:8501

# From your browser
# Visit: http://your-instance-public-ip:8501
```

### Step 6: Configure Auto-Start

Create systemd service for automatic startup:

```bash
sudo nano /etc/systemd/system/stock-dashboard.service
```

```ini
[Unit]
Description=Stock Analytics Dashboard
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/architecture-fullstack
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
User=ubuntu

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable stock-dashboard
sudo systemctl start stock-dashboard
sudo systemctl status stock-dashboard
```

## 🌐 Custom Domain Setup

### Option 1: Cloudflare DNS

#### Step 1: Add Domain to Cloudflare

1. Sign up at [Cloudflare](https://www.cloudflare.com/)
2. Add your domain
3. Update nameservers at your domain registrar

#### Step 2: Configure DNS Record

1. Go to DNS settings
2. Add an A record:
   - **Name**: @ (root domain) or subdomain
   - **IPv4 address**: Your EC2 public IP
   - **Proxy status**: Proxied (orange cloud)
   - **TTL**: Auto

Example:
```
A    @    12.34.56.78    Proxied
A    www  12.34.56.78    Proxied
```

#### Step 3: Configure SSL/TLS

1. Go to SSL/TLS settings
2. Set mode to "Flexible" (Cloudflare to browser only)

Note: Direct access to Streamlit on port 8501. For SSL termination, consider using Cloudflare's proxy service.

### Option 2: AWS Route 53

#### Step 1: Create Hosted Zone

1. Open Route 53 console
2. Click "Create hosted zone"
3. Enter domain name
4. Click "Create hosted zone"

#### Step 2: Create Record

1. Click "Create record"
2. Configure:
   - **Record name**: Leave blank or subdomain
   - **Record type**: A
   - **Value**: EC2 public IP
   - **TTL**: 300
3. Click "Create records"

#### Step 3: Update Nameservers

Update your domain registrar with Route 53 nameservers.

### Option 3: Elastic IP (Recommended)

To prevent IP changes when EC2 restarts:

```bash
# In AWS Console:
# 1. Go to EC2 > Elastic IPs
# 2. Allocate new address
# 3. Associate with your instance
```

Update DNS records with the Elastic IP.

## 🔒 SSL/HTTPS Configuration

### Using Cloudflare (Recommended)

The easiest way to add HTTPS is to use Cloudflare's proxy service:

1. Add your domain to Cloudflare
2. Set SSL/TLS mode to "Flexible"
3. Enable "Always Use HTTPS" in SSL/TLS settings
4. Cloudflare will handle SSL termination at their edge

### Alternative: Streamlit with SSL

For direct SSL configuration with Streamlit, update `.streamlit/config.toml`:

```toml
[server]
sslCertFile = "/path/to/cert.pem"
sslKeyFile = "/path/to/key.pem"
```

Note: This requires obtaining SSL certificates via Let's Encrypt or another certificate authority.

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8501

# Kill process
kill -9 <PID>
```

### Docker Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in
```

### Cannot Connect to EC2

1. Check Security Group rules
2. Verify instance is running
3. Check Docker containers: `docker ps`
4. View logs: `docker-compose logs`

### Streamlit Not Loading

```bash
# Check container logs
docker logs dashboard-report

# Restart container
docker-compose restart dashboard-report
```

### Data Not Updating

1. Clear Streamlit cache (menu → Clear cache)
2. Check Yahoo Finance API status
3. Verify internet connectivity

### Domain Not Resolving

1. Check DNS propagation: `dig yourdomain.com`
2. Wait for DNS propagation (up to 48 hours)
3. Clear browser DNS cache
4. Try different DNS server: `nslookup yourdomain.com 8.8.8.8`

## 📊 Monitoring

### View Logs

```bash
# Real-time logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs -f dashboard-report
```

### Check Resource Usage

```bash
# Container stats
docker stats

# System resources
htop  # or top
```

### Health Checks

Add to docker-compose.yaml:

```yaml
dashboard-report:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
```

## 🔄 Updates and Maintenance

### Update Application

```bash
cd architecture-fullstack
git pull origin main
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Update Dependencies

```bash
# Update requirements.txt
# Then rebuild
docker-compose build --no-cache dashboard-report
docker-compose up -d
```

### Backup

```bash
# Backup configuration
tar -czf backup-$(date +%Y%m%d).tar.gz \
  docker-compose.yaml \
  Dockerfile \
  .streamlit/
```

## 📞 Support

If you encounter issues:
1. Check logs: `docker-compose logs`
2. Review [Troubleshooting](#troubleshooting)
3. Open an issue on GitHub
4. Check documentation at [README.md](../README.md)

---

**Last Updated**: January 2026

