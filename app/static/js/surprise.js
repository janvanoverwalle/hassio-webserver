window.onload = (event) => {
    if (!window.location.pathname.startsWith('/mystery')) {
        return;
    }

    handle_used_codes();

    if (document.getElementById('sliding-puzzle-figure-container')) {
        sliding_puzzle_game();
    }
}

//#region Used codes
function clear_used_codes() {
    localStorage.removeItem('used_codes');

    const el = document.getElementById("used-codes-container");
    if (el) {
        el.remove();
    }
}

function handle_used_codes() {
    const surprise_code = document.getElementById('surprise-code');
    if (surprise_code) {
        handle_new_code(surprise_code.textContent);
    }

    const container = document.getElementById('used-codes-list');
    if (container) {
        handle_used_codes_list(container);
    }
}

function handle_new_code(code) {
    var used_codes = localStorage.getItem('used_codes');
    used_codes = used_codes ? JSON.parse(used_codes) : [];

    if (!used_codes.includes(code)) {
        console.log('Caching code: ' + code);
        used_codes.push(code);
    }

    localStorage.setItem('used_codes', JSON.stringify(used_codes));
}

function handle_used_codes_list(container) {
    var used_codes = localStorage.getItem('used_codes');
    if (!used_codes) {
        const el = document.getElementById("used-codes-container");
        if (el) {
            el.remove();
        }
        return;
    }

    used_codes = JSON.parse(used_codes);
    //used_codes.sort();
    for (code of used_codes) {
        const span = document.createElement('span');
        span.classList.add('surprise-code');
        span.textContent = code;

        const a = document.createElement('a');
        a.classList.add('ml-4', 'h5');
        a.href = '/mystery/' + code;
        a.appendChild(span);

        const li = document.createElement('li');
        li.classList.add('mt-2');
        li.appendChild(a);

        container.appendChild(li);
    }

    const el = document.getElementById("used-codes-container");
    if (el) {
        el.classList.remove('invisible');
    }
}
//#endregion

//#region Sliding puzzle
function sliding_puzzle_game() {
    // Source: https://github.com/danishmughal/sliding-puzzle

    // Data structure to hold positions of tiles
    var parentX = document.querySelector(".sliding-puzzle").clientHeight;
    var baseDistance = 33.8;
    var tileMap = {
        1: {
            tileNumber: 1,
            position: 1,
            top: 0,
            left: 0
        },
        2: {
            tileNumber: 2,
            position: 2,
            top: 0,
            left: baseDistance * 1
        },
        empty: {
            tileNumber: 3,
            position: 3,
            top: 0,
            left: baseDistance * 2
        },
        4: {
            tileNumber: 4,
            position: 4,
            top: baseDistance,
            left: 0
        },
        5: {
            tileNumber: 5,
            position: 5,
            top: baseDistance,
            left: baseDistance
        },
        6: {
            tileNumber: 6,
            position: 6,
            top: baseDistance,
            left: baseDistance * 2
        },
        7: {
            tileNumber: 7,
            position: 7,
            top: baseDistance * 2,
            left: 0
        },
        8: {
            tileNumber: 8,
            position: 8,
            top: baseDistance * 2,
            left: baseDistance
        },
        9: {
            tileNumber: 9,
            position: 9,
            top: baseDistance * 2,
            left: baseDistance * 2
        }
    }

    // Array of tileNumbers in order of last moved
    var history = [];

    // Movement map
    function movementMap(position) {
        if (position == 9) return [6, 8];
        if (position == 8) return [5, 7, 9];
        if (position == 7) return [4, 8];
        if (position == 6) return [3, 5, 9];
        if (position == 5) return [2, 4, 6, 8];
        if (position == 4) return [1, 5, 7];
        if (position == 3) return [2, 6];
        if (position == 2) return [1, 3, 5];
        if (position == 1) return [2, 4];
    }

    // Board setup according to the tileMap
    document.querySelector('#shuffle').addEventListener('click', shuffle, true);
    document.querySelector('#solve').addEventListener('click', solve, true);
    var tiles = document.querySelectorAll('.tile');
    var delay = 0;
    for (var i = 0; i < tiles.length; i++) {
        tiles[i].addEventListener('click', tileClicked, true);

        setTimeout(setup, delay, tiles[i]);
        delay += 50;
    }
    //setTimeout(shuffle, delay, 30);

    function setup(tile) {
        var tileId = tile.getAttribute("value");
        // tile.style.left = tileMap[tileId].left + '%';
        // tile.style.top = tileMap[tileId].top + '%';
        var factor = 100;
        var xMovement = parentX * (tileMap[tileId].left / factor);
        var yMovement = parentX * (tileMap[tileId].top / factor);
        var translateString = "translateX(" + xMovement + "px) " + "translateY(" + yMovement + "px)"
        tile.style.webkitTransform = translateString;
        recolorTile(tile, tileId);
    }

    function tileClicked(event) {
        moveTile(event.target);

        if (checkSolution()) {
            puzzleSolved();
        }
    }

    var solved = false;
    function puzzleSolved(timeout) {
        if (solved) {
            return;
        }

        var tiles = document.querySelectorAll('.tile');
        for (var i = 0; i < tiles.length; i++) {
            tiles[i].removeEventListener('click', tileClicked);
        };

        timeout = timeout === undefined ? 500 : timeout;
        setTimeout(() => {
            document.getElementById("audio-player").play();
        }, timeout);

        setTimeout(() => {
            var elements = document.getElementsByClassName("flip-box-inner");
            elements[0].style.webkitTransform = "rotateY(180deg)";
        }, timeout + 10 * 1000);

        solved = true;
    }

    // Moves tile to empty spot
    // Returns error message if tile cannot be moved
    function moveTile(tile, recordHistory = true) {
        // Check if Tile can be moved 
        // (must be touching empty tile)
        // (must be directly perpendicular to empty tile)
        var tileNumber = tile.getAttribute("value");
        if (!tileMovable(tileNumber)) {
            console.log("Tile " + tileNumber + " can't be moved.");
            return;
        }

        // Push to history
        if (recordHistory == true) {
            if (history.length >= 3) {
                if (history[history.length - 1] != history[history.length - 3]) {
                    history.push(tileNumber);
                }
            } else {
                history.push(tileNumber);
            }
        }

        // Swap tile with empty tile
        var emptyTop = tileMap.empty.top;
        var emptyLeft = tileMap.empty.left;
        var emptyPosition = tileMap.empty.position;
        tileMap.empty.top = tileMap[tileNumber].top;
        tileMap.empty.left = tileMap[tileNumber].left;
        tileMap.empty.position = tileMap[tileNumber].position;

        // tile.style.top = emptyTop  + '%'; 
        // tile.style.left = emptyLeft  + '%';

        var factor = 100;
        var xMovement = parentX * (emptyLeft / factor);
        var yMovement = parentX * (emptyTop / factor);
        var translateString = "translateX(" + xMovement + "px) " + "translateY(" + yMovement + "px)"
        tile.style.webkitTransform = translateString;

        tileMap[tileNumber].top = emptyTop;
        tileMap[tileNumber].left = emptyLeft;
        tileMap[tileNumber].position = emptyPosition;

        recolorTile(tile, tileNumber);
    }

    // Determines whether a given tile can be moved
    function tileMovable(tileNumber) {
        var selectedTile = tileMap[tileNumber];
        var emptyTile = tileMap.empty;
        var movableTiles = movementMap(emptyTile.position);
        return movableTiles.includes(selectedTile.position);
    }

    // Returns true/false based on if the puzzle has been solved
    function checkSolution() {
        if (tileMap.empty.position !== 3) {
            return false;
        }

        for (var key in tileMap) {
            if (key == 1 || key == 9) {
                continue;
            }

            var prevKey = key == 4 ? "empty" : key == "empty" ? 2 : key-1;
            if (tileMap[key].position < tileMap[prevKey].position) {
                return false;
            }
        }

        // Clear history if solved
        history = [];
        return true;
    }

    // Check if tile is in correct place!
    function recolorTile(tile, tileId) {
        if (tileId == tileMap[tileId].position) {
            tile.classList.remove("error");
        } else {
            tile.classList.add("error");
        }
    }

    // Shuffles the current tiles
    shuffleTimeouts = [];
    function shuffle(iterations) {
        clearTimers(shuffleTimeouts);

        var durations = [];
        tiles.forEach(t => {
            durations.push(t.style.transitionDuration);
            t.style.transitionDuration = "10ms";
        })
        clearTimers(solveTimeouts);
        shuffleLoop();

        iterations = iterations === undefined ? 20 : iterations;
        var shuffleStep = 100;
        var shuffleDelay = shuffleStep;
        var shuffleCounter = 0;
        while (shuffleCounter < iterations) {
            shuffleDelay += shuffleStep;
            shuffleTimeouts.push(setTimeout(shuffleLoop, shuffleDelay));
            shuffleCounter++;
        }

        setTimeout(() => {
            durations.reverse();
            tiles.forEach(t => {
                t.style.transitionDuration = durations.pop();
            })
        }, shuffleDelay+shuffleStep);
    }

    var lastShuffled;

    function shuffleLoop() {
        var emptyPosition = tileMap.empty.position;
        var shuffleTiles = movementMap(emptyPosition);
        var tilePosition = shuffleTiles[Math.floor(Math.floor(Math.random() * shuffleTiles.length))];
        var locatedTile;
        for (var i = 1; i <= 9; i++) {
            if (i == tileMap.empty.tileNumber) {
                continue;
            }
            if (tileMap[i].position == tilePosition) {
                var locatedTileNumber = tileMap[i].tileNumber;
                if (locatedTileNumber >= tileMap.empty.tileNumber) {
                    locatedTileNumber--;
                }
                locatedTile = tiles[locatedTileNumber - 1];
            }
        }

        if (lastShuffled != locatedTileNumber) {
            moveTile(locatedTile);
            lastShuffled = locatedTileNumber;
        } else {
            shuffleLoop();
        }
    }

    function clearTimers(timeoutArray) {
        for (var i = 0; i < timeoutArray.length; i++) {
            clearTimeout(timeoutArray[i])
        }
    }

    // Temporary function for solving puzzle.
    // To be reimplemented with a more sophisticated algorithm
    solveTimeouts = []
    function solve() {
        clearTimers(shuffleTimeouts);
        clearTimers(solveTimeouts);

        var timeout = 0;
        var repeater = history.length;
        for (var i = 0; i < repeater; i++) {
            timeout = i * 100;
            var tileNumber = history.pop();
            if (tileNumber >= tileMap.empty.tileNumber) {
                tileNumber--;
            }
            var tile = tiles[tileNumber - 1];
            solveTimeouts.push(setTimeout(moveTile, timeout, tile, false));
        }
        puzzleSolved(timeout+500);
    }
}
//#endregion
