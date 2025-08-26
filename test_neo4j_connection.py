from neo4j import GraphDatabase
import os

def test_connection():
    # 使用与db.py相同的连接配置
    NEO4J_URI = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASS = os.getenv("NEO4J_PASS", "neo4j")
    
    print(f"Testing connection to Neo4j at {NEO4J_URI} with user {NEO4J_USER}")
    
    try:
        # 创建驱动
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
        
        # 测试连接
        with driver.session() as session:
            result = session.run("RETURN 'Hello, Neo4j!' AS message")
            record = result.single()
            if record:
                print(f"Connection successful! Message: {record['message']}")
            else:
                print("Connection successful but no result returned.")
        
        # 关闭驱动
        driver.close()
        print("Driver closed successfully.")
        
    except Exception as e:
        print(f"Connection failed: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_connection()