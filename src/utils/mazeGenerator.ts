
export type CellType = 'wall' | 'path' | 'start' | 'exit' | 'item';

export interface MazeCell {
  type: CellType;
  x: number;
  y: number;
  visited?: boolean;
  light?: number;
}

export interface Maze {
  grid: MazeCell[][];
  width: number;
  height: number;
  start: { x: number; y: number };
  exit: { x: number; y: number };
  items: { x: number; y: number }[];
}

// Generate a maze using recursive backtracking algorithm
export function generateMaze(width: number, height: number): Maze {
  // Initialize the grid with all walls
  const grid: MazeCell[][] = Array(height)
    .fill(null)
    .map((_, y) =>
      Array(width)
        .fill(null)
        .map((_, x) => ({
          type: 'wall',
          x,
          y,
          visited: false,
          light: 0,
        }))
    );

  // Function to check if a cell is valid and not visited
  const isValidCell = (x: number, y: number): boolean => {
    return (
      x >= 0 && x < width && y >= 0 && y < height && !grid[y][x].visited
    );
  };

  // Recursive function to generate the maze
  const carve = (x: number, y: number) => {
    // Mark the current cell as visited and make it a path
    grid[y][x].visited = true;
    grid[y][x].type = 'path';

    // Define the four possible directions: [dx, dy]
    const directions = [
      [0, -2], // Up
      [2, 0],  // Right
      [0, 2],  // Down
      [-2, 0], // Left
    ];

    // Shuffle the directions for randomness
    for (let i = directions.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [directions[i], directions[j]] = [directions[j], directions[i]];
    }

    // Try each direction
    for (const [dx, dy] of directions) {
      const newX = x + dx;
      const newY = y + dy;

      if (isValidCell(newX, newY)) {
        // Carve a path between current cell and the new cell
        grid[y + dy / 2][x + dx / 2].type = 'path';
        grid[y + dy / 2][x + dx / 2].visited = true;

        // Continue with the new cell
        carve(newX, newY);
      }
    }
  };

  // Start from a random odd cell
  const startX = 1;
  const startY = 1;
  carve(startX, startY);

  // Place the start point
  grid[startY][startX].type = 'start';
  const start = { x: startX, y: startY };

  // Place the exit at the farthest possible location from start
  let maxDistance = 0;
  let exitX = startX;
  let exitY = startY;

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      if (grid[y][x].type === 'path') {
        const distance = Math.abs(x - startX) + Math.abs(y - startY);
        if (distance > maxDistance) {
          maxDistance = distance;
          exitX = x;
          exitY = y;
        }
      }
    }
  }

  grid[exitY][exitX].type = 'exit';
  const exit = { x: exitX, y: exitY };

  // Place items randomly throughout the maze
  const items: { x: number; y: number }[] = [];
  const numItems = Math.floor((width * height) / 20); // Adjust for desired item density

  let itemsPlaced = 0;
  while (itemsPlaced < numItems) {
    const x = Math.floor(Math.random() * width);
    const y = Math.floor(Math.random() * height);

    // Only place items on path cells that aren't start or exit
    if (grid[y][x].type === 'path') {
      grid[y][x].type = 'item';
      items.push({ x, y });
      itemsPlaced++;
    }
  }

  // Clean up the visited flags
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      grid[y][x].visited = false;
    }
  }

  return {
    grid,
    width,
    height,
    start,
    exit,
    items,
  };
}

// Calculate lighting for the maze based on player position and light sources
export function calculateLighting(
  maze: Maze,
  playerX: number,
  playerY: number,
  lightRadius: number
): Maze {
  const newMaze = {
    ...maze,
    grid: maze.grid.map((row) =>
      row.map((cell) => ({
        ...cell,
        light: 0, // Reset all lights
      }))
    ),
  };

  // Helper to calculate distance between two points
  const distance = (x1: number, y1: number, x2: number, y2: number): number => {
    return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
  };

  // Add light from player
  for (let y = 0; y < maze.height; y++) {
    for (let x = 0; x < maze.width; x++) {
      const dist = distance(x, y, playerX, playerY);
      
      if (dist <= lightRadius) {
        // Calculate light intensity based on distance (inverse square law)
        const intensity = 1 - dist / lightRadius;
        newMaze.grid[y][x].light = Math.max(newMaze.grid[y][x].light, intensity);
      }
    }
  }

  // Add light from items (dimmer than player light)
  maze.items.forEach(({ x, y }) => {
    const itemLightRadius = lightRadius / 2;
    
    for (let cy = Math.max(0, y - Math.ceil(itemLightRadius)); cy < Math.min(maze.height, y + Math.ceil(itemLightRadius)); cy++) {
      for (let cx = Math.max(0, x - Math.ceil(itemLightRadius)); cx < Math.min(maze.width, x + Math.ceil(itemLightRadius)); cx++) {
        const dist = distance(cx, cy, x, y);
        
        if (dist <= itemLightRadius) {
          const intensity = (1 - dist / itemLightRadius) * 0.6; // Items are 60% as bright as player
          newMaze.grid[cy][cx].light = Math.max(newMaze.grid[cy][cx].light, intensity);
        }
      }
    }
  });

  // Add light to exit (constant soft glow)
  const exitLightRadius = lightRadius / 3;
  for (let y = Math.max(0, maze.exit.y - Math.ceil(exitLightRadius)); y < Math.min(maze.height, maze.exit.y + Math.ceil(exitLightRadius)); y++) {
    for (let x = Math.max(0, maze.exit.x - Math.ceil(exitLightRadius)); x < Math.min(maze.width, maze.exit.x + Math.ceil(exitLightRadius)); x++) {
      const dist = distance(x, y, maze.exit.x, maze.exit.y);
      
      if (dist <= exitLightRadius) {
        const intensity = (1 - dist / exitLightRadius) * 0.4; // Exit is 40% as bright as player
        newMaze.grid[y][x].light = Math.max(newMaze.grid[y][x].light, intensity);
      }
    }
  }

  return newMaze;
}
