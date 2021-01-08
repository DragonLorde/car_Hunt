let showBtn = document.querySelector('.com__btn');
let comments = document.querySelector('.comments__column')
let reg = document.querySelector('.reg2__reg22');
let col = document.querySelector('.comments__column');

showBtn.addEventListener('click', (e) => {
    showBtn.classList.toggle('com__hide');
    comments.classList.toggle('com__hide');
    GetData(reg);
});

async function GetData(regNmbr) {

    axios.get('http://bsl-show.online/bot-data/comments.php?reg=' + regNmbr.textContent)
    .then(function (response) {
        rower(response.data);
    })
}


function rower(data) {
    reg.insertAdjacentElement
    for(let i = 0; i <= data.length; i++) {
        col.insertAdjacentHTML("afterbegin", 
        `<div class='comments__row'>  
        <p class='comments__name'>💬 ${data[i]['name']} 
        <span class='comments__date'> ${data[i]['date']} </span> </p>
        <p class='comments__text'> ${data[i]['text']} </p>
        </div>
        `)
    }
}