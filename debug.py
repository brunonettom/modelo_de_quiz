import asyncio
import sys
import pygame

async def main():
    # Log the environment
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Pygame version: {pygame.version.ver}")
    
    # Initialize pygame
    print("Initializing pygame...")
    pygame.init()
    print("Pygame initialized!")
    
    # Set display mode
    print("Setting display mode...")
    screen = pygame.display.set_mode((400, 300))
    print("Display mode set!")
    
    # Loop with visual feedback
    frame = 0
    running = True
    clock = pygame.time.Clock()
    
    while running and frame < 300:  # Limit to 300 frames (10 seconds at 30fps)
        # Fill screen with color based on frame count
        color = (frame % 255, (frame * 2) % 255, (frame * 3) % 255)
        screen.fill(color)
        
        # Draw frame counter
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Frame: {frame}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        # Update display
        pygame.display.flip()
        print(f"Frame {frame} rendered with color {color}")
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Essential for browser
        await asyncio.sleep(0)
        
        # Next frame
        frame += 1
        clock.tick(30)
    
    # Clean up
    pygame.quit()
    print("Debug complete!")
    return 0

if __name__ == "__main__":
    asyncio.run(main())
