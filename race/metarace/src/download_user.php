<?php
    // Start the session
    session_start();

    $file = "user.bak";
    $data = $_SESSION['user'];
    // echo $data;
    $sData = serialize($data);
    header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="replay"');
    header('Cache-Control: must-revalidate');
    header('Pragma: public');
    // header('Content-Length: ' . sizeof($sData));
    echo $sData;
?>