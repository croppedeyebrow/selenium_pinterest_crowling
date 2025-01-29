#사이드 프로젝트 데이터 수집용 크롤링 파이썬 레포

##Selenium, schedule, pandas_csv 활용

###주의사항
<span style="color:red">
<b>
핀터레스트 로그인 정보는 본인의 정보로 입력해야 합니다.
크롤링 대상 키워드는 본인이 원하는 키워드로 입력해야 합니다.(영어 검색어)
</b>

</span>

<span style="color:orange">
<b>
핀터레스트는 본질적으로 크롤링을 방지하는 기능을 가지고 있습니다.
따라서, 너무 짧은 주기는 피하고 한번에 많이 불러온 후 주기를 넓히거나 다양한 아이디를 활용하시길
</b>

</span>
</br>
</br>
<span style="color:blue">
<b>
파일 수집 내용 : img_url,  img_filename, search_term, crawled_at // img_filename은 폴더에 따로 저장.!
</b>
</br>
<b>
파일 수집 목적 : 패션 코디 이미지 추출해서, 추후 전처리용 raw data로 활용
</b>
</br>
<b>
파일 수집 후 전처리 : 검색어에서 키워드 추출해서, 키워드에 맞는 컬럼으로 재배치.
</b>

</span>
