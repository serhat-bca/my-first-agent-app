# Game over collisions

Given a snake whose next move crosses the boundary of the board
When the game ticks forward
Then the game ends with a game over status

Given a snake whose next move collides into its own body
When the game ticks forward
Then the game ends with a game over status
