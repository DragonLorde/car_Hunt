let showBtn = document.querySelector('.com__btn');
let comments = document.querySelector('.comments__column')
let reg = document.querySelector('.header__vins');
let col = document.querySelector('.comments__column');
let loader = document.querySelector('.com__mm');


showBtn.addEventListener('click', (e) => {
        GetData(reg);
        showBtn.removeEventListener('click',(e) => {GetData(reg);} , false);
});

async function GetData(regNmbr) {
    loader.classList.toggle('com__hide')
    await axios.get('https://bsl-show.online/bot-data/comments.php?reg=' + regNmbr.textContent)
    .then(function (response) {
        loader.classList.toggle('com__hide')
        comments.classList.remove('com__hide') 
        rower(response.data)
        showBtn.classList.add('com__hide');
    })
}


function rower(data) {
    for(let prop of data) {
        col.insertAdjacentHTML("afterbegin", 
        `<div class='comments__row'>  
        <p class='comments__name'>💬 ${prop.name} : <span class='comments__date'> 
        ${prop['date']} </span> </p>
        <p class='comments__text'> ${prop['text']} </p>
        </div>
        `);
    }
}