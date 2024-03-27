//클릭 이벤트 연결
$(".Check").click(function () {
    //방금 클릭한 dom의 id값 가져오기
   let checkedId = $(this).attr("id");
   //방금 클릭한 dom의 name값 가져오기
   let checkedName = $(this).attr("name");
   //방금 클릭한 dom의 class값 가져오기
   let checkedClass = $(this).attr("class"); 
   
   //id로 요소 선택하여 check여부 컨트롤
   document.getElementById(checkedId).checked=true;
   //class 이름으로 요소(들) 선택하여 check여부 컨트롤
   document.getElementsByClassName(checkedClass).checked=false;
   //Name으로 요소(들) 선택하여 check여부 컨트롤
   document.getElementsByName(checkedName).checked=false;
});