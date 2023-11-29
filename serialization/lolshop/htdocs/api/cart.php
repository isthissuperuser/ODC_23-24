<?php
header('Content-Type: application/json');

require_once '../config.inc.php';

if(isset($_REQUEST['token'])) {

    $state = $db->retrieveState($_REQUEST['token']);
    if(!$state) {
        http_response_code(400);
    } else {
        echo $state;
    }

} else if(isset($_REQUEST['state'])) {

    $state = State::restore($_REQUEST['state']);

    $enc = json_encode($state->toDict(), JSON_PRETTY_PRINT | JSON_NUMERIC_CHECK);

    if(isset($_REQUEST['save'])) {
        $tok = $db->saveState($enc);
        if(!$tok) {
            http_response_code(400);
        } else {
            echo json_encode(array("token" => $tok));
        }
    } else {
        echo $enc;
    }

} else {
    http_response_code(400);
}

?>
