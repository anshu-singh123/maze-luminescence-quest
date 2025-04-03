
import React from 'react';
import { Maze, MazeCell } from '@/utils/mazeGenerator';
import { cn } from '@/lib/utils';

interface MazeRendererProps {
  maze: Maze;
  player: {
    x: number;
    y: number;
  };
}

const MazeRenderer: React.FC<MazeRendererProps> = ({ maze, player }) => {
  const cellSize = 24; // Size of each cell in pixels
  
  // Get light intensity class based on light value
  const getLightClass = (light: number) => {
    if (light >= 0.7) return 'opacity-100';
    if (light >= 0.5) return 'opacity-80';
    if (light >= 0.3) return 'opacity-50';
    if (light >= 0.1) return 'opacity-30';
    return 'opacity-10';
  };
  
  // Get background color based on cell type
  const getCellStyle = (cell: MazeCell) => {
    const light = cell.light || 0;
    
    switch (cell.type) {
      case 'wall':
        return {
          backgroundColor: `rgb(64, 62, 67, ${Math.max(light * 0.9, 0.05)})`,
        };
      case 'path':
        return {
          backgroundColor: `rgb(34, 31, 38, ${Math.max(light * 0.95, 0.05)})`,
        };
      case 'start':
        return {
          backgroundColor: `rgb(139, 92, 246, ${Math.max(light * 0.8, 0.15)})`,
        };
      case 'exit':
        return {
          backgroundColor: `rgb(14, 165, 233, ${Math.max(light * 0.8, 0.2)})`,
        };
      case 'item':
        return {
          backgroundColor: `rgb(217, 70, 239, ${Math.max(light * 0.8, 0.2)})`,
        };
      default:
        return {};
    }
  };

  return (
    <div 
      className="relative"
      style={{
        width: `${maze.width * cellSize}px`,
        height: `${maze.height * cellSize}px`,
        boxShadow: '0 0 30px rgba(139, 92, 246, 0.2)'
      }}
    >
      {/* Render maze cells */}
      {maze.grid.map((row, y) => (
        <div key={y} className="flex">
          {row.map((cell, x) => (
            <div
              key={`${x}-${y}`}
              className={cn(
                "transition-colors duration-200",
                cell.type === 'wall' && 'border border-maze-wall/20',
                cell.type === 'exit' && 'animate-pulse-light'
              )}
              style={{
                width: `${cellSize}px`,
                height: `${cellSize}px`,
                ...getCellStyle(cell),
              }}
            >
              {cell.type === 'item' && (
                <div className="w-full h-full flex items-center justify-center">
                  <div className="w-2/3 h-2/3 rounded-full bg-white/80 animate-float" />
                </div>
              )}
            </div>
          ))}
        </div>
      ))}

      {/* Render player */}
      <div
        className="absolute rounded-full bg-maze-player transition-all duration-200 shadow-lg shadow-maze-player/50"
        style={{
          width: `${cellSize * 0.8}px`,
          height: `${cellSize * 0.8}px`,
          left: `${player.x * cellSize + cellSize * 0.1}px`,
          top: `${player.y * cellSize + cellSize * 0.1}px`,
          zIndex: 10,
          filter: 'brightness(1.2)',
        }}
      />

      {/* Render player light effect */}
      <div
        className="absolute rounded-full radial-light animate-pulse-light pointer-events-none"
        style={{
          width: `${cellSize * 10}px`,
          height: `${cellSize * 10}px`,
          left: `${player.x * cellSize - cellSize * 4.5}px`,
          top: `${player.y * cellSize - cellSize * 4.5}px`,
          background: 'radial-gradient(circle, rgba(139, 92, 246, 0.5) 0%, rgba(139, 92, 246, 0.1) 60%, rgba(139, 92, 246, 0) 75%)',
          zIndex: 5,
        }}
      />
    </div>
  );
};

export default MazeRenderer;
