from pacman_module.game import Agent
from pacman_module.game import PacmanGame
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue


class PacmanAgent(Agent):
    """
    This PacmanAgent class solves the Pacman game using the Greedy Best-First Search algorithm
    """

    def __init__(self):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        super().__init__()
        self.nextactions = list()  # List to contain the final list of actions

    def construct_path(self, state, meta):
        """
        Given a pacman state and a dictionnary, produces a backtrace of
        the actions taken to find the food dot, using the recorded
        meta dictionary.

        Arguments:
        ----------
        - `state`: the current game state.
        - `meta`: a dictionnary containing the path information
                  from one node to another.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`
        """
        action_list = list()

        # Continue until you reach root meta data (i.e. (None, None))
        while meta[state][0] is not None:
            state, action = meta[state]
            action_list.append(action)

        return action_list

    def getHeuristic(self, state):
        """
        Calculates a basic heuristic: manhattan distance to closest food
        Arguments:
            state: The current pacman game state.
        Returns:
            The heuristic score.
        """
        food_list = state.getFood().asList()
        pacman_pos = state.getPacmanPosition()
        min_distance = float('inf')
        for food in food_list:
            distance = abs(food[0] - pacman_pos[0]) + abs(food[1] - pacman_pos[1])
            min_distance = min(min_distance, distance)
        return min_distance

    def greedy_best_first_search(self, state):
        """
        Implements the Greedy Best-First Search algorithm for Pacman.

        Arguments:
            state: The initial state of the Pacman game.

        Returns:
            A list of actions leading to a goal state or None if not found.
        """

        # Initialize frontier (priority queue based on heuristic)
        frontier = PriorityQueue()
        frontier.push((state, self.getHeuristic(state)), 0)

        # Set to store explored states
        explored = set()

        # Keep track of parent states for path reconstruction (similar to DFS)
        meta = dict()
        meta[state] = (None, None)

        # Loop until frontier is empty
        while not frontier.isEmpty():
            # Get state with highest heuristic from frontier (greedy selection)
            current_state, _ = frontier.pop()

            # Check if goal state reached (all food eaten)
            if state.isWin():
                return self.construct_path(current_state, meta)

            # Mark current state as explored
            explored.add((hash(current_state.getPacmanPosition()), hash(current_state.getFood())))

            # Generate successors for the current state
            successors = state.generatePacmanSuccessors()

            for next_state, action in successors:
                # Skip explored states
                if (hash(next_state.getPacmanPosition()), hash(next_state.getFood())) not in explored:
                    # Calculate heuristic for the successor
                    h_value = self.getHeuristic(next_state)
                    # Add successor to frontier with priority based on heuristic
                    frontier.push((next_state, h_value), h_value)
                    # Update meta data to track parent for path reconstruction
                    meta[next_state] = (current_state, action)

        # No solution found within explored states
        return None

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move using Greedy Best-First Search.

        Arguments:
        ----------
        - `state`: the current game state.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        if not self.nextactions:
            # Perform Greedy Best-First Search and store path (actions)
            path = self.greedy_best_first_search(state)
            if path:
                self.nextactions = path.copy()  # Avoid modifying original path

        # Return the next action from the stored path
        return self.nextactions.pop(0)