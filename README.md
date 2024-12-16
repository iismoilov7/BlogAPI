## Setup Instructions for BlogAPI Server

1. **Install Required Packages**  
   Run the following command to install the necessary dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare the Database**  
   Use Docker Compose to set up the database:  
   ```bash
   sudo docker-compose up
   ```

3. **Generate secret and public keys for JWT**
   Use library openssl
   ```bash
   openssl genrsa -out certs/jwt-private.pem 2048
   openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
   ```


3. **Start the Application**  
   Launch the application with the following command:  
   ```bash
   bash run.sh
   ```
