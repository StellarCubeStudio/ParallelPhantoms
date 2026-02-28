import java.io.*;
import ddf.minim.*;

Minim minim = new Minim(this);
AudioPlayer bgm;

float startScreenAlpha = 255;
boolean showStartScreen = true;
int startScreenHoldTimer = 0;

float startScreenTransitionAlpha = 0;
int startScreenTransitionTimer = 0;

class Star {
    float x, y;
    float alpha;

    Star(float x, float y) {
        this.x = x;
        this.y = y;
        this.alpha = 0;
    }
}

ArrayList<Star> stars = new ArrayList<Star>();
int totalStars = 300;
int starsCreatedPerBatch = 20;
int frameInterval = 5;
int lastStarCreationFrame = 0;

ArrayList<ArrayList<IntList>> Levels = new ArrayList<ArrayList<IntList>>();
ArrayList<ArrayList<IntList>> Levels_Parallel = new ArrayList<ArrayList<IntList>>();
ArrayList<IntList> Obstacles = new ArrayList<IntList>();
ArrayList<IntList> Obstacles_Parallel = new ArrayList<IntList>();

boolean Paralleled = false;
boolean mapLoaded = false;

float dimensionTransitionAlpha = 0;
int dimensionTransitionTimer = 0;
boolean transitionBlocked = false;

boolean leftPressed = false;
boolean rightPressed = false;

int level = 0;
int page = 0;
int selectedLevel = 1;
boolean previewParalleled = false; 
int playerState = 0;

float playerX = 0;
float playerY = 0;
float last_playerX = 0;
float last_playerY = 0;
//For PlayerState :
//value 1 => Stand
//value 2 => Run => 4, 5, 6, 7, 8, 9 Different Running Outlook
//value 3 => Jump

//Collides
int CollideX = 10;
int CollideY = 30;

//FreeJump
float speedX = 0;
float speedY = 0;
float accelerationX = 0;
float a = -1.6;


void loadMaps() {
	mapLoaded = true;
	IntList obstacle = new IntList();

	// # Level 1
	ArrayList<IntList> level1 = new ArrayList<IntList>();
	obstacle.append(250);
	obstacle.append(80);
	obstacle.append(300);
	obstacle.append(0);
	level1.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(400);
	obstacle.append(300);
	obstacle.append(420);
	obstacle.append(0);
	level1.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(530);
	obstacle.append(300);
	obstacle.append(550);
	obstacle.append(0);
	level1.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(650);
	obstacle.append(170);
	obstacle.append(700);
	obstacle.append(0);
	level1.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(50);
	obstacle.append(15);
	level1.add(obstacle.copy());
	obstacle.clear(); // Start
	obstacle.append(950);
	obstacle.append(15);
	level1.add(obstacle.copy());
	obstacle.clear(); // End
	Levels.add(level1);

	ArrayList<IntList> level1_parallel = new ArrayList<IntList>();
	obstacle.append(330);
	obstacle.append(350);
	obstacle.append(350);
	obstacle.append(0);
	level1_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(450);
	obstacle.append(120);
	obstacle.append(500);
	obstacle.append(0);
	level1_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(600);
	obstacle.append(300);
	obstacle.append(620);
	obstacle.append(0);
	level1_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(50);
	obstacle.append(15);
	level1_parallel.add(obstacle.copy());
	obstacle.clear(); // Start
	obstacle.append(950);
	obstacle.append(850);
	level1_parallel.add(obstacle.copy());
	obstacle.clear(); // End
	Levels_Parallel.add(level1_parallel);

	// # Level 2
	ArrayList<IntList> level2 = new ArrayList<IntList>();
	obstacle.append(300);
	obstacle.append(170);
	obstacle.append(400);
	obstacle.append(0);
	level2.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(700);
	obstacle.append(370);
	obstacle.append(800);
	obstacle.append(0);
	level2.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(50);
	obstacle.append(15);
	level2.add(obstacle.copy());
	obstacle.clear(); // Start
	obstacle.append(850);
	obstacle.append(15);
	level2.add(obstacle.copy());
	obstacle.clear(); // End
	Levels.add(level2);

	ArrayList<IntList> level2_parallel = new ArrayList<IntList>();
	obstacle.append(120);
	obstacle.append(50);
	obstacle.append(200);
	obstacle.append(0);
	level2_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(500);
	obstacle.append(290);
	obstacle.append(600);
	obstacle.append(0);
	level2_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(50);
	obstacle.append(15);
	level2_parallel.add(obstacle.copy());
	obstacle.clear(); // Start
	obstacle.append(850);
	obstacle.append(850);
	level2_parallel.add(obstacle.copy());
	obstacle.clear(); // End
	Levels_Parallel.add(level2_parallel);

	// # Level 3
	ArrayList<IntList> level3 = new ArrayList<IntList>();
	obstacle.append(70);
	obstacle.append(40);
	obstacle.append(100);
	obstacle.append(30);
	level3.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(270);
	obstacle.append(240);
	obstacle.append(300);
	obstacle.append(230);
	level3.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(470);
	obstacle.append(440);
	obstacle.append(500);
	obstacle.append(430);
	level3.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(50);
	obstacle.append(15);
	level3.add(obstacle.copy());
	obstacle.clear(); // Start
	obstacle.append(800);
	obstacle.append(515);
	level3.add(obstacle.copy());
	obstacle.clear(); // End
	Levels.add(level3);

	ArrayList<IntList> level3_parallel = new ArrayList<IntList>();
	obstacle.append(170);
	obstacle.append(140);
	obstacle.append(200);
	obstacle.append(130);
	level3_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(370);
	obstacle.append(340);
	obstacle.append(400);
	obstacle.append(330);
	level3_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(570);
	obstacle.append(540);
	obstacle.append(600);
	obstacle.append(530);
	level3_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(50);
	obstacle.append(15);
	level3_parallel.add(obstacle.copy());
	obstacle.clear(); // Start
	obstacle.append(585);
	obstacle.append(545);
	level3_parallel.add(obstacle.copy());
	obstacle.clear(); // End
	Levels_Parallel.add(level3_parallel);

	// # Level 4

	ArrayList<IntList> level4 = new ArrayList<IntList>();
	obstacle.append(100);
	obstacle.append(100);
	obstacle.append(150);
	obstacle.append(0);
	level4.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(150);
	obstacle.append(200);
	obstacle.append(200);
	obstacle.append(0);
	level4.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(200);
	obstacle.append(300);
	obstacle.append(250);
	obstacle.append(0);
	level4.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(250);
	obstacle.append(400);
	obstacle.append(300);
	obstacle.append(0);
	level4.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(300);
	obstacle.append(500);
	obstacle.append(350);
	obstacle.append(0);
	level4.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(350);
	obstacle.append(600);
	obstacle.append(400);
	obstacle.append(0);
	level4.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(400);
	obstacle.append(650);
	obstacle.append(450);
	obstacle.append(0);
	level4.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(50);
	obstacle.append(15);
	level4.add(obstacle.copy());
	obstacle.clear(); // Start
	obstacle.append(800);
	obstacle.append(515);
	level4.add(obstacle.copy());
	obstacle.clear(); // End
	Levels.add(level4);

	ArrayList<IntList> level4_parallel = new ArrayList<IntList>();
	obstacle.append(620);
	obstacle.append(200);
	obstacle.append(650);
	obstacle.append(190);
	level4_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(50);
	obstacle.append(15);
	level4_parallel.add(obstacle.copy());
	obstacle.clear(); // Start
	obstacle.append(630);
	obstacle.append(210);
	level4_parallel.add(obstacle.copy());
	obstacle.clear(); // End
	Levels_Parallel.add(level4_parallel);

	// # Level 5

	ArrayList<IntList> level5 = new ArrayList<IntList>();
	obstacle.append(100);
	obstacle.append(100);
	obstacle.append(130);
	obstacle.append(0);
	level5.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(200);
	obstacle.append(200);
	obstacle.append(230);
	obstacle.append(0);
	level5.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(300);
	obstacle.append(300);
	obstacle.append(330);
	obstacle.append(0);
	level5.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(400);
	obstacle.append(350);
	obstacle.append(430);
	obstacle.append(0);
	level5.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(480);
	obstacle.append(800);
	obstacle.append(500);
	obstacle.append(0);
	level5.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(560);
	obstacle.append(800);
	obstacle.append(580);
	obstacle.append(0);
	level5.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(600);
	obstacle.append(600);
	obstacle.append(630);
	obstacle.append(0);
	level5.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(700);
	obstacle.append(650);
	obstacle.append(730);
	obstacle.append(0);
	level5.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(50);
	obstacle.append(15);
	level5.add(obstacle.copy());
	obstacle.clear(); // Start
	obstacle.append(720);
	obstacle.append(675);
	level5.add(obstacle.copy());
	obstacle.clear(); // End
	Levels.add(level5);

	ArrayList<IntList> level5_parallel = new ArrayList<IntList>();
	obstacle.append(350);
	obstacle.append(800);
	obstacle.append(370);
	obstacle.append(0);
	level5_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(400);
	obstacle.append(320);
	obstacle.append(430);
	obstacle.append(0);
	level5_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(500);
	obstacle.append(420);
	obstacle.append(530);
	obstacle.append(0);
	level5_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(600);
	obstacle.append(520);
	obstacle.append(630);
	obstacle.append(0);
	level5_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(650);
	obstacle.append(800);
	obstacle.append(670);
	obstacle.append(0);
	level5_parallel.add(obstacle.copy());
	obstacle.clear();
	obstacle.append(50);
	obstacle.append(15);
	level5_parallel.add(obstacle.copy());
	obstacle.clear(); // Start
	obstacle.append(800);
	obstacle.append(800);
	level5_parallel.add(obstacle.copy());
	obstacle.clear(); // End
	Levels_Parallel.add(level5_parallel);
}

void logo(int CentreX, int CentreY) {
	stroke(0, 0, 0);
	fill(255, 255, 255);
	beginShape();
	vertex(CentreX, CentreY - 70);
	vertex(CentreX + 80, CentreY - 25);
	vertex(CentreX, CentreY + 20);
	vertex(CentreX - 80, CentreY - 25);
	vertex(CentreX, CentreY - 70);
	endShape();
	beginShape();
	vertex(CentreX, CentreY + 20);
	vertex(CentreX - 80, CentreY - 25);
	vertex(CentreX - 80, CentreY + 75);
	vertex(CentreX, CentreY + 120);
	vertex(CentreX, CentreY + 20);
	endShape();
	beginShape();
	vertex(CentreX, CentreY + 20);
	vertex(CentreX + 80, CentreY - 25);
	vertex(CentreX + 80, CentreY + 75);
	vertex(CentreX, CentreY + 120);
	vertex(CentreX, CentreY + 20);
	endShape();
}

void rendMap() {
	if (Paralleled) {
		background(0, 0, 0, 128);
		stroke(255, 255, 255);
		fill(255, 255, 255);
	} else {
		background(255, 255, 255);
		stroke(0, 0, 0);
		fill(0, 0, 0);
	}
	ArrayList<IntList> currentObstacles = Paralleled ? Obstacles_Parallel : Obstacles;

	int i = 0;
	while (i < currentObstacles.size() - 2) {
		IntList p = currentObstacles.get(i);
		beginShape();
		vertex(p.get(0), height - p.get(1));
		vertex(p.get(0), height - p.get(3));
		vertex(p.get(2), height - p.get(3));
		vertex(p.get(2), height - p.get(1));
		vertex(p.get(0), height - p.get(1));
		endShape();
		i++;
	}

	stroke(0, 255, 0);
	fill(0, 255, 0);
	IntList startPos = currentObstacles.get(currentObstacles.size() - 2);
	rect(startPos.get(0) - 10, height - startPos.get(1) - 10, 20, 20);

	stroke(255, 0, 0);
	fill(255, 0, 0);
	IntList endPos = currentObstacles.get(currentObstacles.size() - 1);
	rect(endPos.get(0) - 10, height - endPos.get(1) - 10, 20, 20);

	if (Paralleled) {
		stroke(255, 255, 255);
		fill(255, 255, 255);
	} else {
		stroke(0, 0, 0);
		fill(0, 0, 0);
	}
}

void renderLevelPreview(int levelIndex, boolean parallelMode) {
	ArrayList<IntList> currentObstacles = parallelMode ? Levels_Parallel.get(levelIndex - 1) : Levels.get(levelIndex - 1);
	float scale = min((float)(width * 0.4) / 1000, (float)(height * 0.4) / 300); // 缩放比例，稍微缩小一些留出空间给UI

	pushMatrix();
	translate(width / 2, height / 2);
	scale(scale);

	noStroke();
	fill(parallelMode ? 0 : 255, 180);
	rect(-500, -150, 1000, 300);

	if (parallelMode) {
		stroke(255, 255, 255, 200);
		fill(255, 255, 255, 180);
	} else {
		stroke(0, 0, 0, 200);
		fill(0, 0, 0, 180);
	}

	for (int i = 0; i < currentObstacles.size() - 2; i++) {
		IntList p = currentObstacles.get(i);
		beginShape();
		vertex(p.get(0) - 500, 150 - p.get(1));
		vertex(p.get(0) - 500, 150 - p.get(3));
		vertex(p.get(2) - 500, 150 - p.get(3));
		vertex(p.get(2) - 500, 150 - p.get(1));
		vertex(p.get(0) - 500, 150 - p.get(1));
		endShape();
	}

	if (parallelMode) {
		stroke(0, 255, 0, 220);
		fill(0, 255, 0, 200);
	} else {
		stroke(0, 255, 0, 220);
		fill(0, 255, 0, 200);
	}
	IntList startPos = currentObstacles.get(currentObstacles.size() - 2);
	rect(startPos.get(0) - 510, 140 - startPos.get(1), 20, 20);

	if (parallelMode) {
		stroke(255, 0, 0, 220);
		fill(255, 0, 0, 200);
	} else {
		stroke(255, 0, 0, 220);
		fill(255, 0, 0, 200);
	}
	IntList endPos = currentObstacles.get(currentObstacles.size() - 1);
	rect(endPos.get(0) - 510, 140 - endPos.get(1), 20, 20);

	popMatrix();
}

void drawArrow(boolean isLeft, boolean enabled, boolean isWhite) {
	pushStyle();
	if (enabled) {
		if (isWhite) {
			fill(255, 255, 255, 128);
			stroke(255, 255, 255, 128);
		} else {
			fill(128, 128, 128, 128);
			stroke(128, 128, 128, 128);
		}
	} else {
		if (isWhite) {
			fill(255, 255, 255, 64);
			stroke(255, 255, 255, 64);
		} else {
			fill(128, 128, 128, 64);
			stroke(128, 128, 128, 64);
		}
	}
	strokeWeight(2);

	if (isLeft) {
		triangle(70, height / 2 - 20, 70, height / 2 + 20, 30, height / 2);
	} else {
		triangle(width - 70, height / 2 - 20, width - 70, height / 2 + 20, width - 30, height / 2);
	}
	popStyle();
}

boolean isCollide(float playerLeft, float playerRight, float playerTop, float playerBottom,
                  float obstacleLeft, float obstacleRight, float obstacleTop, float obstacleBottom) {
	if (playerRight <= obstacleLeft || obstacleRight <= playerLeft) {
		return false;
	}

	if (playerTop <= obstacleBottom || obstacleTop <= playerBottom) {
		return false;
	}

	return true;
}

void player(float CentreX, float CentreY, int state) {
	CentreY = height - CentreY;
	if (Paralleled) {
		fill(255, 255, 255);
		stroke(255, 255, 255);
	} else {
		fill(0, 0, 0);
		stroke(0, 0, 0);
	}
	if (state == 1) {
		//State 1: Stand
		ellipse(CentreX, CentreY - 10, 10, 10);
		strokeWeight(2);
		line(CentreX, CentreY - 5, CentreX, CentreY + 15);
	} else if (state == 2) {
		//State 2: Run
		ellipse(CentreX, CentreY - 10, 10, 10);
		strokeWeight(2);
		line(CentreX, CentreY - 5, CentreX, CentreY + 5);
		line(CentreX, CentreY + 5, CentreX - 5, CentreY + 15);
		line(CentreX, CentreY + 5, CentreX + 5, CentreY + 15);
		line(CentreX, CentreY, CentreX - 3, CentreY + 3);
		line(CentreX, CentreY, CentreX + 3, CentreY + 3);
	} else if (state == 3) {
		// State 3: Jump
		ellipse(CentreX, CentreY - 10, 10, 10);
		strokeWeight(2);
		line(CentreX, CentreY - 5, CentreX, CentreY + 5);
		line(CentreX, CentreY + 5, CentreX - 5, CentreY + 12);
		line(CentreX, CentreY + 5, CentreX - 2, CentreY + 15);
		line(CentreX, CentreY, CentreX - 3, CentreY - 3);
		line(CentreX, CentreY, CentreX + 3, CentreY - 3);
	}
}

void readData() {
	File f = new File("PP_level.data");
	if (!f.exists()) {
		level = 1;
		return;
	}
	try {
		FileInputStream fis = new FileInputStream("PP_level.data");
		level = fis.read();
		fis.close();
	} catch (IOException i) {
		println("Catched Input Error, got : ");
		println(i);
	}
}

void saveData() {
	try {
		FileOutputStream fos = new FileOutputStream("PP_level.data");
		fos.write(level);
		fos.close();
	} catch (IOException i) {
		println("Catched Output Error, got : ");
		println(i);
	}
}

void setup() {
	pixelDensity(2);
	fullScreen();
	frameRate(30);

	bgm = minim.loadFile("background.mp3");
	bgm.loop();
	page = 1;

	for (int i = 0; i < min(starsCreatedPerBatch, totalStars); i++) {
		stars.add(new Star(random(0, width), random(0, height)));
	}
	lastStarCreationFrame = 0;
}

void draw() {
	if (showStartScreen) {
		background(0, 0, 0);
		logo(width / 2, height / 2);
		fill(255, 255, 255);
		textFont(loadFont("DengXian-Light-48.vlw"));
		textSize(50);
		textAlign(CENTER);
		text("Stellar Cube Studio", width / 2, height / 2 + 200);

		for (Star star : stars) {
			if (star.alpha < 255) {
				star.alpha = min(star.alpha + 5, 255);
			}
		}

		if (frameCount % frameInterval == 0 && stars.size() < totalStars) {
			int remainingStars = totalStars - stars.size();
			int starsToAdd = min(starsCreatedPerBatch, remainingStars);
			for (int i = 0; i < starsToAdd; i++) {
				stars.add(new Star(random(0, width), random(0, height)));
			}
		}

		for (Star star : stars) {
			fill(255, 255, 255, star.alpha);
			stroke(255, 255, 255, star.alpha);
			ellipse(star.x, star.y, 1, 1);
		}

		fill(0, 0, 0, startScreenAlpha);
		noStroke();
		rect(0, 0, width, height);
		startScreenAlpha -= 255.0 / 60;
		if (startScreenAlpha <= 0) {
			startScreenAlpha = 0;
			if (startScreenHoldTimer == 0) {
				startScreenHoldTimer = 30;
			} else if (startScreenHoldTimer > 0) {
				startScreenHoldTimer--;
				if (startScreenHoldTimer <= 0) {
					showStartScreen = false;
				}
			}
		}
	} else if (page == 1) {
		if (Paralleled) {
			fill(255, 255, 255);
			background(0, 0, 0);
		} else {
			fill(0, 0, 0);
			background(255, 255, 255);
		}
		textFont(loadFont("InkFree-48.vlw"));
		textSize(100);
		text("Parallel Phantoms", width / 2, height / 2 - 180);
		textFont(loadFont("DengXian-Light-48.vlw"));
		textSize(45);
		text("Press Enter or I to start.", width / 2, height / 2 + 200);

		if (startScreenTransitionTimer > 0) {
			fill(255, 255, 255, startScreenTransitionAlpha);
			noStroke();
			rect(0, 0, width, height);

			startScreenTransitionTimer--;
			if (startScreenTransitionTimer >= 10) {
				startScreenTransitionAlpha = 128;
			} else {
				startScreenTransitionAlpha = map(startScreenTransitionTimer, 10, 0, 128, 0);
			}
		}

		if (frameCount % 60 == 0 && startScreenTransitionTimer <= 0) {
			Paralleled = !Paralleled;
			startScreenTransitionAlpha = 128;
			startScreenTransitionTimer = 10;
		}
	} else if (page == 2) {
		background(255, 255, 255);
		textSize(100);
		text("Loading...", width / 2, height / 2);
		if (!mapLoaded) {
			loadMaps();
		}
		if (level == 0) {
			readData();
		}
		if (level < 1 || level > Levels.size()) {
			level = 1;
		}
		Obstacles = Levels.get(level - 1);
		Obstacles_Parallel = Levels_Parallel.get(level - 1);
		Paralleled = false;
		IntList startPos = Obstacles.get(Obstacles.size() - 2);
		playerX = startPos.get(0);
		playerY = startPos.get(1);
		page = 4;
		playerState = 1;
		selectedLevel = level;
	} else if (page == 4) {
		if (previewParalleled) {
			background(0, 0, 0);
		} else {
			background(255, 255, 255);
		}
		fill(128, 128, 128, 200);
		textSize(100);
		textAlign(CENTER);
		textFont(loadFont("InkFree-48.vlw"));
		text("Select Level", width / 2, 120);
		renderLevelPreview(selectedLevel, previewParalleled);

		if (previewParalleled) {
			fill(255, 255, 255, 220);
		} else {
			fill(0, 0, 0, 220);
		}
		textFont(loadFont("DengXian-Light-48.vlw"));
		textSize(75);
		textAlign(CENTER);
		text("Level " + selectedLevel, width / 2, height - 100);

		fill(128, 128, 128, 180);
		textSize(30);
		text("Press A/D to switch levels, Q to toggle preview, Enter to play", width / 2, height - 40);

		if (selectedLevel > 1) {
			drawArrow(true, true, previewParalleled);
		} else {
			drawArrow(true, false, previewParalleled);
		}

		if (selectedLevel < Levels.size()) {
			drawArrow(false, true, previewParalleled);
		} else {
			drawArrow(false, false, previewParalleled);
		}
	} else if (page == 3) {
		rendMap();
		if (dimensionTransitionTimer > 0) {
			if (transitionBlocked) {
				fill(255, 0, 0, dimensionTransitionAlpha);
			} else {
				fill(255, 255, 255, dimensionTransitionAlpha);
			}
			noStroke();
			rect(0, 0, width, height);

			dimensionTransitionTimer--;
			if (transitionBlocked) {
				dimensionTransitionAlpha = map(dimensionTransitionTimer, 10, 0, 77, 0);
			} else {
				dimensionTransitionAlpha = map(dimensionTransitionTimer, 10, 0, 128, 0);
			}
		}
		speedX *= 0.9;

		if (leftPressed && !rightPressed) {
			accelerationX = -0.8;
		} else if (rightPressed && !leftPressed) {
			accelerationX = 0.8;
		} else {
			accelerationX = 0;
		}

		speedX += accelerationX;

		float maxSpeed = 8.0;
		if (speedX > maxSpeed) speedX = maxSpeed;
		if (speedX < -maxSpeed) speedX = -maxSpeed;

		float newX = playerX + speedX;
		if (!checkCollisionAtPosition(newX, playerY)) {
			playerX = newX;
		} else if (speedX != 0) {
			speedX = 0;
		}
		float newY = playerY + speedY;

		if (playerState == 3) {
			speedY += a;
		}

		if (!checkCollisionAtPosition(playerX, newY)) {
			playerY = newY;
			if (speedY > 0.5) {
				playerState = 3;
			} else if (speedY < -0.5) {
				playerState = 3;
			}
		} else if (playerY > newY) {
			float prevY = playerY;
			playerY = newY;

			if (checkCollisionAtPosition(playerX, playerY)) {
				playerY = prevY;
				for (int offset = 1; offset <= 5; offset++) {
					if (!checkCollisionAtPosition(playerX, playerY - offset)) {
						playerY -= offset;
						break;
					}
				}

				if (!checkCollisionAtPosition(playerX, playerY)) {
					speedY = 0;
					if (checkCollisionBelowAfterFall()) {
						playerState = (speedX == 0 ? 1 : 2);
					} else {
						playerState = 3;
					}
				} else {
					playerY = prevY;
					playerState = 3;
				}
			} else {
				speedY = 0;
				playerState = (speedX == 0 ? 1 : 2);
			}
		}

		if (playerState != 3 && !checkCollisionAtPosition(playerX, playerY - 1)) {
			if (speedY > -0.5 && speedY < 0.5) {
				if (speedY <= 0) {
					playerState = 3;
				}
			}
		}

		if (speedX != 0 && playerState != 3) {
			playerState = 2;
		} else if (speedX == 0 && playerState != 3) {
			playerState = 1;
		}

		if (playerX < 5) {
			playerX = 5;
			speedX = 0;
		}
		if (playerX > width - 5) {
			playerX = width - 5;
			speedX = 0;
		}

		if (playerY <= 15) {
			playerY = 15;
			speedY = 0;
			playerState = (speedX == 0 ? 1 : 2);
		}
		if (playerY > height - 15) {
			playerY = height - 15;
			speedY = 0;
		}

		player(playerX, playerY, playerState);

		last_playerX = playerX;
		last_playerY = playerY;
	}
}

boolean checkCollisionAtPosition(float x, float y) {
	float BoxLeftX = x - CollideX / 2;
	float BoxRightX = x + CollideX / 2;
	float BoxUpY = y + CollideY / 2;
	float BoxDownY = y - CollideY / 2;

	ArrayList<IntList> currentObstacles = Paralleled ? Obstacles_Parallel : Obstacles;

	for (int i = 0; i < currentObstacles.size() - 2; i++) {
		IntList obs = currentObstacles.get(i);
		float ObsLeftX = obs.get(0);
		float ObsRightX = obs.get(2);
		float ObsUpY = obs.get(1);
		float ObsDownY = obs.get(3);
		if (isCollide(BoxLeftX, BoxRightX, BoxUpY, BoxDownY, ObsLeftX, ObsRightX, ObsUpY, ObsDownY)) {
			return true;
		}
	}
	return false;
}

boolean checkCollisionBelowAfterFall() {
	return checkCollisionAtPosition(playerX, playerY - 2);
}

void keyPressed() {
	if (showStartScreen) {
		showStartScreen = false;
		startScreenAlpha = 0;
	} else if (page == 1) {
		if (key == ENTER || key == 'I' || key == 'i') {
			page = 2;
		}
		if (key == ESC) {
			exit();
		}
	} else if (page == 4) {
		if (key == 'A' || key == 'a') {
			if (selectedLevel > 1) {
				selectedLevel--;
			}
		} else if (key == 'D' || key == 'd') {
			if (selectedLevel < Levels.size()) {
				selectedLevel++;
			}
		} else if (key == 'Q' || key == 'q' || key == 'K' || key == 'k') {
			previewParalleled = !previewParalleled;
		} else if (key == ENTER || key == 'I' || key == 'i') { 
			page = 3; 
			level = selectedLevel;
			Obstacles = Levels.get(level - 1);
			Obstacles_Parallel = Levels_Parallel.get(level - 1);
			Paralleled = false;
			IntList startPos = Obstacles.get(Obstacles.size() - 2);
			playerX = startPos.get(0);
			playerY = startPos.get(1);
			speedX = 0;
			speedY = 0;
			playerState = 1;
		} else if (key == BACKSPACE) {
			page = 1;
		}
	} else if (page == 3) {
		if (playerState != 3 && (key == 'W' || key == 'w')) {
			playerState = 3;
			speedY = 20;
		}
		if (key == 'D' || key == 'd') {
			rightPressed = true;
		}
		if (key == 'A' || key == 'a') {
			leftPressed = true;
		}
		if (key == 'Q' || key == 'q' || key == 'K' || key == 'k') {
			boolean targetDimension = !Paralleled;
			ArrayList<IntList> targetObstacles = targetDimension ? Obstacles_Parallel : Obstacles;

			boolean wouldCollide = false;
			for (int i = 0; i < targetObstacles.size() - 2; i++) {
				IntList obs = targetObstacles.get(i);
				float ObsLeftX = obs.get(0);
				float ObsRightX = obs.get(2);
				float ObsUpY = obs.get(1);
				float ObsDownY = obs.get(3);

				float BoxLeftX = playerX - CollideX / 2;
				float BoxRightX = playerX + CollideX / 2;
				float BoxUpY = playerY + CollideY / 2;
				float BoxDownY = playerY - CollideY / 2;

				if (isCollide(BoxLeftX, BoxRightX, BoxUpY, BoxDownY, ObsLeftX, ObsRightX, ObsUpY, ObsDownY)) {
					wouldCollide = true;
					break;
				}
			}

			if (wouldCollide) {
				transitionBlocked = true;
				dimensionTransitionAlpha = 77;
				dimensionTransitionTimer = 10;
			} else {
				transitionBlocked = false;
				dimensionTransitionAlpha = 128;
				dimensionTransitionTimer = 10;
				Paralleled = targetDimension;
			}
		}
		if (key == 'I' || key == 'i') {
			if (playerX >= (Obstacles.get(Obstacles.size() - 1)).get(0) - 15 && playerX <= (Obstacles.get(Obstacles.size() - 1)).get(0) + 15
			        && playerY >= (Obstacles.get(Obstacles.size() - 1)).get(1) - 15 && playerY <= (Obstacles.get(Obstacles.size() - 1)).get(1) + 15) {
				page = 2;
				level++;
				saveData();
			}
			if (playerX >= (Obstacles_Parallel.get(Obstacles_Parallel.size() - 1)).get(0) - 15 && playerX <= (Obstacles_Parallel.get(Obstacles_Parallel.size() - 1)).get(0) + 15
			        && playerY >= (Obstacles_Parallel.get(Obstacles_Parallel.size() - 1)).get(1) - 15 && playerY <= (Obstacles_Parallel.get(Obstacles_Parallel.size() - 1)).get(1) + 15) {
				page = 2;
				level++;
				saveData();
			}
		}
		if (key == BACKSPACE) {
			page = 1;
		}
	}
}

void keyReleased() {
	if (page == 3) {
		if ((key == 'D' || key == 'd')) {
			rightPressed = false;
		}
		if ((key == 'A' || key == 'a')) {
			leftPressed = false;
		}
	}
}
