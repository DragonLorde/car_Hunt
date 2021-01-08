let doc = document.querySelectorAll('.show');


for(let prop of doc) {
    prop.addEventListener('click' , (e) => {
        //let showis = e.path[1].querySelector('.hide-s1');
        let shw = e.composedPath()[1].querySelector('.av__hide');
        shw.classList.toggle('hide-s1')
    });
}