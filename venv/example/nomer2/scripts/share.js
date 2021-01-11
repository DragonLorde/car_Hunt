let currentLocation = window.location;
let inputLink = document.querySelector('.link').value = currentLocation; 

let input_rep = document.querySelector('.rep');
let input_bot = document.querySelector('.bt');

let btnShows = document.querySelector('.show__share-rep');

let clos = document.querySelector('.close');
shows = document.querySelector('.share');


let btn_rep = document.querySelector('.report').addEventListener('click' , (e) => {
    input_rep.select();
    document.execCommand("copy");
    e.target.classList.add('al')
    e.target.classList.remove('bt__tt');
    e.target.textContent = 'Скопированно!'
});

let btn_bot = document.querySelector('.bot').addEventListener('click' , (e) => {
    input_bot.select();
    document.execCommand("copy");
    e.target.classList.add('al')
    e.target.textContent = 'Скопированно!'
});

clos.addEventListener('click' , () => {
    shows.classList.toggle('close__hide-slide');
})

btnShows.addEventListener('click' , () => {
    shows.classList.toggle('close__hide-slide');
    console.log('asfasfasf');
});
