from neo4j import GraphDatabase
import os
import getpass

def test_connection_with_credentials():
    # 获取用户输入的凭据
    default_uri = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    default_user = os.getenv("NEO4J_USER", "neo4j")
    
    neo4j_uri = input(f"Enter Neo4j URI [{default_uri}]: ") or default_uri
    neo4j_user = input(f"Enter Neo4j username [{default_user}]: ") or default_user
    neo4j_pass = getpass.getpass(f"Enter Neo4j password (will not be displayed): ")
    
    print(f"\nTesting connection to Neo4j at {neo4j_uri} with user {neo4j_user}")
    
    try:
        # 创建驱动
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
        
        # 测试连接
        with driver.session() as session:
            result = session.run("RETURN 'Hello, Neo4j!' AS message")
            record = result.single()
            if record:
                print(f"Connection successful! Message: {record['message']}")
                
                # 如果连接成功，提示用户如何更新db.py文件
                print("\nTo update your application with these credentials:")
                print(f"1. Open app/db.py")
                print(f"2. Update the following lines:")
                print(f"   NEO4J_URI = os.getenv(\"NEO4J_URI\", \"{neo4j_uri}\")")
                print(f"   NEO4J_USER = os.getenv(\"NEO4J_USER\", \"{neo4j_user}\")")
                print(f"   NEO4J_PASS = os.getenv(\"NEO4J_PASS\", \"your_password_here\")")
                print("   OR set environment variables with these values")
            else:
                print("Connection successful but no result returned.")
        
        # 关闭驱动
        driver.close()
        print("Driver closed successfully.")
        
    except Exception as e:
        print(f"Connection failed: {type(e).__name__}: {e}")
        print("\nPlease check your Neo4j server is running and your credentials are correct.")

if __name__ == "__main__":
    print("Neo4j Connection Tester")
    print("=====================")
    print("This tool will help you test your Neo4j connection credentials.")
    print("Please make sure Neo4j server is running before proceeding.")
    print("")
    test_connection_with_credentials()