<?php



if($_GET['regHx']) {
    $reg = $_GET['regHx'];
    echo json_encode(array('hex'=>bin2hex($reg)));
} else {
    $reg = $_GET['regBin'];
    echo json_encode(array('bin'=>hex2bin($reg)));
}
?>