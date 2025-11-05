"""测试 JWT 认证是否正常工作"""
import requests
import json

BASE_URL = 'http://localhost:5002/api'

def test_jwt():
    print("=" * 50)
    print("测试 JWT 认证流程")
    print("=" * 50)
    
    # 1. 测试登录
    print("\n1. 测试登录...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ 登录成功")
            print(f"   用户: {result['user']['username']}")
            print(f"   角色: {result['user']['role']}")
            
            token = result['access_token']
            print(f"   Token: {token[:50]}...")
            
            # 2. 测试使用 token 获取用户信息
            print("\n2. 测试使用 Token 获取用户资料...")
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            profile_response = requests.get(f'{BASE_URL}/auth/profile', headers=headers)
            print(f"   状态码: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print(f"   ✓ 获取成功")
                print(f"   用户名: {profile['username']}")
                print(f"   角色: {profile['role']}")
            else:
                print(f"   ✗ 获取失败")
                print(f"   错误: {profile_response.text}")
            
            # 3. 测试获取日程列表
            print("\n3. 测试获取日程列表...")
            events_response = requests.get(f'{BASE_URL}/events', headers=headers)
            print(f"   状态码: {events_response.status_code}")
            
            if events_response.status_code == 200:
                events_data = events_response.json()
                print(f"   ✓ 获取成功")
                print(f"   日程数量: {events_data['count']}")
            else:
                print(f"   ✗ 获取失败")
                print(f"   错误: {events_response.text}")
                
        else:
            print(f"   ✗ 登录失败")
            print(f"   错误: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ✗ 无法连接到后端服务")
        print("   请确保后端服务正在运行在 http://localhost:5002")
    except Exception as e:
        print(f"   ✗ 发生错误: {str(e)}")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == '__main__':
    test_jwt()

