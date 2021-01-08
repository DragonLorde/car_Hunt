<?php

$yer = $_GET['date'];

function dateCar($prop) {
    $dif = strtotime(date("y.m.d")) - strtotime($prop) ;
    return floor($dif / (60*60*24*365));
}

$res = dateCar($yer);
function gen($yr , $yr2) {
    $milArr = [];
    $prevDate = date("M-d-Y", mktime(0, 0, 0, rand(1 , 12), rand(1 , 28), $yr2 ));
    $prev = rand(15000 , 18000);
    for($i = 0; $i < $yr; $i += 2) {
        $prev = rand($prev , $prev *= 2);
        $milArr[] = array( "date" => $prevDate , "mileage" => $prev);
        $prevDate = date("M-d-Y", mktime(0, 0, 0, rand(1 , 12), rand(1 , 28), $yr2 + $i + 2 ));
    }
    echo json_encode(array('mile' => $milArr));
}
gen($res , $yer);

?>