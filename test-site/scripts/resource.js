let myImage = document.querySelector('section img');
let myButton = document.querySelector('button');
let myHeading = document.querySelector('h1');

myImage.onclick = function(){
	let mySrc = myImage.getAttribute('src');
	if(mySrc === 'images/dog1.png'){
		myImage.setAttribute('src', 'images/dog2.png');
	}else{
		myImage.setAttribute('src', 'images/dog1.png');
	}
}

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