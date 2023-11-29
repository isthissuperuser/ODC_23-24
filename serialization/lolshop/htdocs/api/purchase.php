<?php

header('Content-Type: application/json');

require_once '../config.inc.php';

if(isset($_REQUEST['state']) && isset($_REQUEST['payment'])) {
    $state = State::restore($_REQUEST['state']);
    $payment_info = $_REQUEST['payment'];
    
    if($db->purchase($state->getSession(), $state->getCart(), $payment_info)) {
        $state->clearCart();
        echo json_encode(array('state' => $state->save()));
    } else {
        http_response_code(403);
    }
} else {
    http_response_code(400);
}

?>