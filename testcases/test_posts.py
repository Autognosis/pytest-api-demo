import pytest


class TestPosts:
    """测试 /posts 接口"""

    def test_get_all_posts(self, api_client):
        """获取所有文章，验证返回 200 且数据量正确"""
        response = api_client.get("posts")
        assert response.status_code == 200
        posts = response.json()
        assert len(posts) == 100  # JSONPlaceholder 固定返回 100 条
        assert all({"userId", "id", "title", "body"} <= post.keys() for post in posts)

    @pytest.mark.parametrize(
        argnames="post_id, expected_status",
        argvalues=[
            (1, 200),
            (2, 200),
            (3, 200),
            (99, 200),
            (100, 200),
        ],
    )
    def test_get_post_by_id_success(self, api_client, post_id, expected_status):
        """参数化测试：验证合法 ID 的文章都能正常获取，非法 ID 返回 404"""
        response = api_client.get(f"posts/{post_id}")
        assert response.status_code == expected_status
        post = response.json()
        assert post["id"] == post_id
        assert "title" in post
        assert "body" in post

    @pytest.mark.parametrize(
        argnames="post_id, expected_status",
        argvalues=[
            (999999, 404),
            (-1, 404),
            (0, 404),
            ("abc", 404),
            (None, 404),
            (" ", 404),
            ("@#$%", 404),
            ("1.5", 404),
            ("1e10", 404),
            ("null", 404),
            ("true", 404),
            ("false", 404),
            ("[]", 404),
            ("{}", 404),
            ("None", 404),
            ("NaN", 404),
            ("Infinity", 404),
            ("-Infinity", 404),
            ("0x1A", 404),
            ("0b101", 404),
            ("0o17", 404),
            ("1/2", 404),
            ("1\\2", 404),
            ("1+1", 404),
            ("1-1", 404),
            ("1*1", 404),
            ("1%1", 404),
            ("1^1", 404),
            ("1&1", 404),
            ("1|1", 404),
            ("1<<1", 404),
            ("1>>1", 404),
            ("1==1", 404),
            ("1!=1", 404),
            ("测试", 404),
            ("测试123", 404),
            ("123测试", 404),
            ("!@#$%^&*()", 404),
            ("`~", 404),
            ("[]{}", 404),
            ("<>?", 404),
            ("/\\", 404),
            ("|", 404),
            (";", 404),
            (":", 404),
            ("'", 404),
            (",", 404),
            ("-", 404),
            ("_", 404),
            ("001", 404),
            ("1' OR '1'='1", 404),
            ("1; DROP TABLE posts;", 404),
            ("<script>alert(1)</script>", 404),
            ("../admin", 404),
            ("..\\", 404),
            ("C:\\Windows\\System32", 404),
            ("C:/Windows/System32", 404),
            ("~/.bashrc", 404),
            ("~/.ssh/id_rsa", 404),
            ("~/.ssh/id_rsa.pub", 404),
            ("~/.ssh/known_hosts", 404),
            ("~/.ssh/config", 404),
            ("~/.gitconfig", 404),
            ("~/.vimrc", 404),
            ("~/.zshrc", 404),
            ("~/.bash_profile", 404),
            ("~/.bash_logout", 404),
            ("~/.profile", 404),
        ],
    )
    def test_get_post_by_id_not_found(self, api_client, post_id, expected_status):
        """参数化测试：验证非法 ID 返回 404"""
        response = api_client.get(f"posts/{post_id}")
        assert response.status_code == expected_status
        assert response.json() == {}

    def test_create_post(self, api_client):
        """创建文章，验证返回 201"""
        new_post = {"title": "测试文章标题", "body": "这是测试文章的内容", "userId": 1}
        response = api_client.post("posts", data=new_post)
        assert response.status_code == 201
        result = response.json()
        assert result["title"] == new_post["title"]
        assert result["body"] == new_post["body"]
        assert result["userId"] == new_post["userId"]
