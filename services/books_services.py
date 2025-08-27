class BookService:
    def __init__(self, neo4j_driver):
        """初始化用户服务类，使用已创建的neo4j驱动
        :param neo4j_driver: Neo4j 驱动实例
        """
        self.driver = neo4j_driver

    def create_book(self, book_id, title, author):
        """
        创建书籍
        :param book_id: 书籍ID
        :param title: 书籍标题
        :param author: 书籍作者
        :return: 新创建的书籍信息
        """
        with self.driver.session() as session:
            # 检查书籍是否已存在
            result = session.run("MATCH (b:Book {id: $book_id}) RETURN b", book_id=book_id)
            if result.single():
                return None
            # 创建新书籍
            result = session.run(
                "CREATE (b:Book {id: $book_id, title: $title, author: $author}) RETURN b",
                book_id=book_id, title=title, author=author
            )
            record = result.single()
            if record:
                return dict(record["b"])
            return None

    def update_book(self, book_id, new_title=None, new_author=None):
        """
        更新书籍信息
        :param book_id: 书籍ID
        :param new_title: 新的书籍标题
        :param new_author: 新的书籍作者
        :return: 更新后的书籍信息，若书籍不存在则返回 None
        """
        with self.driver.session() as session:
            # 构建Cypher语句和参数
            query = "MATCH (b:Book {id: $book_id})"
            set_clauses = []
            params = {"book_id": book_id}

            if new_title:
                set_clauses.append("b.title = $new_title")
                params["new_title"] = new_title
            if new_author:
                set_clauses.append("b.author = $new_author")
                params["new_author"] = new_author

            if not set_clauses:
                # 如果没有更新内容，直接查询书籍
                result = session.run("MATCH (b:Book {id: $book_id}) RETURN b", book_id=book_id)
                record = result.single()
                return dict(record["b"]) if record else None

            query += " SET " + ", ".join(set_clauses) + " RETURN b"
            result = session.run(query, params)
            record = result.single()
            return dict(record["b"]) if record else None

    def delete_book(self, book_id):
        """
        删除书籍
        :param book_id: 书籍ID
        :return: 若删除成功返回 True，若书籍不存在返回 False
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:Book {id: $book_id}) DELETE b RETURN count(b) as deleted_count",
                book_id=book_id
            )
            record = result.single()
            return record["deleted_count"] == 0

    def get_book(self, book_id):
        """
        获取单个书籍信息
        :param book_id: 书籍ID
        :return: 书籍信息，若书籍不存在则返回 None
        """
        with self.driver.session() as session:
            result = session.run("MATCH (b:Book {id: $book_id}) RETURN b", book_id=book_id)
            record = result.single()
            return dict(record["b"]) if record else None

    def get_all_books(self):
        """
        获取所有书籍信息
        :return: 包含所有书籍信息的列表
        """
        with self.driver.session() as session:
            result = session.run("MATCH (b:Book) RETURN b")
            return [dict(record["b"]) for record in result]


if __name__ == "__main__":
    # 使用示例，需要根据实际情况修改URI、用户名和密码
    book_service = BookService("bolt://localhost:7687", "neo4j", "password")

    try:
        # 创建书籍
        new_book = book_service.create_book(1, "Python编程", "Guido van Rossum")
        print("创建的书籍:", new_book)

        # 查询书籍
        book = book_service.get_book(1)
        print("查询的书籍:", book)

        # 更新书籍
        updated_book = book_service.update_book(1, new_title="Python编程：从入门到实践")
        print("更新后的书籍:", updated_book)

        # 查询所有书籍
        all_books = book_service.get_all_books()
        print("所有书籍:", all_books)

        # 删除书籍
        deleted = book_service.delete_book(1)
        print("删除结果:", "成功" if deleted else "失败")
    finally:
        book_service.close()
