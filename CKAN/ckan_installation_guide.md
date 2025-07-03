# ✅ CKAN Installation from Source (with Docker + Solr + PostgreSQL)

> This guide helps you install CKAN 2.11+ from source using Python 3.9, PostgreSQL, and Docker-based Solr.

---

## 🧱 1. System Dependencies

Install required packages:

```bash
sudo apt update && sudo apt install -y \
  python3.9 python3.9-venv python3.9-dev \
  git libpq-dev build-essential \
  libxml2-dev libxslt1-dev \
  libjpeg-dev zlib1g-dev libssl-dev libffi-dev \
  nginx redis-server
```

Create and activate a Python virtual environment:

```bash
mkdir -p /usr/lib/ckan/default
cd /usr/lib/ckan/default
python3.9 -m venv .
source bin/activate
```

---

## 🧩 2. Clone CKAN and Install Dependencies

```bash
mkdir -p src && cd src
git clone https://github.com/ckan/ckan.git
cd ckan
pip install --upgrade pip
pip install -e '.[dev,requirements]'
```

---

## ⚙️ 3. Generate and Edit CKAN Config File

```bash
ckan generate config /etc/ckan/default/ckan.ini
```

Set environment variable:

```bash
export CKAN_INI=/etc/ckan/default/ckan.ini
```

---

## 🐘 4. Setup PostgreSQL

Enter PostgreSQL:

```bash
sudo -u postgres psql
```

In psql:

```sql
CREATE USER ckan_default WITH PASSWORD 'yourpassword';
CREATE DATABASE ckan_default OWNER ckan_default;
\q
```

Edit your config file (`ckan.ini`):

```
sqlalchemy.url = postgresql://ckan_default:yourpassword@localhost/ckan_default
```

---

## 🔍 5. Setup Solr via Docker

Install Docker:

```bash
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

Run official CKAN Solr image:

```bash
docker run --name ckan-solr -p 8983:8983 -d ckan/ckan-solr:2.11-solr9
```

Create Solr core inside the container:

```bash
docker exec -it ckan-solr bash
solr create_core -c ckan
exit
```

Update config in `ckan.ini`:

```
solr_url = http://localhost:8983/solr/ckan
```

---

## 📁 6. Setup CKAN Data Directory and Initialize DB

Create and set permission:

```bash
sudo mkdir -p /var/lib/ckan
sudo chown -R $(whoami):$(whoami) /var/lib/ckan
```

Initialize the CKAN database:

```bash
ckan db init
```

---

## ▶️ 7. Run the CKAN Development Server

```bash
CKAN_INI=/etc/ckan/default/ckan.ini ckan run
```

Or explicitly use the full path:

```bash
CKAN_INI=/etc/ckan/default/ckan.ini /usr/lib/ckan/default/bin/ckan run
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 👤 8. Create an Admin User

```bash
ckan sysadmin add admin --password=yourpassword --email=you@example.com
```

---

## 🌐 9. (Optional) Install Frontend Dependencies

If you want to build custom themes or JS:

```bash
npm install
npm run build
```

---

## ✅ 10. Access and Management

- CKAN portal: http://localhost:5000  
- Solr dashboard: http://localhost:8983/solr  
- You can log in using the admin user and begin adding organizations, datasets, etc.

---

## 🧭 Optional Next Steps

- Set up NGINX + uWSGI/Gunicorn for production
- Enable plugins (e.g., `ckanext-pages`)
- Configure file storage (Filestore or S3)
- Add HTTPS, cron jobs, backup scripts, etc.
