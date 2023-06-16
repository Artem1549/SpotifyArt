let features = [0.38, 0.2, 0.72, 0.0, 0.7];
let acousticness = features[0];
let danceability = features[1];
let energy = features[2]; // represeted by the amount of colours
let instrumentalness = 1 - features[3];
let valence = features[4]; // represented by the colours of the art pieces
const alphabet = [
  "a",
  "b",
  "c",
  "d",
  "e",
  "f",
  "g",
  "h",
  "i",
  "j",
  "k",
  "l",
  "m",
  "n",
  "o",
  "p",
  "q",
  "r",
  "s",
  "t",
  "u",
  "v",
  "w",
  "x",
  "y",
  "z",
];

let xoff = 0.0; // used for perlin noise movement of the art piece on the x axis
let yoff = 0.0; // used for perlin noise movement of the art piece on the x axis

let minYchange = 10; //these two ranges determine line overlap and width
let maxYchange = 2 / danceability;
let layers = 1;
let rotStripe = 100; //rotation of each stripe
let lines = true;
let alph = 255;
let colRand = false;
let filling = true;
let colorLines = false; //false for black lines
let sw = 1; //line width

let r, g, b;
let table;

function preload() {
  table = loadTable("colors.csv", "csv", "header");
  //csv - file extension, header - indicates that the file has a header
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  rotStripe = 90 * pow(danceability, 2);
  randW = random(1, 6);
  randH = random(1, 6);

  if (lines == true) {
    // if lines are true include a stroke
    stroke(0, 0, 0);
    strokeWeight(sw);
  } else {
    noStroke();
  }
  angleMode(DEGREES);
  let end = height / 2 + 500; // where lines stop
  let palette = floor(random(10));
  // floor calculates the closest int value that is less than or equal to the value of the parameter
  // the colour is chosen from the csv, one row in the csv file is one colour pallet
  for (let i = 0; i < layers; i++) {
    // this represents the layer of the project
    let y1;
    if (i == 0) {
      y1 = height - 2 * height;
    } else {
      y1 = -height / 2 + (height / layers) * i;
    }
    //starting height for each layer
    let y2 = y1,
      y3 = y1,
      y4 = y1,
      y5 = y1,
      y6 = y1;
    let rotLayer = random(359); //layer rotation
    let rotThisStripe = 0;
    // keep going until all the lines are at the bottom
    while (
      (y1 < end) &
      (y2 < end) &
      (y3 < end) &
      (y4 < end) &
      (y5 < end) &
      (y6 < end) &
      (-maxYchange < minYchange)
    ) {
      y1 += random(minYchange, maxYchange);
      y2 += random(minYchange, maxYchange);
      y3 += random(minYchange, maxYchange);
      y4 += random(minYchange, maxYchange);
      y5 += random(minYchange, maxYchange);
      y6 += random(minYchange, maxYchange);

      if (colRand == true) {
        // if the color is set to random then get the random values for the colours
        r = random(256);
        g = random(256);
        b = random(256);
      } else {
        // if the color is not set to random then get the color values from the color pallet
        let col = floor(random(round(energy, 1) * 10)) * 3; // change this value to select less colours
        //col has to be divisible by 3

        let valenceRound = round(valence, 1);

        if (valenceRound == 0.0) {
          r = table.get(0, col);
          g = table.get(0, col + 1);
          b = table.get(0, col + 2);
        } else if (valenceRound == 0.1) {
          r = table.get(1, col);
          g = table.get(1, col + 1);
          b = table.get(1, col + 2);
        } else if (valenceRound == 0.2) {
          r = table.get(2, col);
          g = table.get(2, col + 1);
          b = table.get(2, col + 2);
        } else if (valenceRound == 0.3) {
          r = table.get(3, col);
          g = table.get(3, col + 1);
          b = table.get(3, col + 2);
        } else if (valenceRound == 0.4) {
          r = table.get(4, col);
          g = table.get(4, col + 1);
          b = table.get(4, col + 2);
        } else if (valenceRound == 0.5) {
          r = table.get(5, col);
          g = table.get(5, col + 1);
          b = table.get(5, col + 2);
        } else if (valenceRound == 0.6) {
          r = table.get(6, col);
          g = table.get(6, col + 1);
          b = table.get(6, col + 2);
        } else if (valenceRound == 0.7) {
          r = table.get(7, col);
          g = table.get(7, col + 1);
          b = table.get(7, col + 2);
        } else if (valenceRound == 0.8) {
          r = table.get(8, col);
          g = table.get(8, col + 1);
          b = table.get(8, col + 2);
        } else if (valenceRound == 0.9) {
          r = table.get(9, col);
          g = table.get(9, col + 1);
          b = table.get(9, col + 2);
        } else if (valenceRound == 1.0) {
          r = table.get(10, col);
          g = table.get(10, col + 1);
          b = table.get(10, col + 2);
        }
      }
      if (filling == true) {
        // fill the stripes if the filling is set to true
        fill(r, g, b, alph);
      } else {
        noFill();
      }
      if (colorLines == true) {
        // colour the lines
        stroke(r, g, b, alph);
      }

      push();
      //make translate random for cooler shapes
      translate(width / 2, height / 2);
      // translate(width / randW, height / randH);
      // Specifies an amount to displace objects within the display window. The x parameter specifies left/right translation, the y parameter specifies up/down translation.
      scale(0.8); // scale is a cool thing to use zoom in and out 0.4 is the lowest you can go

      rotThisStripe += rotStripe; // rotating after each stripe
      rotate(rotThisStripe + rotLayer); // rotate stripe taking into account the layer rotation
      let xStart = -width / 2;
      beginShape(); // drawing the shapes

      let noiseScale = 0; // map(noise(i*xoff, yoff), 0, 1, -20, 20)
      curveVertex(xStart - 300, height / 2 + 500);
      curveVertex(xStart - 300, y1);
      curveVertex(xStart + (width / 5) * 1, y2);
      curveVertex(xStart + (width / 5) * 2, y3);
      curveVertex(xStart + (width / 5) * 3, y4);
      curveVertex(xStart + (width / 5) * 4, y5); // * y by frameCount or mouseX works well with high danceability values 0.9
      curveVertex(width / 2 + 300, y6); // * x and y by frameCount works well with high danceability values 0.9
      curveVertex(width / 2 + 300, height / 2 + 500);
      xoff += 0.00002;

      endShape(CLOSE);
      pop();
    }
  }
  yoff += 0.0001;

  let xOffset = 100;
  let yOffset = 100;

  translate(width / 2, height / 2);
  fill(0);
  // for loop to output the letters
  for (let i = 0; i < (instrumentalness / 2) * 10; i++) {
    let randomLetter = alphabet[Math.floor(Math.random() * alphabet.length)];

    let randWidth = random(-width / 2 + xOffset, width / 2 - xOffset);
    let randHeight = random(-height / 2 + yOffset, height / 2 - yOffset);
    print(randomLetter);
    print("width " + randWidth);
    print("height " + randHeight);
    textSize(100);
    fill(255);
    strokeWeight(1);
    rotate(random(360));
    text(randomLetter, randWidth, randHeight); // x y
  }
}

// function allowing the user to save the art piece
function keyTyped() {
  if (key == "s") {
    save("spotify_art_piece.jpg");
  }
}
