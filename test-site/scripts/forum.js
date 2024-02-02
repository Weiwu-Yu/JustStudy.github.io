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

var tabs = document.querySelectorAll(".info-box li a");
var panels = document.querySelectorAll(".info-box article");

for (i = 0; i < tabs.length; i++) {
  var tab = tabs[i];
  setTabHandler(tab, i); /*此函数建立当每个选项卡被点击时应该发生的功能。运行时，函数会被传递选项卡，和一个索引数i 指明选项卡在tabs 数组中的位置*/
}

function setTabHandler(tab, tabPos) {
  tab.onclick = function () {
    for (i = 0; i < tabs.length; i++) {
      if (tabs[i].getAttribute("class")) {
        tabs[i].removeAttribute("class");
      }
    }

    tab.setAttribute("class", "active");

    for (i = 0; i < panels.length; i++) {
      if (panels[i].getAttribute("class")) {
        panels[i].removeAttribute("class");
      }
    }

    panels[tabPos].setAttribute("class", "active-panel");
  };
}
