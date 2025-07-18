"""
추천 서비스 빠른 테스트 스크립트 (RESTful API)
"""
import asyncio
import httpx

BASE_URL = "http://localhost:8000/api/recommender/v1"

async def test_api():
    """RESTful API 테스트 실행"""
    async with httpx.AsyncClient() as client:
        print("🚀 추천 서비스 RESTful API 테스트 시작\n")
        
        # 1. 기본 헬스체크
        try:
            response = await client.get(f"{BASE_URL}/health/simple")
            print(f"✅ 헬스체크: {response.status_code}")
            print(f"   응답: {response.json()}\n")
        except Exception as e:
            print(f"❌ 헬스체크 실패: {e}\n")
            return
        
        # 2. 더미 데이터 확인
        try:
            response = await client.get(f"{BASE_URL}/test/dummy-data")
            print(f"✅ 더미 데이터: {response.status_code}")
            data = response.json()
            print(f"   사용자 수: {len(data['data']['users'])}")
            print(f"   웹소설 수: {len(data['data']['novels'])}\n")
        except Exception as e:
            print(f"❌ 더미 데이터 실패: {e}\n")
        
        # 3. RESTful 사용자 추천 테스트 (POST)
        try:
            user_id = 1
            response = await client.post(
                f"{BASE_URL}/users/{user_id}/recommendations",
                json={
                    "limit": 5,
                    "recommendation_type": "popular"
                }
            )
            print(f"✅ 사용자 추천 (POST): {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   사용자 ID: {result['user_id']}")
                print(f"   추천 개수: {result['total_count']}")
                for rec in result['recommendations'][:2]:  # 처음 2개만 출력
                    print(f"   - {rec['title']} (점수: {rec['score']:.2f})")
            else:
                print(f"   에러: {response.text}")
            print()
        except Exception as e:
            print(f"❌ 사용자 추천 (POST) 실패: {e}\n")
        
        # 4. RESTful 사용자 추천 테스트 (GET)
        try:
            user_id = 1
            response = await client.get(
                f"{BASE_URL}/users/{user_id}/recommendations?limit=3"
            )
            print(f"✅ 사용자 추천 (GET): {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   추천 개수: {result['total_count']}")
            else:
                print(f"   에러: {response.text}")
            print()
        except Exception as e:
            print(f"❌ 사용자 추천 (GET) 실패: {e}\n")
        
        # 5. RESTful 유사 작품 추천 테스트 (POST)
        try:
            novel_id = 1
            response = await client.post(
                f"{BASE_URL}/novels/{novel_id}/similar",
                json={
                    "limit": 3,
                    "similarity_threshold": 0.1
                }
            )
            print(f"✅ 유사 작품 추천 (POST): {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   유사 작품 개수: {len(result)}")
                for rec in result[:2]:  # 처음 2개만 출력
                    print(f"   - {rec['title']} (유사도: {rec['score']:.2f})")
            else:
                print(f"   에러: {response.text}")
            print()
        except Exception as e:
            print(f"❌ 유사 작품 추천 (POST) 실패: {e}\n")
        
        print("🎉 RESTful API 테스트 완료!")

if __name__ == "__main__":
    asyncio.run(test_api())
