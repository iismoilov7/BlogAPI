## Setup Instructions for BlogAPI Server

1. **Clone repository**  
   Run the following command to download project:  
   ```bash
   git clone https://github.com/iismoilov7/BlogAPI.git
   cd BlogAPI
   ```

2. **Install Required Packages**  
   Run the following command to install the necessary dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the Database**  
   Use Docker Compose to set up the database:  
   ```bash
   sudo docker-compose up
   ```

4. **Generate secret and public keys for JWT**
   Use library openssl
   ```bash
   mkdir ./certs
   openssl genrsa -out certs/jwt-private.pem 2048
   openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
   ```
   ```Do not forget to remove -----BEGIN KEY----- and -----END KEY----- lines from files```

5. **Set up database**
   Using alembic
   ```bash
   alembic upgrade head
   ```

6. **Start the Application**  
   Launch the application with the following command:  
   ```bash
   bash run.sh
   ```

## To run internal scripts:
   ```bash
   PYTHONPATH=$(pwd) python scripts/script_name.py
   ```
