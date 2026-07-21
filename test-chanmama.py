#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试蝉妈妈登录接口
"""

import hashlib
import requests
import json
from datetime import datetime

# 账号信息
USERNAME = "13888155195"
PASSWORD = "ZYP1025zyp"

def encrypt_password(password):
    """MD5加密密码"""
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode())
    return md5_hash.hexdigest()

def test_login():
    """测试登录接口"""
    print("=" * 60)
    print("蝉妈妈登录测试")
    print("=" * 60)
    
    # 加密密码
    encrypted_password = encrypt_password(PASSWORD)
    print(f"✓ 密码已加密: {encrypted_password[:16]}...")
    
    # 准备登录数据
    timestamp = int(datetime.now().timestamp())
    login_data = {
        'username': USERNAME,
        'password': encrypted_password,
        'appId': 10000,
        'timeStamp': timestamp
    }
    
    print(f"✓ 时间戳: {timestamp}")
    print(f"✓ 用户名: {USERNAME[:3]}****{USERNAME[-4:]}")
    
    # 发送登录请求
    print("\n正在登录...")
    try:
        response = requests.post(
            'https://api-service.chanmama.com/v1/access/token',
            json=login_data,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        print(f"✓ HTTP状态码: {response.status_code}")
        
        # 解析响应
        result = response.json()
        print(f"✓ 响应码: {result.get('errCode')}")
        
        if result.get('errCode') == 0:
            token = result['data']['token']
            expire_time = result['data']['expire_time']
            
            print(f"\n✅ 登录成功！")
            print(f"✓ Token: {token[:50]}...")
            print(f"✓ 过期时间: {datetime.fromtimestamp(expire_time)}")
            
            # 保存Token到文件
            with open('chanmama_token.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'token': token,
                    'expire_time': expire_time,
                    'created_at': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Token已保存到: chanmama_token.json")
            
            return token
        else:
            print(f"\n❌ 登录失败: {result.get('errMsg', '未知错误')}")
            print(f"完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_data_fetch(token):
    """测试数据爬取"""
    print("\n" + "=" * 60)
    print("测试数据爬取")
    print("=" * 60)
    
    cookies = {
        'LOGIN-TOKEN-FORSNS': token
    }
    
    # 测试获取达人销量排行榜
    params = {
        'day_type': 'day',
        'day': datetime.now().strftime('%Y-%m-%d'),
        'category_id': '-1',
        'sort': 'sales_volume',
        'page': '1',
        'size': '10'
    }
    
    print(f"请求参数: {json.dumps(params, ensure_ascii=False)}")
    print("\n正在获取数据...")
    
    try:
        response = requests.get(
            'https://api-service.chanmama.com/v5/douyin/live/rank/author/sales',
            params=params,
            cookies=cookies,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            timeout=10
        )
        
        print(f"✓ HTTP状态码: {response.status_code}")
        
        result = response.json()
        print(f"✓ 响应码: {result.get('errCode')}")
        
        if result.get('errCode') == 0:
            data = result.get('data', {})
            print(f"\n✅ 数据获取成功！")
            print(f"✓ 数据类型: {type(data)}")
            
            # 保存原始数据
            with open('chanmama_test_data.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✓ 数据已保存到: chanmama_test_data.json")
            
            # 显示部分数据
            if isinstance(data, dict):
                print(f"\n数据字段: {list(data.keys())}")
            elif isinstance(data, list):
                print(f"\n数据条数: {len(data)}")
                if len(data) > 0:
                    print(f"第一条数据: {json.dumps(data[0], ensure_ascii=False)[:200]}...")
            
            return True
        else:
            print(f"\n❌ 数据获取失败: {result.get('errMsg', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n⚠️  警告：此脚本仅用于个人学习研究\n")
    
    # 测试登录
    token = test_login()
    
    if token:
        # 测试数据爬取
        test_data_fetch(token)
    else:
        print("\n❌ 登录失败，无法继续测试")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
