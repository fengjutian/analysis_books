class UserService:
    def __init__(self, neo4j_driver):
        """
        初始化用户服务类
        :param neo4j_driver: Neo4j 驱动实例
        """
        self.driver = neo4j_driver

    def create_user(self, user_id, name, age):
        """
        创建用户节点
        :param user_id: 用户 ID
        :param name: 用户名
        :param age: 用户年龄
        :return: 创建的用户节点
        """
        with self.driver.session() as session:
            result = session.run(
                "CREATE (u:User {user_id: $user_id, name: $name, age: $age}) RETURN u",
                user_id=user_id, name=name, age=age
            )
            return result.single()[0]

    def get_user(self, user_id):
        """
        根据用户 ID 查询用户
        :param user_id: 用户 ID
        :return: 用户节点，若不存在则返回 None
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User {user_id: $user_id}) RETURN u",
                user_id=user_id
            )
            record = result.single()
            return record[0] if record else None

    def update_user(self, user_id, new_name=None, new_age=None):
        """
        修改用户信息
        :param user_id: 用户 ID
        :param new_name: 新用户名
        :param new_age: 新年龄
        :return: 更新后的用户节点，若用户不存在则返回 None
        """
        with self.driver.session() as session:
            query = "MATCH (u:User {user_id: $user_id})"
            set_clauses = []
            params = {"user_id": user_id}
            
            if new_name is not None:
                set_clauses.append("u.name = $new_name")
                params["new_name"] = new_name
            if new_age is not None:
                set_clauses.append("u.age = $new_age")
                params["new_age"] = new_age
            
            if set_clauses:
                query += " SET " + ", ".join(set_clauses)
                query += " RETURN u"
                result = session.run(query, **params)
                record = result.single()
                return record[0] if record else None
            return None

    def delete_user(self, user_id):
        """
        根据用户 ID 删除用户
        :param user_id: 用户 ID
        :return: 是否删除成功
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User {user_id: $user_id}) DELETE u RETURN count(u) as deleted_count",
                user_id=user_id
            )
            return result.single()[0] == 0
    
    def get_all_users(self):
        """
        获取所有用户
        :return: 用户列表
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User) RETURN u"
            )
            users = []
            for record in result:
                user_node = record["u"]
                # Convert Neo4j node to dictionary format
                user_dict = {
                    "id": int(user_node["user_id"]),  # Convert to int to match the User model
                    "name": user_node["name"],
                    "email": f"{user_node['name'].lower()}@example.com"  # Generate email as it's not in the database
                }
                users.append(user_dict)
            return users
