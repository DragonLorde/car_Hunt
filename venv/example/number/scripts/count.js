avito = document.querySelectorAll('.avito__row').length;
ul = document.querySelectorAll('.ul__row').length;
drom = document.querySelectorAll('.drom__row').length;


av = document.querySelectorAll('.av__row').length;




count = document.querySelectorAll('.banner p span');

count[0].innerText = avito + ul + drom;
count[1].innerText = av + drom;