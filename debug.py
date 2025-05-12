import asyncio
import sys
import pygame
import time
import math

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
    
    # Better font handling
    try:
        font = pygame.font.SysFont(None, 36)
    except:
        print("Error loading font, using alternative method")
        font = pygame.font.Font(None, 36)
    
    # Loop with visual feedback
    frame = 0
    running = True
    clock = pygame.time.Clock()
    start_time = time.time()
    
    while running:
        # Use time-based color changes instead of frame-based
        elapsed = time.time() - start_time
        r = int(128 + 127 * math.sin(elapsed * 0.5))
        g = int(128 + 127 * math.sin(elapsed * 0.3))
        b = int(128 + 127 * math.sin(elapsed * 0.7))
        color = (r, g, b)
        
        # Fill screen with color
        screen.fill(color)
        
        # Draw frame counter and info
        text = font.render(f"Frame: {frame}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        color_text = font.render(f"Color: {color}", True, (255, 255, 255))
        screen.blit(color_text, (10, 50))
        
        time_text = font.render(f"Time: {elapsed:.1f}s", True, (255, 255, 255))
        screen.blit(time_text, (10, 90))
        
        # Handle clicks to verify interactivity
        mouse_pos = pygame.mouse.get_pos()
        pos_text = font.render(f"Mouse: {mouse_pos}", True, (255, 255, 255))
        screen.blit(pos_text, (10, 130))
        
        # Update display
        pygame.display.flip()
        print(f"Frame {frame} rendered with color {color}")
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Mouse clicked at {event.pos}")
        
        # Essential for browser
        await asyncio.sleep(0)
        
        # Next frame
        frame += 1
        clock.tick(30)  # Limit to 30 FPS
    
    # Clean up
    pygame.quit()
    print("Debug complete!")
    return 0

if __name__ == "__main__":
    asyncio.run(main())
