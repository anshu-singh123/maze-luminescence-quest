
import React from 'react';
import { Button } from '@/components/ui/button';
import { Star, Trophy, Footprints } from 'lucide-react';

interface GameUIProps {
  score: number;
  moves: number;
  collectedItems: number;
  totalItems: number;
  gameStatus: 'init' | 'playing' | 'won';
  onRestart: () => void;
}

const GameUI: React.FC<GameUIProps> = ({
  score,
  moves,
  collectedItems,
  totalItems,
  gameStatus,
  onRestart,
}) => {
  return (
    <div className="w-full max-w-2xl mb-4">
      <div className="flex flex-col sm:flex-row justify-between items-center bg-maze-wall/30 p-4 rounded-lg mb-4">
        <div className="flex items-center mb-2 sm:mb-0">
          <Star className="h-5 w-5 text-maze-item mr-2" />
          <span className="font-bold">Score: {score}</span>
        </div>
        
        <div className="flex items-center mb-2 sm:mb-0">
          <Star className="h-5 w-5 text-maze-item mr-2" />
          <span>Items: {collectedItems}/{totalItems}</span>
        </div>
        
        <div className="flex items-center">
          <Footprints className="h-5 w-5 text-maze-light mr-2" />
          <span>Moves: {moves}</span>
        </div>
      </div>
      
      {gameStatus === 'won' && (
        <div className="bg-maze-exit/20 p-4 rounded-lg mb-4 text-center">
          <h2 className="text-2xl font-bold mb-2 flex items-center justify-center">
            <Trophy className="h-6 w-6 text-maze-exit mr-2" />
            Victory!
          </h2>
          <p className="mb-4">You completed the maze with a score of {score} in {moves} moves!</p>
          <Button
            onClick={onRestart}
            className="bg-maze-exit hover:bg-maze-exit/80 text-white"
          >
            Play Again
          </Button>
        </div>
      )}
      
      {gameStatus === 'playing' && (
        <div className="flex justify-end">
          <Button
            onClick={onRestart}
            variant="outline"
            className="text-maze-light border-maze-wall/50 hover:bg-maze-wall/20"
          >
            Restart
          </Button>
        </div>
      )}
    </div>
  );
};

export default GameUI;
