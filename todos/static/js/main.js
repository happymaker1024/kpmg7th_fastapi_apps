// textarea에 공백일 경우 경고창 띄우기
let task = document.getElementById("task");
let add_task = document.getElementById("add_task")
add_task.addEventListener("click", (e) =>{
  if (task.value == "") {
    alert("입력한 TODO가 없습니다.");
    // submit 방지함
    e.preventDefault();
    return false;
  }
})