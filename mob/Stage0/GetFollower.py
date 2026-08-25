import requests
import certifi

def get_followers(username="torvalds"):
    """
    通过 GitHub 公共 API 获取指定用户的粉丝数量。

    Args:
        username (str): GitHub 用户名，默认为 "torvalds"

    Returns:
        int or None: 粉丝数量，如果请求失败则返回 None
    """
    url = f"https://api.github.com/users/{username}"

    try:
        response = requests.get(url, verify=False)

        response.raise_for_status()

        user_data = response.json()
        return user_data["followers"]

    except requests.exceptions.RequestException as e:
        print(f"请求github api发生错误: {e}")
        return None

if __name__ == "__main__":
    followers = get_followers()

    if followers is not None:
        print(f"用户 torvalds 的粉丝数量为: {followers}")
    else:
        print("获取粉丝数量失败，请检查网络连接或用户名是否正确。")