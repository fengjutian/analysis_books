class AuthorService:
    def __init__(self, neo4j_driver):
        """
        初始化作者服务类
        :param neo4j_driver: Neo4j 驱动实例
        """
        self.driver = neo4j_driver

    def create_author(self, name, email, gender, birth_date, birth_place, family_members, imdb_id, occupation):
        """
        创建作者节点
        :param name: 作者名
        :param email: 邮箱
        :param gender: 性别
        :param birth_date: 出生日期
        :param birth_place: 出生地
        :param family_members: 家庭成员
        :param imdb_id: IMDB ID
        :param occupation: 职业
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
                "CREATE (a:Author {author_id: $author_id, name: $name, email: $email, gender: $gender, birth_date: $birth_date, birth_place: $birth_place, family_members: $family_members, imdb_id: $imdb_id, occupation: $occupation}) RETURN a",
                author_id=new_id, name=name, email=email, gender=gender, birth_date=birth_date, birth_place=birth_place, family_members=family_members, imdb_id=imdb_id, occupation=occupation
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

    def update_author(self, author_id, new_name=None, new_email=None, new_gender=None, new_birth_date=None, new_birth_place=None, new_family_members=None, new_imdb_id=None, new_occupation=None):
        """
        修改作者信息
        :param author_id: 作者 ID
        :param new_name: 新作者名
        :param new_email: 新邮箱
        :param new_gender: 新性别
        :param new_birth_date: 新出生日期
        :param new_birth_place: 新出生地
        :param new_family_members: 新家庭成员
        :param new_imdb_id: 新IMDB ID
        :param new_occupation: 新职业
        :return: 更新后的作者节点，若作者不存在则返回 None
        """
        with self.driver.session() as session:
            query = "MATCH (a:Author {author_id: $author_id})"
            set_clauses = []
            params = {"author_id": author_id}
            
            if new_name is not None:
                set_clauses.append("a.name = $new_name")
                params["new_name"] = new_name
            if new_email is not None:
                set_clauses.append("a.email = $new_email")
                params["new_email"] = new_email
            if new_gender is not None:
                set_clauses.append("a.gender = $new_gender")
                params["new_gender"] = new_gender
            if new_birth_date is not None:
                set_clauses.append("a.birth_date = $new_birth_date")
                params["new_birth_date"] = new_birth_date
            if new_birth_place is not None:
                set_clauses.append("a.birth_place = $new_birth_place")
                params["new_birth_place"] = new_birth_place
            if new_family_members is not None:
                set_clauses.append("a.family_members = $new_family_members")
                params["new_family_members"] = new_family_members
            if new_imdb_id is not None:
                set_clauses.append("a.imdb_id = $new_imdb_id")
                params["new_imdb_id"] = new_imdb_id
            if new_occupation is not None:
                set_clauses.append("a.occupation = $new_occupation")
                params["new_occupation"] = new_occupation
            
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
                "email": author_node.get("email", f"{author_node['name'].lower()}@example.com"),
                "gender": author_node.get("gender", ""),
                "birth_date": author_node.get("birth_date", ""),
                "birth_place": author_node.get("birth_place", ""),
                "family_members": author_node.get("family_members", ""),
                "imdb_id": author_node.get("imdb_id", ""),
                "occupation": author_node.get("occupation", "")
            }
                authors.append(author_dict)
            return authors
