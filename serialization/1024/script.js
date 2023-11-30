document.addEventListener('DOMContentLoaded', () => {

  let size = 4;
  let name = "Player"
  const canvas = document.getElementById("canvas");
  const movelist = document.getElementById("movelist");
  const rankinglist = document.getElementById("ranking");
  const scoreLabel = document.getElementById("score");
  const restartBtn = document.getElementById("restart");
  const sizeBox = document.getElementById("size")
  const nameBox = document.getElementById("name")

  const ctx = canvas.getContext("2d");
  const colors = {
    0: "#EEEEEE",
    2: "#D6CDC4",
    4: "#f7e3b7",
    8: "#F2B179",
    16: "#F58360",
    32: "#F65E3B",
    64: "#F6501C",
    128: "#EDC850",
    256: "#506EE5",
    512: "#63BAF1",
    1024: "#20DDB1",
    2048: "#333333"
  };
  const winScore = 1024;

  let tiles = [];
  let actions = [];
  let ranking = [];
  let width = canvas.width / size - 6;
  let score = 0;
  let failed = false;
  let fontSize;
  let c = 0;

  ///////////////

  // Restart
  $("#restart").click(ev => {
    failed = false;
    start();
  });


  //// DRAW ////

  $("#size").change(e => {
    size = parseInt(sizeBox.value);
    width = canvas.width / size - 6;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    failed = false;
    start()
    failed = false;
  });

  $("#name").change(e => {
    name = nameBox.value;
  });

  /**
   * Draw tile
   * @function
   * @param {object} - Tile object
   */
  function draw(tile) {
    ctx.beginPath()
    ctx.rect(tile.x, tile.y, width, width) // Define rectangle

    ctx.fillStyle = colors[tile.value];

    ctx.fill(); // Draw tile
    ctx.strokeStyle = "#FFF";
    ctx.strokeRect(tile.x, tile.y, width, width)

    if (tile.value) { // Check if there is a number (not 0)
      fontSize = width / 2.7;
      ctx.font = fontSize + "px Arial"
      ctx.fillStyle = "#FFFFFF"
      ctx.textAlign = "center"

      // Put value inside tile at center
      ctx.fillText(tile.value, tile.x + width / 2, tile.y + width / 1.6)
    }
  }

function drawMoveList(){
  movelist.innerHTML = ""
  l = actions.length-1;
  for (var move in actions) {
    movelist.innerHTML+= actions[l-move] + "<br/>"
  }
}

function drawRanking(){
  rankinglist.innerText = ""
  for (var r in ranking) {
    rankinglist.innerText+= r+" - ["+ ranking[r].score +"] "+ranking[r].name + "\n"
  }
}

  /**
   * Redraw all tiles
   * @function
   */
  function drawAll() {
    let left = 0;

    for (let row = 0; row < size; row++) {
      for (let col = 0; col < size; col++) {
        draw({
          "value": tiles[row][col],
          "x": col * width + 5 * (col + 1),
          "y": row * width + 5 * (row + 1)
        });

        if (tiles[row][col] == winScore) return won();

        if (slide(tiles, "up", true)) left++;
        else if (slide(tiles, "down", true)) left++;
        else if (slide(tiles, "right", true)) left++;
        else if (slide(tiles, "left", true)) left++;
      }
    }

    if (!left) return fail();

    scoreLabel.innerHTML = score;
    drawMoveList();
    drawRanking();
  }

  /**
   * Put new tile to the random place
   * @function
   */
  function randomTile() {
    while (true) {
      let row = random(size);
      let col = random(size);

      if (!tiles[row][col]) {
        let val = Math.random() > 0.8 ? 4 : 2;

        tiles[row][col] = val;
        drawAll();

        break;
      }
    }
  }


  //// MOVE ////

  /**
   * Gestures and keyboard handler
   * @function
   */
  function move() {
    let mc = new Hammer.Manager(canvas);
    let gesture = new Hammer.Swipe();

    mc.add([gesture]);

    mc.on("swipeleft swiperight swipeup swipedown", (ev) => {
      if (failed) return;
      switch (ev.type.slice(5)) {
        case "up":
          rSlide("up");
          break;
        case "down":
          rSlide("down");
          break;
        case "right":
          rSlide("right");
          break;
        case "left":
          rSlide("left");
          break;
      }

    });

    $(document).keydown((e) => {
      if (failed) return;

      if (e.keyCode === 37) rSlide("left");
      if (e.keyCode === 39) rSlide("right");
      if (e.keyCode === 38) rSlide("up");
      if (e.keyCode === 40) rSlide("down");

    });

    // TODO: Rewrite drawing at page load to put previous
    //       data from localStorage to tiles and etc.

    // if (storageAvailable('localStorage')) {
    //   let settings = {
    //     "tiles": tiles,
    //     "size": size,
    //     "score": score
    //   }
    //
    //   localStorage.setItem(settings)
    // } else {
    //   if (!c)
    //     console.warn("Browser does not support 'localStorage', then no data would be saved."),
    //     c++;
    // }
  }

  function updateRanking(){
    axios.get('/game.php', {params: {"action": "getRanking"}})
      .then(function (response) {
        // handle success
        ranking = response.data.ranking;
        drawAll();
        console.log(response.data);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .then(function () {
        // always executed
      });

  }

  function rSlide(direction){
    axios.get('/game.php', {params: {"action": direction}})
      .then(function (response) {
        // handle success
        tiles = response.data.gameBoard;
        score = response.data.score;
        actions = response.data.actions;
        drawAll();
        console.log(response.data);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .then(function () {
        // always executed
      });
    updateRanking();
  }

  /**
   * Get object from matrix
   * @function
   * @param {number} i - Row/Col
   * @param {number} j - Row/Col
   * @param {string} direction - Direction (see {@link slide})
   */
  function getTile(i, j, direction) {
    switch (direction) {
      case "left":
        return tiles[i][j];
      case "right":
        return tiles[i][size - 1 - j];
      case "up":
        return tiles[j][i];
      case "down":
        return tiles[size - 1 - j][i];
    }
  }

  /**
   * Set object to matrix
   * @function
   * @param {number} i - Row/Col
   * @param {number} j - Row/Col
   * @param {string} direction - Direction (see {@link slide})
   * @param {number} value - Value to set
   */
  function setTile(i, j, direction, value) {
    switch (direction) {
      case "left":
        tiles[i][j] = value;
        break;
      case "right":
        tiles[i][size - 1 - j] = value;
        break;
      case "up":
        tiles[j][i] = value;
        break;
      case "down":
        tiles[size - 1 - j][i] = value;
        break;
    }
  }

  /**
   * Slide and combine function for matrix
   * @function
   * @param {array} rows - Matrix
   * @param {string} direction - Direction to slide (left, up, right, down)
   */
  function slide(tiles, direction, check) {
    let moved = false;

    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        // Find non-empty tile
        let k = j + 1;
        while (k < size && !getTile(i, k, direction)) {
          k++;
        }
        if (k == size)
          continue;

        // k < size && tiles[i][k]
        if (getTile(i, j, direction) == getTile(i, k, direction)) {
          if (check) return true;

          setTile(i, j, direction, getTile(i, j, direction) * 2);
          setTile(i, k, direction, 0);

          score += getTile(i, j, direction);
          moved = true;
        } else if (getTile(i, j, direction) == 0) {
          if (check) return true;

          setTile(i, j, direction, getTile(i, k, direction));
          setTile(i, k, direction, 0);

          // Stay on the same tile!
          j--;
          moved = true;
        }
      }
    }

    if (moved) randomTile();
  }

  /**
   * Start
   * @function
   */
  function start() {
    canvas.style.opacity = 1;
    score = 0;
    scoreLabel.innerHTML = score;

    axios.get('/game.php', {params: {"action": "initGameBoard", "size": size, "name": name}})
      .then(function (response) {
        // handle success
        tiles = response.data.gameBoard;
        score = response.data.score;
        actions = response.data.actions;
        drawAll();
        console.log(response.data);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      })
      .then(function () {
        // always executed
      });

  }

  /**
   * On failing
   * @function
   */
  function fail() {
    failed = true;
    canvas.style.opacity = 0.5;
    console.log("FAILED")
  }

  /**
   * On winning
   * @function
   */
  function won() {
    failed = true;
    canvas.style.opacity = 0.2;
    console.log("Well done!")
  }

  //// UTILS ////

  /**
   * Get random number from 0 to "end"
   * @function
   * @param {number} end - End of random numbers
   */
  function random(end) {
    return Math.floor(Math.random() * end);
  }

  /**
   * Check that storage is avaliable in client browser
   * @function
   * @param {number} type - Type of storage, e.g. 'localStorage'
   */
  function storageAvailable(type) {
    try {
      var storage = window[type],
        x = '__test__';
      storage.setItem(x, x);
      storage.removeItem(x);
      return true;
    } catch (e) {
      return e instanceof DOMException && (
          e.code === 22 ||
          e.code === 1014 ||
          e.name === 'QuotaExceededError' ||
          e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
        storage.length !== 0;
    }
  }

  ///////////////

  start();
  move();

});
