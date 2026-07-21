#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试千瓜数据登录接口
"""

import requests
import json
from datetime import datetime

# 账号信息
USERNAME = "13888155195"
PASSWORD = "ZYP1025zyp"

def test_qiangua_login():
    """测试千瓜数据登录"""
    print("=" * 60)
    print("千瓜数据登录测试")
    print("=" * 60)
    
    print(f"✓ 用户名: {USERNAME[:3]}****{USERNAME[-4:]}")
    
    # 尝试多种登录接口
    login_urls = [
        'https://api.qian-gua.com/api/login',
        'https://app.qian-gua.com/api/login',
        'https://api.qian-gua.com/v1/login',
        'https://api.qian-gua.com/user/login'
    ]
    
    login_data = {
        'phone': USERNAME,
        'password': PASSWORD,
        'loginType': 'password'
    }
    
    for url in login_urls:
        print(f"\n尝试接口: {url}")
        try:
            response = requests.post(
                url,
                json=login_data,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Content-Type': 'application/json',
                    'Origin': 'https://app.qian-gua.com',
                    'Referer': 'https://app.qian-gua.com/'
                },
                timeout=10
            )
            
            print(f"✓ HTTP状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ 响应: {json.dumps(result, ensure_ascii=False)[:200]}")
                
                # 检查是否成功
                if result.get('code') == 0 or result.get('success') or 'token' in str(result).lower():
                    print(f"\n✅ 登录成功！")
                    return result
                else:
                    print(f"❌ 登录失败: {result.get('message', result.get('msg', '未知错误'))}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("❌ 请求超时")
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    return None

def test_qiangua_category():
    """测试千瓜分类数据接口"""
    print("\n" + "=" * 60)
    print("测试千瓜分类数据")
    print("=" * 60)
    
    # 尝试访问分类数据页面
    urls = [
        'https://api.qian-gua.com/api/category/list',
        'https://app.qian-gua.com/api/category',
        'https://api.qian-gua.com/v1/data/category'
    ]
    
    for url in urls:
        print(f"\n尝试接口: {url}")
        try:
            response = requests.get(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json'
                },
                timeout=10
            )
            
            print(f"✓ HTTP状态码: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✓ 响应: {response.text[:200]}")
                return True
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    return False

if __name__ == '__main__':
    print("\n⚠️  警告：此脚本仅用于个人学习研究\n")
    
    # 测试登录
    result = test_qiangua_login()
    
    if result:
        print("\n✅ 登录成功，可以继续测试数据接口")
    else:
        print("\n❌ 登录失败，尝试直接访问数据接口")
        test_qiangua_category()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
