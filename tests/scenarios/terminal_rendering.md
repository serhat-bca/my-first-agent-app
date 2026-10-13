# Terminal rendering

Given a terminal display session
When the render loop starts
Then the hardware cursor is hidden via terminal escape sequences
And cursor positioning during updates is disabled with leaveok
And the screen is cleared once before drawing frames

Given an active terminal display
When the render loop finishes or exits
Then the hardware cursor is re-enabled via terminal escape sequences

Given an active terminal display
When a frame is drawn
Then each line is drawn with clear to end of line
And the full screen is not erased on every frame
