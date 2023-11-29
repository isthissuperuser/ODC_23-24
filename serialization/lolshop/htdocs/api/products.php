<?php
header('Content-Type: application/json');

require_once '../config.inc.php';

$products = $db->getAvailableProducts();

$a = array();
foreach($products as $p) {
    array_push($a, $p->toDict());
}

echo json_encode(array("products" => $a), JSON_PRETTY_PRINT | JSON_NUMERIC_CHECK);

?>
