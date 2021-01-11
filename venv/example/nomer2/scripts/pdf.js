let pdfE = document.querySelector('.pdf').addEventListener('click', getPdf);
let pdfEl = document.querySelector('.load__pdf')


function getPdf () {
    pdfEl.classList.remove('pdf__hide');
    data = {
        'link': window.location.href
    };
    axios
    .post('https://bsl-show.online/bot-data/pdf.php' , data)
    .then(response => {
        pdfEl.classList.add('pdf__hide');
        window.location = response.data['link'];
    })
    .catch((e) => console.log(e));
}