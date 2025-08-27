class SchoolService:
    def __init__(self, neo4j_driver):
        """初始化学校服务类，使用已创建的neo4j驱动
        :param neo4j_driver: Neo4j 驱动实例
        """
        self.driver = neo4j_driver

    def create_school(self, title, author):
        """
        创建学校，自动生成唯一的school_id
        :param title: 学校名称
        :param author: 学校创建者
        :return: 新创建的学校信息
        """
        with self.driver.session() as session:
            # 生成唯一的school_id (通过获取当前最大ID并加1)
            result = session.run("MATCH (s:School) RETURN COALESCE(MAX(s.id), 0) AS max_id")
            max_id = result.single()['max_id']
            school_id = max_id + 1
            
            # 创建新学校
            result = session.run(
                "CREATE (s:School {id: $school_id, title: $title, author: $author}) RETURN s",
                school_id=school_id, title=title, author=author
            )
            record = result.single()
            if record:
                return dict(record["s"])
            return None

    def update_school(self, school_id, new_title=None, new_author=None):
        """
        更新学校信息
        :param school_id: 学校ID
        :param new_title: 新的学校名称
        :param new_author: 新的学校创建者
        :return: 更新后的学校信息，若学校不存在则返回 None
        """
        with self.driver.session() as session:
            # 构建Cypher语句和参数
            query = "MATCH (s:School {id: $school_id})"
            set_clauses = []
            params = {"school_id": school_id}

            if new_title:
                set_clauses.append("s.title = $new_title")
                params["new_title"] = new_title
            if new_author:
                set_clauses.append("s.author = $new_author")
                params["new_author"] = new_author

            if not set_clauses:
                # 如果没有更新内容，直接查询学校
                result = session.run("MATCH (s:School {id: $school_id}) RETURN s", school_id=school_id)
                record = result.single()
                return dict(record["s"]) if record else None

            query += " SET " + ", ".join(set_clauses) + " RETURN s"
            result = session.run(query, params)
            record = result.single()
            return dict(record["s"]) if record else None

    def delete_school(self, school_id):
        """
        删除学校
        :param school_id: 学校ID
        :return: 若删除成功返回 True，若学校不存在返回 False
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (s:School {id: $school_id}) DELETE s RETURN count(s) as deleted_count",
                school_id=school_id
            )
            record = result.single()
            return record["deleted_count"] == 0

    def get_school(self, school_id):
        """
        获取单个学校信息
        :param school_id: 学校ID
        :return: 学校信息，若学校不存在则返回 None
        """
        with self.driver.session() as session:
            result = session.run("MATCH (s:School {id: $school_id}) RETURN s", school_id=school_id)
            record = result.single()
            return dict(record["s"]) if record else None

    def get_all_schools(self):
        """
        获取所有学校信息
        :return: 包含所有学校信息的列表
        """
        with self.driver.session() as session:
            result = session.run("MATCH (s:School) RETURN s")
            return [dict(record["s"]) for record in result]


if __name__ == "__main__":
    # 使用示例，需要根据实际情况修改URI、用户名和密码
    school_service = SchoolService("bolt://localhost:7687", "neo4j", "password")

    try:
        # 创建学校
        new_school = school_service.create_school(1, "北京大学", "蔡元培")
        print("创建的学校:", new_school)

        # 查询学校
        school = school_service.get_school(1)
        print("查询的学校:", school)

        # 更新学校
        updated_school = school_service.update_school(1, new_title="北京大学（北京校区）")
        print("更新后的学校:", updated_school)

        # 查询所有学校
        all_schools = school_service.get_all_schools()
        print("所有学校:", all_schools)

        # 删除学校
        deleted = school_service.delete_school(1)
        print("删除结果:", "成功" if deleted else "失败")
    finally:
        school_service.close()
