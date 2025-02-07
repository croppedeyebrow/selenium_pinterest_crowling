    #csv파일에 있는 이미지를 기반으로, tpo/weather_condition/preference 만들기

import pandas as pd
import os

def categorize_image(search_term):
    """검색어를 기반으로 TPO, 날씨씨, 추구 컨셉을을 분류"""
    
    # TPO 분류
    tpo = 'daily'  # 기본값
    if 'resort' in search_term:
        tpo = 'resort'
    elif 'classy' in search_term or 'demure' in search_term:
        tpo = 'wedding guest'
    elif 'cute' in search_term:
        tpo = 'date'
    elif 'party' in search_term:
        tpo = 'party'   
    elif 'work' in search_term:
        tpo = 'office'  
                   
    # 계절 분류
    weather_condition = 'all'  # 기본값
    if 'summer' in search_term:
        weather_condition = 'hot'
    elif 'winter' in search_term:
        weather_condition = 'cold'
    elif 'spring' in search_term:
        weather_condition = 'warm'
    elif 'autumn' in search_term:
        weather_condition = 'chill'
    elif 'cold' in search_term:
        weather_condition = 'cold wave' 
    elif 'summer umbrella' in search_term:
        weather_condition = 'summer umbrella rainy'        
    elif 'winter umbrella' in search_term:
        weather_condition = 'winter umbrella rainy'          
    elif 'spring umbrella' in search_term:
        weather_condition = 'spring umbrella rainy'          
    elif 'authum umbrella' in search_term:
        weather_condition = 'authum umbrella rainy'          
   
                
    # 스타일 선호도
    preference = 'normal'  # 기본값
    if 'cute' in search_term:
        preference = 'cute'
    elif 'classy' in search_term:
        preference = 'classy'
        
        
    # 나이 분류
    
    target_age_group = 'normal'  # 기본값
    if 'early 20s' in search_term:
        target_age_group = '20대 초반'
    elif 'mid-20s' in search_term:
        target_age_group = '20대 중반'
    elif 'late 20s' in search_term:
        target_age_group = '20대 후반'
    elif 'early 30s' in search_term:
        target_age_group = '30대 초반'
    elif 'mid-30s' in search_term:
        target_age_group = '30대 중반'
    elif 'late 30s' in search_term:
        target_age_group = '30대 후반'    
        
    return {
        'tpo': tpo,
        'weather_condition': weather_condition,
        'preference': preference,
        'target_age_group': target_age_group,
    }
    


        

        


def update_csv_with_categories():
    """CSV 파일에 카테고리 정보 추가"""
    # CSV 파일 경로
    csv_file = 'pinterestcrowling.csv'
    output_file = 'Coordinate.csv'  # 결과를 저장할 파일 경로
    
    if not os.path.exists(csv_file):
        print(f"CSV 파일을 찾을 수 없습니다: {csv_file}")
        return
    
    try:
        # CSV 파일 읽기
        df = pd.read_csv(csv_file)
        
        # 중복된 행 제거 및 인덱스 재설정
        df = df.drop_duplicates().reset_index(drop=True)

        # NaN 값 처리 (예: 빈 문자열로 대체)
        df['search_term'] = df['search_term'].fillna('')
        
        # 카테고리 컬럼이 없는 경우에만 추가
        if 'tpo' not in df.columns:
            # 검색어를 기반으로 카테고리 정보 추가
            categories = df['search_term'].apply(categorize_image)
            
            # 카테고리 정보를 개별 컬럼으로 분리
            df['tpo'] = categories.apply(lambda x: x['tpo'])
            df['weather_condition'] = categories.apply(lambda x: x['weather_condition'])
            df['preference'] = categories.apply(lambda x: x['preference'])
            df['target_age_group'] = categories.apply(lambda x: x['target_age_group'])

            # coordinate_id 추가 (1부터 시작하는 순차적 번호)
            df['coordinate_id'] = range(1, len(df) + 1)
            
            # image_url 컬럼을 coordinate_id와 tpo 사이에 추가
            df = df[['coordinate_id', 'image_url', 'tpo', 'weather_condition', 'preference', 'target_age_group']]
            
            # 업데이트된 데이터프레임을 Coordinate.csv 파일로 저장
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print("카테고리 정보가 성공적으로 추가되어 Coordinate.csv에 저장되었습니다.")
        else:
            print("이미 카테고리 정보가 존재합니다.")
            
    except Exception as e:
        print(f"CSV 파일 처리 중 오류 발생: {e}")

if __name__ == "__main__":
    update_csv_with_categories()


