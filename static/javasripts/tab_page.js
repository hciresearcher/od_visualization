document.addEventListener("DOMContentLoaded", function() {
    // 페이지 로드가 완료된 후 실행될 코드
  
    // 탭 네비게이션의 모든 탭 요소를 가져옵니다.
    var tabs = document.querySelectorAll('.tabnav li a');
  
    // 탭 내용의 모든 요소를 가져옵니다.
    var tabContents = document.querySelectorAll('.tabcontent > div');
  
    // 탭1에 대해 초기 활성화를 설정합니다.
    tabs[0].parentElement.classList.add('active');
    tabContents[0].classList.add('active');
  
    // 각 탭에 대해 클릭 이벤트를 추가합니다.
    tabs.forEach(function(tab) {
        tab.addEventListener('click', function(event) {
            event.preventDefault(); // 링크의 기본 동작을 방지합니다.
  
            // 현재 활성화된 탭이라면 아무 것도 하지 않습니다.
            if (tab.parentElement.classList.contains('active')) {
                return;
            }
  
            // 모든 탭에 active 클래스를 제거합니다.
            tabs.forEach(function(item) {
                item.parentElement.classList.remove('active');
            });
  
            // 클릭된 탭에 active 클래스를 추가합니다.
            tab.parentElement.classList.add('active');
  
            // 클릭된 탭의 href 속성 값을 가져옵니다.
            var targetId = tab.getAttribute('href');
  
            // 모든 탭 내용을 숨깁니다.
            tabContents.forEach(function(content) {
                content.classList.remove('active');
            });
  
            // 클릭된 탭에 해당하는 탭 내용을 표시합니다.
            document.querySelector(targetId).classList.add('active');

        });
    });
  });
