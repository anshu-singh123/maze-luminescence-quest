
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { generateMaze, calculateLighting, Maze, MazeCell } from '@/utils/mazeGenerator';
import { Button } from '@/components/ui/button';
import { toast } from '@/components/ui/use-toast';
import MazeRenderer from '@/components/MazeRenderer';
import GameUI from '@/components/GameUI';

// Define keyboard controls
const CONTROLS = {
  UP: ['ArrowUp', 'w', 'W'],
  RIGHT: ['ArrowRight', 'd', 'D'],
  DOWN: ['ArrowDown', 's', 'S'],
  LEFT: ['ArrowLeft', 'a', 'A'],
};

interface Player {
  x: number;
  y: number;
}

interface GameState {
  status: 'init' | 'playing' | 'won';
  score: number;
  moves: number;
  startTime: number | null;
  endTime: number | null;
}

const MazeGame: React.FC = () => {
  // Game configuration
  const mazeWidth = 21; // Must be odd for the algorithm
  const mazeHeight = 21; // Must be odd for the algorithm
  const lightRadius = 5;
  
  // Game state
  const [maze, setMaze] = useState<Maze | null>(null);
  const [player, setPlayer] = useState<Player>({ x: 0, y: 0 });
  const [gameState, setGameState] = useState<GameState>({
    status: 'init',
    score: 0,
    moves: 0,
    startTime: null,
    endTime: null,
  });
  const [collectedItems, setCollectedItems] = useState<Set<string>>(new Set());
  
  // Animation frame reference
  const animationFrameRef = useRef<number | null>(null);

  // Initialize a new game
  const initGame = useCallback(() => {
    const newMaze = generateMaze(mazeWidth, mazeHeight);
    const initializedMaze = calculateLighting(
      newMaze,
      newMaze.start.x,
      newMaze.start.y,
      lightRadius
    );
    
    setMaze(initializedMaze);
    setPlayer({ x: newMaze.start.x, y: newMaze.start.y });
    setCollectedItems(new Set());
    setGameState({
      status: 'playing',
      score: 0,
      moves: 0,
      startTime: Date.now(),
      endTime: null,
    });
    
    toast('Maze generated! Find the exit and collect items.', {
      description: 'Use WASD or arrow keys to move.',
    });
  }, [mazeWidth, mazeHeight, lightRadius]);

  // Handle keyboard inputs
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    if (gameState.status !== 'playing' || !maze) return;

    let newX = player.x;
    let newY = player.y;

    if (CONTROLS.UP.includes(event.key)) {
      newY = Math.max(0, player.y - 1);
    } else if (CONTROLS.RIGHT.includes(event.key)) {
      newX = Math.min(maze.width - 1, player.x + 1);
    } else if (CONTROLS.DOWN.includes(event.key)) {
      newY = Math.min(maze.height - 1, player.y + 1);
    } else if (CONTROLS.LEFT.includes(event.key)) {
      newX = Math.max(0, player.x - 1);
    } else {
      return; // Not a movement key
    }

    // Check if the new position is valid (not a wall)
    if (maze.grid[newY][newX].type !== 'wall') {
      // Update moves
      setGameState((prev) => ({
        ...prev,
        moves: prev.moves + 1,
      }));

      // Check if player collected an item
      if (maze.grid[newY][newX].type === 'item') {
        const itemKey = `${newX},${newY}`;
        if (!collectedItems.has(itemKey)) {
          const newCollectedItems = new Set(collectedItems);
          newCollectedItems.add(itemKey);
          setCollectedItems(newCollectedItems);
          
          setGameState((prev) => ({
            ...prev,
            score: prev.score + 10,
          }));
          
          toast('Item collected!', {
            description: '+10 points',
          });
          
          // Update the maze to mark the item as collected
          setMaze((prevMaze) => {
            if (!prevMaze) return prevMaze;
            
            const updatedGrid = [...prevMaze.grid];
            updatedGrid[newY][newX] = {
              ...updatedGrid[newY][newX],
              type: 'path',
            };
            
            return {
              ...prevMaze,
              grid: updatedGrid,
            };
          });
        }
      }

      // Check if player reached the exit
      if (maze.grid[newY][newX].type === 'exit') {
        setGameState((prev) => ({
          ...prev,
          status: 'won',
          endTime: Date.now(),
        }));
        
        const timeBonus = Math.floor(5000 / (Date.now() - (gameState.startTime || Date.now())) * 1000);
        const totalScore = gameState.score + timeBonus;
        
        toast('You won!', {
          description: `Final score: ${totalScore} (including time bonus: ${timeBonus})`,
        });
      }

      // Update player position
      setPlayer({ x: newX, y: newY });
    }
  }, [player, maze, gameState, collectedItems, lightRadius]);

  // Update lighting based on player position
  useEffect(() => {
    if (maze && gameState.status === 'playing') {
      const updateLighting = () => {
        setMaze((prevMaze) => {
          if (!prevMaze) return prevMaze;
          return calculateLighting(prevMaze, player.x, player.y, lightRadius);
        });
      };
      
      // Use requestAnimationFrame for smooth lighting updates
      const animate = () => {
        updateLighting();
        animationFrameRef.current = requestAnimationFrame(animate);
      };
      
      animationFrameRef.current = requestAnimationFrame(animate);
      
      return () => {
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current);
        }
      };
    }
  }, [player, maze, gameState.status, lightRadius]);

  // Set up keyboard event listeners
  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);

  // Calculate total items in the maze
  const totalItems = maze?.items.length || 0;
  const collectedItemsCount = collectedItems.size;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-maze-bg text-white p-4">
      <h1 className="text-4xl font-bold mb-6 text-maze-player">Luminescence Maze</h1>
      
      {gameState.status === 'init' && (
        <div className="flex flex-col items-center space-y-4 mb-8">
          <p className="text-xl max-w-md text-center mb-4">
            Navigate through the maze, collect items, and find the exit.
          </p>
          <Button 
            onClick={initGame}
            className="bg-maze-player hover:bg-maze-player/80 text-white px-8 py-4 text-lg"
          >
            Start Game
          </Button>
        </div>
      )}
      
      {gameState.status !== 'init' && maze && (
        <>
          <GameUI 
            score={gameState.score} 
            moves={gameState.moves} 
            collectedItems={collectedItemsCount}
            totalItems={totalItems}
            gameStatus={gameState.status}
            onRestart={initGame}
          />
          
          <div className="relative mb-8 mt-4 overflow-hidden rounded-lg border-4 border-maze-wall/30">
            <MazeRenderer maze={maze} player={player} />
          </div>
          
          <div className="flex flex-wrap justify-center gap-4 max-w-md">
            <p className="text-sm text-center text-maze-light/70 w-full">
              Use arrow keys or WASD to move
            </p>
          </div>
        </>
      )}
    </div>
  );
};

export default MazeGame;
