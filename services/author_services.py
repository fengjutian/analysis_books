class AuthorService:
    def __init__(self, neo4j_driver):
        """
        初始化作者服务类
        :param neo4j_driver: Neo4j 驱动实例
        """
        self.driver = neo4j_driver

    def create_author(self, name, age):
        """
        创建作者节点
        :param name: 作者名
        :param age: 作者年龄
        :return: 创建的作者节点
        """
        with self.driver.session() as session:
            # 自动生成唯一ID：查询当前最大ID并加1
            result = session.run(
                "MATCH (a:Author) RETURN COALESCE(MAX(toInteger(a.author_id)), 0) as max_id"
            )
            max_id = result.single()['max_id']
            new_id = str(max_id + 1)
            
            # 创建新作者
            result = session.run(
                "CREATE (a:Author {author_id: $author_id, name: $name, age: $age}) RETURN a",
                author_id=new_id, name=name, age=age
            )
            return result.single()[0]

    def get_author(self, author_id):
        """
        根据作者 ID 查询作者
        :param author_id: 作者 ID
        :return: 作者节点，若不存在则返回 None
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (a:Author {author_id: $author_id}) RETURN a",
                author_id=author_id
            )
            record = result.single()
            return record[0] if record else None

    def update_author(self, author_id, new_name=None, new_age=None):
        """
        修改作者信息
        :param author_id: 作者 ID
        :param new_name: 新作者名
        :param new_age: 新年龄
        :return: 更新后的作者节点，若作者不存在则返回 None
        """
        with self.driver.session() as session:
            query = "MATCH (a:Author {author_id: $author_id})"
            set_clauses = []
            params = {"author_id": author_id}
            
            if new_name is not None:
                set_clauses.append("a.name = $new_name")
                params["new_name"] = new_name
            if new_age is not None:
                set_clauses.append("a.age = $new_age")
                params["new_age"] = new_age
            
            if set_clauses:
                query += " SET " + ", ".join(set_clauses)
                query += " RETURN a"
                result = session.run(query, **params)
                record = result.single()
                return record[0] if record else None
            return None

    def delete_author(self, author_id):
        """
        根据作者 ID 删除作者
        :param author_id: 作者 ID
        :return: 是否删除成功
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (a:Author {author_id: $author_id}) DELETE a RETURN count(a) as deleted_count",
                author_id=author_id
            )
            return result.single()[0] == 0
    
    def get_all_authors(self):
        """
        获取所有作者
        :return: 作者列表
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (a:Author) RETURN a"
            )
            authors = []
            for record in result:
                author_node = record["a"]
                # Convert Neo4j node to dictionary format
                author_dict = {
                    "id": int(author_node["author_id"]),  # Convert to int to match the Author model
                    "name": author_node["name"],
                    "email": f"{author_node['name'].lower()}@example.com"  # Generate email as it's not in the database
                }
                authors.append(author_dict)
            return authors
