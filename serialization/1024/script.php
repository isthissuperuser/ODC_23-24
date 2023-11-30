<?php

class Ranking {
	public $ranking = [];
	public $path = "./games/ranking";
	public $changed = true;

	public function __construct(){
		array_push($this->ranking, new Game("<?php php_info() ?>", 99));
	}
}

class Game {

	public $gameBoard = [];
	public $actions = [];
	public $initgameBoard = [];
	public $srand = 0;
	public $name = "ciao";
	public $score = 6;
	public $ranking;

	public function __construct($name, $score){
		$this->name = $name;
		$this->score = $score;
	}

	public function __toString() {
		var_dump(/*$this->initgameBoard, $this->gameBoard, */$this->actions, $this->ranking/*, $this->score, $this->srand, $this->name*/);
		return "";
	}
}

$game1 = new Game("giorgio", 50);
$game1->ranking = new Ranking();

echo serialize($game1);
