const list = document.createElement('ul');
const info1 = document.createElement('p');
const info2 = document.createElement('p');
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

info1.textContent = 'Below is a dynamic list. Click on this paragraph to add a new list item to annotate some information. Click an existing list item to change its text to something else.';
info2.textContent = '（单击此段落添加一个新的列表项以注释某些信息 / 单击现有列表项将其文本更改为其他内容）';

document.body.appendChild(info1);
document.body.appendChild(info2);
document.body.appendChild(list);

info1.onclick = function() {
  const listItem = document.createElement('li');
  const listContent = prompt('What content do you want the list item to have?');
  if(!listContent){} else {
	listItem.textContent = listContent;
	list.appendChild(listItem);
  }

  listItem.onclick = function(e) {
    e.stopPropagation();
    const listContent = prompt('Enter new content for your list item');
    this.textContent = listContent;
  }
}

info2.onclick = function() {
  const listItem = document.createElement('li');
  const listContent = prompt('What content do you want the list item to have?');
  if(!listContent){} else {
	listItem.textContent = listContent;
	list.appendChild(listItem);
  }

  listItem.onclick = function(e) {
    e.stopPropagation();
    const listContent = prompt('Enter new content for your list item');
    this.textContent = listContent;
  }
}