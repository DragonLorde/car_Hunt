<?php

$dat = $_GET['date'];

function dateCar($prop) {
    $dif = strtotime(date("y.m.d")) - strtotime($prop) ;
    return floor($dif / (60*60*24*365));
}

$res = dateCar($dat);
echo json_encode(array('date' => $res));    

?>