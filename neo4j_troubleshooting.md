# Neo4j Connection Troubleshooting Guide

This guide will help you troubleshoot and resolve common Neo4j connection issues in the FastAPI application.

## Common Connection Errors

### 1. Authentication Error

**Error Message:** `neo4j.exceptions.AuthError: {code: Neo.ClientError.Security.Unauthorized} {message: The client is unauthorized due to authentication failure.}`

**Possible Causes:**
- Incorrect username or password
- Default password not changed after initial Neo4j installation
- Neo4j server running with different authentication settings

**Solutions:**
1. Verify your Neo4j username and password
2. If you're using a fresh Neo4j installation, ensure you've changed the default password
3. Check if Neo4j is configured to require authentication (it should be enabled by default)

### 2. Service Unavailable Error

**Error Message:** `neo4j.exceptions.ServiceUnavailable: Unable to retrieve routing information`

**Possible Causes:**
- Neo4j server is not running
- Network connectivity issues
- Incorrect URI or port
- Firewall blocking the connection

**Solutions:**
1. Ensure Neo4j server is running
2. Verify the URI and port are correct (default is `neo4j://localhost:7687`)
3. Check network connectivity to the Neo4j server
4. Ensure firewall settings allow connections to the Neo4j port

## Checking if Neo4j is Running

### Windows
1. Open the Neo4j Desktop application
2. Check if your database is marked as "Running"
3. If not, click the "Start" button to start the database

### macOS/Linux
```bash
# Check Neo4j service status
sudo systemctl status neo4j

# Start Neo4j service if it's not running
sudo systemctl start neo4j
```

## Resetting Neo4j Password

If you've forgotten your Neo4j password or need to change it:

### Using Neo4j Browser
1. Open Neo4j Browser (http://localhost:7474)
2. Log in with your current credentials
3. Run the following command to change your password:
   ```cypher
   ALTER USER neo4j SET PASSWORD 'new_password';
   ```

### Resetting Default Password
If you're using a fresh installation and haven't changed the default password:
1. Start Neo4j server
2. Open Neo4j Browser (http://localhost:7474)
3. When prompted, enter the default username `neo4j` and password `neo4j`
4. You'll be asked to set a new password
5. Update your application configuration with the new password

## Updating Application Configuration

Once you have the correct Neo4j credentials, you can update the application configuration in two ways:

### 1. Update the Configuration File

Open `app/db.py` and update the following lines with your correct credentials:

```python
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "your_username_here")
NEO4J_PASS = os.getenv("NEO4J_PASS", "your_password_here")
```

### 2. Set Environment Variables

Set the following environment variables with your correct credentials:

**Windows (Command Prompt):**
```cmd
set NEO4J_URI=neo4j://localhost:7687
set NEO4J_USER=your_username_here
set NEO4J_PASS=your_password_here
```

**Windows (PowerShell):**
```powershell
$env:NEO4J_URI="neo4j://localhost:7687"
$env:NEO4J_USER="your_username_here"
$env:NEO4J_PASS="your_password_here"
```

**macOS/Linux:**
```bash
export NEO4J_URI="neo4j://localhost:7687"
export NEO4J_USER="your_username_here"
export NEO4J_PASS="your_password_here"
```

## Testing the Connection

After updating your credentials, use the provided test scripts to verify the connection:

```bash
# Run the simple connection test
python test_neo4j_connection.py

# Or run the interactive connection test to try different credentials
python test_neo4j_interactive.py
```

## Additional Resources

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Neo4j Driver for Python Documentation](https://neo4j.com/docs/python-manual/current/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

If you continue to experience issues, please check the Neo4j server logs for more detailed error information.