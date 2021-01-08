
function valid() {
    let ta = document.querySelector('textarea').value.length;
    if(ta > 4) {
        request()
    } else {
        console.log('no');
        return;
    }
}


function request() {

    let nm = document.querySelector('.header__name').textContent;
    let gos = document.querySelector('.reg2__reg22').textContent;

    let url = 'http://bsl-show.online/bot-data/comments.php';
    let data =  {
        "name": '',
        "reg" : '',
        "date": '' ,
        "text": ' ', 
    } ;

    //поле ввода для мыло
    //поле ввода для имя
    //поле ввода для телефона


    let elem = document.querySelectorAll("form");
        elem.forEach((e)=> {
               e.querySelectorAll('textarea').forEach((input) => {
                   for(let props in data) {
                      if(input.name == 'text' && props == 'text') {
                          console.log(input.value.length);
                            if(input.value.length > 4) {
                               data[props] = input.value;
                            } else {
                                return;
                            }
                        }
                   }
               });
        });
        
        data.name = nm;
        data.reg = gos;

        console.log(data);

        axios
        .post(url , data)
        .then(response => {
            if(!localStorage.getItem('test')) {
                console.log(response);
                document.querySelector('.comments__column').innerHTML = "";
                rower(response.data);
                localStorage.test = 2;
                console.log(localStorage.test);
            } else {
                alert('no')
            }
        })
        .catch((e) => console.log(e));
  

}

