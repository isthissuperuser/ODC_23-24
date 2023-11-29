<?php
header('Content-Type: application/json');

require_once('../config.inc.php');

if(isset($_REQUEST['state']) && isset($_REQUEST['product'])) {
    $state = State::restore($_REQUEST['state']);
    $state->addToCart($_REQUEST['product']);

    echo json_encode(array(
        'session_id' => $state->getSessionID(),
        'state' => $state->save()
    ), JSON_PRETTY_PRINT);

} else {
    http_response_code(400);
}

?>
