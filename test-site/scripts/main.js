let myButton = document.querySelector('button');
let myHeading = document.querySelector('h1');


function setUserName() {
  let myName = prompt('请输入你的名字。');
  if(!myName) {} else {
    //localStorage.setItem('name', myName);
    myHeading.textContent = 'Hi, ' + myName;
	}
}
myButton.onclick = function() {
   setUserName();
}
/*
if(!localStorage.getItem('name')) {
  setUserName();
} else {
  let storedName = localStorage.getItem('name');
  myHeading.textContent = 'Hi, ' + storedName;
}
*/