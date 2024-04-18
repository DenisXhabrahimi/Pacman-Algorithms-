
from pacman_module.game import Agent, Directions
from pacman_module.util import Stack


def key(state):
    """Returns a key that uniquely identifies a Pacman game state.

    Arguments:
        state: a game state. See API or class pacman.GameState.

    Returns:
        A hashable key tuple.
    """
    return state.getPacmanPosition(),


class PacmanAgent(Agent):
    """Pacman agent based on iterative deepening depth-first search (IDS-DFS)."""

    def _init_(self):
        super()._init_()
        self.moves = None

    def get_action(self, state):
        """Given a Pacman game state, returns a legal move.

        Arguments:
            state: a game state. See API or class pacman.GameState.

        Return:
            A legal move as defined in game.Directions.
        """
        if self.moves is None:
            self.moves = self.iterative_deepening_search(state)

        if self.moves:
            return self.moves.pop(0)
        else:
            return Directions.STOP

    def iterative_deepening_search(self, state):
        """Iterative Deepening Depth-First Search (IDS-DFS).

        Arguments:
            state: a game state. See API or class pacman.GameState.

        Returns:
            A list of legal moves.
        """
        depth_limit = 0

        while True:
            result = self.dfs(state, depth_limit)
            if result is not None:
                return result
            depth_limit += 1

    def dfs(self, state, depth_limit):
        """Depth-First Search (DFS) with depth limit.

        Arguments:
            state: a game state. See API or class pacman.GameState.
            depth_limit: maximum depth to explore.

        Returns:
            A list of legal moves.
        """
        fringe = Stack()
        fringe.push((state, []))  # Initialize an empty path
        closed = set()

        while not fringe.isEmpty():
            current, path = fringe.pop()

            if current.isWin():
                return path

            current_key = key(current)

            if current_key in closed:
                continue
            else:
                closed.add(current_key)

            if len(path) < depth_limit:
                for successor, action in current.generatePacmanSuccessors():
                    fringe.push((successor, path + [action]))

        return None


if __name__ == '_main_':
    # You can test the IDS-DFS agent here if needed
    pass