<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT, DELETE');
header('Access-Control-Allow-Headers: X-Requested-With,Origin,Content-Type,Cookie,Accept');
header('Content-type: application/json'); 


$link = json_decode(file_get_contents('php://input'), true);



$pdf_link = file_get_contents('https://api.html2pdf.app/v1/generate?url='. $link['link'] . '&apiKey=wYSOkiicp66P70ukkgayvbUoF8tQ9oqWi8Caj7aJpchJZPTiAJXPx7qLXZZTt63I');
$id = uniqid();

file_put_contents($id . '.pdf', $pdf_link);

echo json_encode( array( "link" => 'http://bsl-show.online/bot-data/' . $id . '.pdf' ) );










?>