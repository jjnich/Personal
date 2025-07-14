import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 12
        self.on_ground = False
        self.jumps_remaining = 2
        self.max_jumps = 2
        self.health = 100
        self.max_health = 100
        self.currency = 0
        self.weapon_type = "pistol"  # Default weapon
        self.weapon_level = 1
        self.weapon_damage = 10
        self.weapon_range = 150
        self.weapon_fire_rate = 10  # Lower = faster (frames between shots)
        self.weapon_projectile_size = 3
        self.weapon_accuracy = 8  # 1-10 scale
        self.weapon_reload_speed = 5  # Reload upgrade
        self.weapon_penetration = 1  # Bullets pierce through enemies
        self.last_shot_time = 0
        
    def update(self, platforms):
        # Apply gravity
        self.vel_y += 0.8
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            if player_rect.colliderect(platform):
                if self.vel_y > 0:  # Falling
                    self.y = platform.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.jumps_remaining = self.max_jumps  # Reset jumps when touching ground
                elif self.vel_y < 0:  # Jumping
                    self.y = platform.bottom
                    self.vel_y = 0
        
        # Keep player on screen
        if self.y > SCREEN_HEIGHT:
            self.health = 0
    
    def move(self, keys, w_pressed_this_frame):
        self.vel_x = 0
        if keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_d]:
            self.vel_x = self.speed
        if w_pressed_this_frame and self.jumps_remaining > 0:
            self.vel_y = -self.jump_power
            self.jumps_remaining -= 1
    
    def shoot(self, mouse_pos, camera_x, current_frame):
        # Calculate direction to mouse
        target_x = mouse_pos[0] + camera_x
        target_y = mouse_pos[1]
        
        dx = target_x - (self.x + self.width // 2)
        dy = target_y - (self.y + self.height // 2)
        
        # Always shoot toward mouse position, regardless of distance
        self.last_shot_time = current_frame
        return Bullet(self.x + self.width // 2, self.y + self.height // 2, dx, dy, self.weapon_damage, self.weapon_projectile_size)
    
    def upgrade_weapon_damage(self):
        cost = self.weapon_damage * 10
        if self.currency >= cost:
            self.currency -= cost
            self.weapon_damage += 5
            return True
        return False
    
    def upgrade_weapon_fire_rate(self):
        cost = (11 - self.weapon_fire_rate) * 20
        if self.currency >= cost and self.weapon_fire_rate > 3:
            self.currency -= cost
            self.weapon_fire_rate -= 1  # Lower = faster
            return True
        return False
    
    def upgrade_weapon_projectile_size(self):
        cost = self.weapon_projectile_size * 15
        if self.currency >= cost and self.weapon_projectile_size < 8:
            self.currency -= cost
            self.weapon_projectile_size += 1
            return True
        return False
    
    def upgrade_weapon_accuracy(self):
        cost = (11 - self.weapon_accuracy) * 25
        if self.currency >= cost and self.weapon_accuracy < 10:
            self.currency -= cost
            self.weapon_accuracy += 1
            return True
        return False
    
    def upgrade_weapon_reload_speed(self):
        cost = self.weapon_reload_speed * 30
        if self.currency >= cost and self.weapon_reload_speed < 10:
            self.currency -= cost
            self.weapon_reload_speed += 1
            return True
        return False
    
    def upgrade_weapon_penetration(self):
        cost = self.weapon_penetration * 50
        if self.currency >= cost and self.weapon_penetration < 5:
            self.currency -= cost
            self.weapon_penetration += 1
            return True
        return False
    
    def can_shoot(self, current_frame):
        return current_frame - self.last_shot_time >= self.weapon_fire_rate
    
    def draw(self, screen, camera_x):
        # Draw human-like character
        x = self.x - camera_x
        y = self.y
        
        # Head (circle)
        head_radius = 8
        head_x = x + self.width // 2
        head_y = y + head_radius
        pygame.draw.circle(screen, (255, 220, 177), (head_x, head_y), head_radius)  # Skin color
        
        # Eyes
        pygame.draw.circle(screen, BLACK, (head_x - 3, head_y - 2), 1)
        pygame.draw.circle(screen, BLACK, (head_x + 3, head_y - 2), 1)
        
        # Body (rectangle)
        body_width = 12
        body_height = 18
        body_x = x + (self.width - body_width) // 2
        body_y = y + head_radius * 2
        pygame.draw.rect(screen, (0, 100, 200), (body_x, body_y, body_width, body_height))  # Blue shirt
        
        # Arms
        arm_width = 3
        arm_height = 12
        # Left arm
        pygame.draw.rect(screen, (255, 220, 177), (body_x - arm_width, body_y + 2, arm_width, arm_height))
        # Right arm  
        pygame.draw.rect(screen, (255, 220, 177), (body_x + body_width, body_y + 2, arm_width, arm_height))
        
        # Legs
        leg_width = 4
        leg_height = 12
        # Left leg
        pygame.draw.rect(screen, (50, 50, 50), (body_x + 2, body_y + body_height, leg_width, leg_height))  # Dark pants
        # Right leg
        pygame.draw.rect(screen, (50, 50, 50), (body_x + body_width - leg_width - 2, body_y + body_height, leg_width, leg_height))
        
        # Health bar
        health_width = 50
        health_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x - camera_x, self.y - 15, health_width, health_height))
        pygame.draw.rect(screen, GREEN, (self.x - camera_x, self.y - 15, health_width * health_ratio, health_height))

class Bullet:
    def __init__(self, x, y, dx, dy, damage, size=3):
        self.x = x
        self.y = y
        self.damage = damage
        self.size = size
        self.speed = 10
        
        # Normalize direction
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
        else:
            self.vel_x = self.vel_y = 0
        
        self.lifetime = 60  # Frames
    
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, YELLOW, (int(self.x - camera_x), int(self.y)), self.size)
        # Add glow effect for larger projectiles
        if self.size > 3:
            pygame.draw.circle(screen, (255, 255, 150), (int(self.x - camera_x), int(self.y)), self.size + 2, 2)

class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.type = enemy_type
        self.vel_x = 0
        self.vel_y = 0
        self.speed = random.uniform(1, 2)
        self.direction = random.choice([-1, 1])
        
        if enemy_type == "basic":
            self.health = 20
            self.damage = 10
            self.currency_value = 10
            self.color = RED
        elif enemy_type == "fast":
            self.health = 15
            self.damage = 8
            self.currency_value = 15
            self.color = PURPLE
            self.speed = 3
        elif enemy_type == "tank":
            self.health = 50
            self.damage = 20
            self.currency_value = 25
            self.color = GRAY
            self.speed = 0.5
    
    def update(self, platforms, player):
        # Simple AI - move toward player
        if abs(self.x - player.x) < 200:
            if self.x < player.x:
                self.vel_x = self.speed
            else:
                self.vel_x = -self.speed
        else:
            self.vel_x = self.direction * self.speed
        
        # Apply gravity
        self.vel_y += 0.8
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for platform in platforms:
            if enemy_rect.colliderect(platform):
                if self.vel_y > 0:
                    self.y = platform.top - self.height
                    self.vel_y = 0
        
        # Change direction at edges
        if self.y > SCREEN_HEIGHT - 100:
            self.direction *= -1
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
    
    def draw(self, screen, camera_x):
        x = self.x - camera_x
        y = self.y
        
        if self.type == "basic":
            # Basic monster - blob-like with spikes
            # Main body
            pygame.draw.ellipse(screen, self.color, (x, y + 5, self.width, self.height - 5))
            # Spikes on top
            spike_points = [
                (x + 5, y + 5), (x + 8, y), (x + 11, y + 5),
                (x + 14, y + 5), (x + 17, y), (x + 20, y + 5)
            ]
            pygame.draw.polygon(screen, (150, 0, 0), spike_points)
            # Eyes
            pygame.draw.circle(screen, BLACK, (x + 8, y + 12), 2)
            pygame.draw.circle(screen, BLACK, (x + 17, y + 12), 2)
            # Mouth
            pygame.draw.arc(screen, BLACK, (x + 6, y + 15, 13, 8), 0, 3.14, 2)
            
        elif self.type == "fast":
            # Fast monster - spider-like with long legs
            # Body
            pygame.draw.ellipse(screen, self.color, (x + 5, y + 8, self.width - 10, self.height - 8))
            # Spider legs
            leg_points = [
                # Left legs
                (x + 2, y + 10), (x - 3, y + 5),
                (x + 2, y + 15), (x - 3, y + 20),
                # Right legs  
                (x + self.width - 2, y + 10), (x + self.width + 3, y + 5),
                (x + self.width - 2, y + 15), (x + self.width + 3, y + 20)
            ]
            for i in range(0, len(leg_points), 2):
                pygame.draw.line(screen, BLACK, leg_points[i], leg_points[i + 1], 2)
            # Multiple eyes
            pygame.draw.circle(screen, RED, (x + 8, y + 12), 1)
            pygame.draw.circle(screen, RED, (x + 12, y + 12), 1) 
            pygame.draw.circle(screen, RED, (x + 16, y + 12), 1)
            pygame.draw.circle(screen, RED, (x + 10, y + 15), 1)
            pygame.draw.circle(screen, RED, (x + 14, y + 15), 1)
            
        elif self.type == "tank":
            # Tank monster - armored with horns
            # Main armored body
            pygame.draw.rect(screen, self.color, (x, y + 3, self.width, self.height - 3))
            # Armor plates
            for i in range(3):
                plate_y = y + 5 + i * 6
                pygame.draw.rect(screen, (100, 100, 100), (x + 2, plate_y, self.width - 4, 4))
            # Horns
            horn_points = [
                (x + 3, y + 3), (x + 6, y - 2), (x + 9, y + 3),
                (x + 16, y + 3), (x + 19, y - 2), (x + 22, y + 3)
            ]
            pygame.draw.polygon(screen, (80, 80, 80), horn_points[:3])
            pygame.draw.polygon(screen, (80, 80, 80), horn_points[3:])
            # Glowing red eyes
            pygame.draw.circle(screen, (255, 50, 50), (x + 8, y + 10), 3)
            pygame.draw.circle(screen, (255, 50, 50), (x + 17, y + 10), 3)
            pygame.draw.circle(screen, WHITE, (x + 8, y + 10), 1)
            pygame.draw.circle(screen, WHITE, (x + 17, y + 10), 1)

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 100
        self.health = 500
        self.max_health = 500
        self.damage = 30
        self.speed = 2
        self.attack_timer = 0
        self.currency_value = 200
        
    def update(self, player):
        # Move toward player
        if self.x < player.x:
            self.x += self.speed
        else:
            self.x -= self.speed
        
        self.attack_timer += 1
        
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
        
    def draw(self, screen, camera_x):
        x = self.x - camera_x
        y = self.y
        
        # Main boss body - large demon-like creature
        # Body segments
        pygame.draw.ellipse(screen, (64, 0, 64), (x, y + 20, self.width, self.height - 20))
        pygame.draw.ellipse(screen, (96, 0, 96), (x + 10, y + 30, self.width - 20, self.height - 40))
        
        # Head
        head_width = 50
        head_height = 40
        head_x = x + (self.width - head_width) // 2
        pygame.draw.ellipse(screen, (80, 0, 80), (head_x, y, head_width, head_height))
        
        # Horns
        horn_size = 15
        pygame.draw.polygon(screen, BLACK, [
            (head_x + 8, y + 5), (head_x + 3, y - horn_size), (head_x + 13, y + 8)
        ])
        pygame.draw.polygon(screen, BLACK, [
            (head_x + head_width - 8, y + 5), (head_x + head_width - 3, y - horn_size), (head_x + head_width - 13, y + 8)
        ])
        
        # Eyes - glowing red
        eye_size = 6
        pygame.draw.circle(screen, (255, 0, 0), (head_x + 12, y + 15), eye_size)
        pygame.draw.circle(screen, (255, 0, 0), (head_x + head_width - 12, y + 15), eye_size)
        pygame.draw.circle(screen, (255, 150, 150), (head_x + 12, y + 15), eye_size - 2)
        pygame.draw.circle(screen, (255, 150, 150), (head_x + head_width - 12, y + 15), eye_size - 2)
        pygame.draw.circle(screen, WHITE, (head_x + 12, y + 15), 2)
        pygame.draw.circle(screen, WHITE, (head_x + head_width - 12, y + 15), 2)
        
        # Menacing mouth
        mouth_points = [
            (head_x + 15, y + 25), (head_x + 25, y + 35), (head_x + 35, y + 25),
            (head_x + 30, y + 30), (head_x + 20, y + 30)
        ]
        pygame.draw.polygon(screen, BLACK, mouth_points)
        
        # Teeth
        for i in range(3):
            tooth_x = head_x + 18 + i * 6
            pygame.draw.polygon(screen, WHITE, [
                (tooth_x, y + 25), (tooth_x + 2, y + 30), (tooth_x + 4, y + 25)
            ])
        
        # Arms/claws
        # Left arm
        pygame.draw.ellipse(screen, (64, 0, 64), (x - 15, y + 40, 20, 45))
        # Left claws
        for i in range(3):
            claw_x = x - 10 + i * 3
            pygame.draw.polygon(screen, (200, 200, 200), [
                (claw_x, y + 80), (claw_x + 1, y + 90), (claw_x + 2, y + 80)
            ])
        
        # Right arm  
        pygame.draw.ellipse(screen, (64, 0, 64), (x + self.width - 5, y + 40, 20, 45))
        # Right claws
        for i in range(3):
            claw_x = x + self.width + i * 3
            pygame.draw.polygon(screen, (200, 200, 200), [
                (claw_x, y + 80), (claw_x + 1, y + 90), (claw_x + 2, y + 80)
            ])
        
        # Pulsing aura effect based on attack timer
        if self.attack_timer % 30 < 15:  # Pulse every 30 frames
            aura_color = (128, 0, 128, 50)  # Semi-transparent purple
            pygame.draw.ellipse(screen, (100, 0, 100), (x - 5, y - 5, self.width + 10, self.height + 10), 3)
        
        # Health bar
        health_width = 100
        health_height = 8
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x - camera_x, self.y - 20, health_width, health_height))
        pygame.draw.rect(screen, GREEN, (self.x - camera_x, self.y - 20, health_width * health_ratio, health_height))

class LevelGenerator:
    def __init__(self):
        self.platforms = []
        self.enemies = []
        self.level = 1
        self.boss = None
        self.world_x = 0  # Track how far the world extends
        self.last_platform_x = 0
        self.enemies_per_level = 5
        
    def generate_initial_level(self):
        self.platforms.clear()
        self.enemies.clear()
        self.level = 1
        self.boss = None
        self.world_x = 0
        
        # Generate initial ground and platforms
        self.generate_segment(0, 2000)
        
    def generate_segment(self, start_x, end_x):
        # Generate ground for this segment
        for x in range(start_x, end_x, 100):
            self.platforms.append(pygame.Rect(x, SCREEN_HEIGHT - 50, 100, 50))
        
        # Generate reachable platforms in a path-like structure
        if start_x == 0:
            current_x = 300
            current_y = SCREEN_HEIGHT - 150
        else:
            # Continue from where we left off
            current_x = start_x + 200
            current_y = SCREEN_HEIGHT - 150
        
        segment_platforms = int((end_x - start_x) / 120)  # Roughly one platform every 120 pixels
        
        for i in range(segment_platforms):
            # Create platform
            width = random.randint(100, 180)
            self.platforms.append(pygame.Rect(current_x, current_y, width, 20))
            
            # Calculate next platform position (ensure it's reachable)
            jump_distance_x = random.randint(80, 140)  # Horizontal jump distance
            jump_distance_y = random.randint(-80, 40)   # Vertical jump distance (-80 up, +40 down)
            
            current_x += jump_distance_x
            current_y += jump_distance_y
            
            # Keep platforms within reasonable bounds
            current_y = max(150, min(current_y, SCREEN_HEIGHT - 100))
            
            # Don't go past the segment end
            if current_x >= end_x - 200:
                break
            
            # Add some random platforms for variety
            if i % 3 == 0 and current_x < end_x - 300:
                extra_x = current_x + random.randint(-100, 100)
                extra_y = current_y + random.randint(-60, 60)
                extra_y = max(150, min(extra_y, SCREEN_HEIGHT - 100))
                extra_width = random.randint(80, 120)
                if extra_x < end_x - 100:  # Make sure it fits in segment
                    self.platforms.append(pygame.Rect(extra_x, extra_y, extra_width, 20))
        
        self.last_platform_x = current_x
        
        # Generate enemies for this segment
        enemy_count = random.randint(3, 6)
        for i in range(enemy_count):
            x = random.randint(start_x + 200, end_x - 200)
            y = 100
            
            # Higher levels have more difficult enemies
            if self.level >= 7:
                enemy_type = random.choice(["basic", "fast", "tank"])
            elif self.level >= 4:
                enemy_type = random.choice(["basic", "fast"])
            else:
                enemy_type = "basic"
                
            self.enemies.append(Enemy(x, y, enemy_type))
        
        # Update world extent
        self.world_x = max(self.world_x, end_x)
        
    def check_and_generate_ahead(self, player_x):
        # Generate new segment if player is getting close to the edge
        if player_x > self.world_x - 800:  # Generate when player is 800 pixels from edge
            segment_start = self.world_x
            segment_end = self.world_x + 1500  # Generate 1500 pixel segments
            self.generate_segment(segment_start, segment_end)
            
            # Check if we should advance to next level
            enemies_in_current_area = [e for e in self.enemies if e.x < player_x + 400]
            if len(enemies_in_current_area) == 0 and self.level < 10:
                self.level += 1
                if self.level == 10:
                    # Generate boss instead of regular enemies
                    self.boss = Boss(self.world_x - 500, SCREEN_HEIGHT - 150)
    
    def cleanup_distant_objects(self, player_x):
        # Remove platforms and enemies that are too far behind the player
        cleanup_distance = 1000
        
        self.platforms = [p for p in self.platforms if p.x > player_x - cleanup_distance]
        self.enemies = [e for e in self.enemies if e.x > player_x - cleanup_distance]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.player = Player(100, SCREEN_HEIGHT - 100)
        self.level_gen = LevelGenerator()
        self.bullets = []
        self.camera_x = 0
        self.game_state = "main_menu"  # "main_menu", "weapon_select", "playing", "game_over", "victory", "paused"
        self.pause_menu_selection = 0  # 0=resume, 1=upgrades, 2=quit
        self.upgrade_menu_selection = 0  # 0=damage, 1=fire_rate, 2=projectile_size, etc.
        self.weapon_select_selection = 0  # For weapon selection screen
        self.main_menu_selection = 0  # 0=start game, 1=quit
        self.in_upgrade_menu = False
        self.frame_count = 0
        self.mouse_held = False
        
        # Weapon types and their base stats
        self.weapon_types = {
            "pistol": {"name": "Pistol", "damage": 10, "fire_rate": 8, "accuracy": 9, "size": 3, "description": "Balanced and reliable"},
            "rifle": {"name": "Rifle", "damage": 15, "fire_rate": 12, "accuracy": 10, "size": 2, "description": "High damage, slower fire"},
            "smg": {"name": "SMG", "damage": 6, "fire_rate": 4, "accuracy": 6, "size": 2, "description": "Fast fire rate, lower damage"},
            "shotgun": {"name": "Shotgun", "damage": 20, "fire_rate": 20, "accuracy": 4, "size": 5, "description": "Devastating close range"}
        }
        
        # Don't generate level until weapon is selected
        if self.game_state == "playing":
            self.level_gen.generate_initial_level()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game_state == "playing":
                        if self.player.can_shoot(self.frame_count):
                            bullet = self.player.shoot(pygame.mouse.get_pos(), self.camera_x, self.frame_count)
                            if bullet:
                                self.bullets.append(bullet)
                        self.mouse_held = True
                    elif self.game_state == "paused":
                        self.handle_mouse_click(event.pos)
                    elif self.game_state == "weapon_select":
                        self.handle_weapon_select_click(event.pos)
                    elif self.game_state == "main_menu":
                        self.handle_main_menu_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_held = False
            elif event.type == pygame.MOUSEMOTION:
                if self.game_state == "paused":
                    self.handle_mouse_hover(event.pos)
                elif self.game_state == "weapon_select":
                    self.handle_weapon_select_hover(event.pos)
                elif self.game_state == "main_menu":
                    self.handle_main_menu_hover(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                    elif self.game_state == "paused":
                        if self.in_upgrade_menu:
                            self.in_upgrade_menu = False
                        else:
                            self.game_state = "playing"
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Reset cursor
                elif self.game_state == "paused":
                    self.handle_pause_menu_input(event.key)
                elif event.key == pygame.K_r and self.game_state not in ["playing", "paused"]:  # Restart
                    self.__init__()
    
    def handle_pause_menu_input(self, key):
        if not self.in_upgrade_menu:
            # Main pause menu
            if key == pygame.K_UP or key == pygame.K_w:
                self.pause_menu_selection = (self.pause_menu_selection - 1) % 3
            elif key == pygame.K_DOWN or key == pygame.K_s:
                self.pause_menu_selection = (self.pause_menu_selection + 1) % 3
            elif key == pygame.K_RETURN or key == pygame.K_SPACE:
                if self.pause_menu_selection == 0:  # Resume
                    self.game_state = "playing"
                elif self.pause_menu_selection == 1:  # Upgrades
                    self.in_upgrade_menu = True
                elif self.pause_menu_selection == 2:  # Quit
                    self.running = False
        else:
            # Upgrade menu
            if key == pygame.K_UP or key == pygame.K_w:
                self.upgrade_menu_selection = (self.upgrade_menu_selection - 1) % 4
            elif key == pygame.K_DOWN or key == pygame.K_s:
                self.upgrade_menu_selection = (self.upgrade_menu_selection + 1) % 4
            elif key == pygame.K_RETURN or key == pygame.K_SPACE:
                if self.upgrade_menu_selection == 0:  # Damage
                    self.player.upgrade_weapon_damage()
                elif self.upgrade_menu_selection == 1:  # Fire Rate
                    self.player.upgrade_weapon_fire_rate()
                elif self.upgrade_menu_selection == 2:  # Projectile Size
                    self.player.upgrade_weapon_projectile_size()
                elif self.upgrade_menu_selection == 3:  # Back
                    self.in_upgrade_menu = False
    
    def handle_mouse_hover(self, mouse_pos):
        mouse_over_option = False
        
        if not self.in_upgrade_menu:
            # Main pause menu hover detection
            menu_width = 400
            menu_height = 350
            menu_x = SCREEN_WIDTH//2 - menu_width//2
            menu_y = SCREEN_HEIGHT//2 - menu_height//2
            
            for i in range(3):  # 3 menu options
                option_y = SCREEN_HEIGHT//2 - 30 + i * 60
                option_rect = pygame.Rect(menu_x + 20, option_y - 10, menu_width - 40, 50)
                if option_rect.collidepoint(mouse_pos):
                    self.pause_menu_selection = i
                    mouse_over_option = True
                    break
        else:
            # Upgrade menu hover detection
            upgrade_width = 600
            upgrade_height = 450
            upgrade_x = SCREEN_WIDTH//2 - upgrade_width//2
            upgrade_y = SCREEN_HEIGHT//2 - upgrade_height//2
            
            for i in range(4):  # 4 upgrade options
                option_y = upgrade_y + 160 + i * 70
                option_rect = pygame.Rect(upgrade_x + 30, option_y - 15, upgrade_width - 60, 60)
                if option_rect.collidepoint(mouse_pos):
                    self.upgrade_menu_selection = i
                    mouse_over_option = True
                    break
        
        # Change cursor based on hover state
        if mouse_over_option:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def handle_mouse_click(self, mouse_pos):
        if not self.in_upgrade_menu:
            # Main pause menu click detection
            menu_width = 400
            menu_height = 350
            menu_x = SCREEN_WIDTH//2 - menu_width//2
            menu_y = SCREEN_HEIGHT//2 - menu_height//2
            
            for i in range(3):  # 3 menu options
                option_y = SCREEN_HEIGHT//2 - 30 + i * 60
                option_rect = pygame.Rect(menu_x + 20, option_y - 10, menu_width - 40, 50)
                if option_rect.collidepoint(mouse_pos):
                    if i == 0:  # Resume
                        self.game_state = "playing"
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Reset cursor
                    elif i == 1:  # Upgrades
                        self.in_upgrade_menu = True
                    elif i == 2:  # Quit
                        self.running = False
                    break
        else:
            # Upgrade menu click detection
            upgrade_width = 600
            upgrade_height = 450
            upgrade_x = SCREEN_WIDTH//2 - upgrade_width//2
            upgrade_y = SCREEN_HEIGHT//2 - upgrade_height//2
            
            for i in range(4):  # 4 upgrade options
                option_y = upgrade_y + 160 + i * 70
                option_rect = pygame.Rect(upgrade_x + 30, option_y - 15, upgrade_width - 60, 60)
                if option_rect.collidepoint(mouse_pos):
                    if i == 0:  # Damage
                        self.player.upgrade_weapon_damage()
                    elif i == 1:  # Fire Rate
                        self.player.upgrade_weapon_fire_rate()
                    elif i == 2:  # Projectile Size
                        self.player.upgrade_weapon_projectile_size()
                    elif i == 3:  # Back
                        self.in_upgrade_menu = False
                    break
    
    def update(self):
        self.frame_count += 1
        
        if self.game_state != "playing":
            return
        
        # Handle continuous firing
        if self.mouse_held and self.player.can_shoot(self.frame_count):
            bullet = self.player.shoot(pygame.mouse.get_pos(), self.camera_x, self.frame_count)
            if bullet:
                self.bullets.append(bullet)
            
        keys = pygame.key.get_pressed()
        # Handle W key press for double jump
        w_pressed_this_frame = False
        if keys[pygame.K_w] and not hasattr(self, 'w_was_pressed'):
            self.w_was_pressed = False
        
        if keys[pygame.K_w] and not self.w_was_pressed:
            w_pressed_this_frame = True
        
        self.w_was_pressed = keys[pygame.K_w]
        
        self.player.move(keys, w_pressed_this_frame)
        self.player.update(self.level_gen.platforms)
        
        # Update camera
        self.camera_x = self.player.x - SCREEN_WIDTH // 3
        self.camera_x = max(0, self.camera_x)
        
        # Update bullets
        self.bullets = [bullet for bullet in self.bullets if bullet.update()]
        
        # Update enemies
        for enemy in self.level_gen.enemies[:]:
            enemy.update(self.level_gen.platforms, self.player)
            
            # Player-enemy collision
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                self.player.health -= enemy.damage * 0.1  # Damage over time
            
            # Bullet-enemy collision
            for bullet in self.bullets[:]:
                bullet_rect = pygame.Rect(bullet.x - bullet.size, bullet.y - bullet.size, bullet.size * 2, bullet.size * 2)
                if bullet_rect.colliderect(enemy_rect):
                    if enemy.take_damage(bullet.damage):
                        self.player.currency += enemy.currency_value
                        self.level_gen.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    break
        
        # Update boss
        if self.level_gen.boss:
            self.level_gen.boss.update(self.player)
            
            # Player-boss collision
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            boss_rect = pygame.Rect(self.level_gen.boss.x, self.level_gen.boss.y, self.level_gen.boss.width, self.level_gen.boss.height)
            if player_rect.colliderect(boss_rect):
                self.player.health -= self.level_gen.boss.damage * 0.1
            
            # Bullet-boss collision
            for bullet in self.bullets[:]:
                bullet_rect = pygame.Rect(bullet.x - bullet.size, bullet.y - bullet.size, bullet.size * 2, bullet.size * 2)
                if bullet_rect.colliderect(boss_rect):
                    if self.level_gen.boss.take_damage(bullet.damage):
                        self.player.currency += self.level_gen.boss.currency_value
                        self.game_state = "victory"
                    self.bullets.remove(bullet)
                    break
        
        # Continuous level generation
        self.level_gen.check_and_generate_ahead(self.player.x)
        self.level_gen.cleanup_distant_objects(self.player.x)
        
        # Check game over
        if self.player.health <= 0:
            self.game_state = "game_over"
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw platforms
        for platform in self.level_gen.platforms:
            if platform.x - self.camera_x > -100 and platform.x - self.camera_x < SCREEN_WIDTH + 100:
                pygame.draw.rect(self.screen, BROWN, (platform.x - self.camera_x, platform.y, platform.width, platform.height))
        
        # Draw player
        self.player.draw(self.screen, self.camera_x)
        
        # Draw enemies
        for enemy in self.level_gen.enemies:
            enemy.draw(self.screen, self.camera_x)
        
        # Draw boss
        if self.level_gen.boss:
            self.level_gen.boss.draw(self.screen, self.camera_x)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen, self.camera_x)
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        
        # Currency and weapon info
        currency_text = font.render(f"Currency: {self.player.currency}", True, WHITE)
        damage_text = font.render(f"Damage: {self.player.weapon_damage}", True, WHITE)
        fire_rate_text = font.render(f"Fire Rate: {11 - self.player.weapon_fire_rate}/10", True, WHITE)
        projectile_text = font.render(f"Projectile Size: {self.player.weapon_projectile_size}", True, WHITE)
        level_text = font.render(f"Level: {self.level_gen.level}", True, WHITE)
        pause_text = font.render("Press ESC to pause", True, WHITE)
        
        self.screen.blit(currency_text, (10, 10))
        self.screen.blit(damage_text, (10, 50))
        self.screen.blit(fire_rate_text, (10, 90))
        self.screen.blit(projectile_text, (10, 130))
        self.screen.blit(level_text, (10, 170))
        self.screen.blit(pause_text, (10, 210))
        
        # Game over/victory screen
        if self.game_state == "game_over":
            game_over_text = pygame.font.Font(None, 72).render("GAME OVER", True, RED)
            restart_text = font.render("Press R to restart", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))
        elif self.game_state == "victory":
            victory_text = pygame.font.Font(None, 72).render("VICTORY!", True, GREEN)
            restart_text = font.render("Press R to restart", True, WHITE)
            self.screen.blit(victory_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20))
        elif self.game_state == "paused":
            # Semi-transparent overlay with gradient effect
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((20, 20, 40))  # Dark blue tint
            self.screen.blit(overlay, (0, 0))
            
            if not self.in_upgrade_menu:
                # Main pause menu with styled box
                menu_width = 400
                menu_height = 350
                menu_x = SCREEN_WIDTH//2 - menu_width//2
                menu_y = SCREEN_HEIGHT//2 - menu_height//2
                
                # Menu background with gradient
                menu_bg = pygame.Surface((menu_width, menu_height))
                menu_bg.fill((40, 40, 80))
                menu_bg.set_alpha(220)
                self.screen.blit(menu_bg, (menu_x, menu_y))
                
                # Menu border
                pygame.draw.rect(self.screen, (100, 150, 255), (menu_x - 3, menu_y - 3, menu_width + 6, menu_height + 6), 3)
                pygame.draw.rect(self.screen, (200, 200, 255), (menu_x - 1, menu_y - 1, menu_width + 2, menu_height + 2), 1)
                
                # Title with shadow effect
                title_font = pygame.font.Font(None, 84)
                pause_shadow = title_font.render("PAUSED", True, (20, 20, 20))
                pause_title = title_font.render("PAUSED", True, (255, 255, 100))
                self.screen.blit(pause_shadow, (SCREEN_WIDTH//2 - 115, SCREEN_HEIGHT//2 - 130))
                self.screen.blit(pause_title, (SCREEN_WIDTH//2 - 117, SCREEN_HEIGHT//2 - 132))
                
                # Menu options with better styling
                menu_options = ["Resume Game", "Weapon Upgrades", "Quit to Desktop"]
                option_font = pygame.font.Font(None, 48)
                
                for i, option in enumerate(menu_options):
                    option_y = SCREEN_HEIGHT//2 - 30 + i * 60
                    
                    # Highlight selected option
                    if i == self.pause_menu_selection:
                        # Selection background
                        select_rect = pygame.Rect(menu_x + 20, option_y - 10, menu_width - 40, 50)
                        pygame.draw.rect(self.screen, (100, 150, 255), select_rect)
                        pygame.draw.rect(self.screen, (150, 200, 255), select_rect, 2)
                        
                        color = WHITE
                        # Add arrow indicator
                        arrow_points = [
                            (menu_x + 30, option_y + 15),
                            (menu_x + 45, option_y + 25),
                            (menu_x + 30, option_y + 35)
                        ]
                        pygame.draw.polygon(self.screen, (255, 255, 100), arrow_points)
                    else:
                        color = (200, 200, 200)
                    
                    option_text = option_font.render(option, True, color)
                    self.screen.blit(option_text, (menu_x + 60, option_y))
                
                # Controls help with icon-style text
                controls_font = pygame.font.Font(None, 28)
            else:
                # Upgrade menu with enhanced styling
                upgrade_width = 600
                upgrade_height = 450
                upgrade_x = SCREEN_WIDTH//2 - upgrade_width//2
                upgrade_y = SCREEN_HEIGHT//2 - upgrade_height//2
                
                # Upgrade menu background
                upgrade_bg = pygame.Surface((upgrade_width, upgrade_height))
                upgrade_bg.fill((30, 50, 80))
                upgrade_bg.set_alpha(240)
                self.screen.blit(upgrade_bg, (upgrade_x, upgrade_y))
                
                # Upgrade menu border with double line
                pygame.draw.rect(self.screen, (150, 100, 255), (upgrade_x - 4, upgrade_y - 4, upgrade_width + 8, upgrade_height + 8), 4)
                pygame.draw.rect(self.screen, (200, 150, 255), (upgrade_x - 1, upgrade_y - 1, upgrade_width + 2, upgrade_height + 2), 1)
                
                # Title with glow effect
                title_font = pygame.font.Font(None, 84)
                upgrade_shadow = title_font.render("WEAPON UPGRADES", True, (40, 20, 40))
                upgrade_title = title_font.render("WEAPON UPGRADES", True, (255, 200, 100))
                self.screen.blit(upgrade_shadow, (SCREEN_WIDTH//2 - 225, upgrade_y + 25))
                self.screen.blit(upgrade_title, (SCREEN_WIDTH//2 - 227, upgrade_y + 23))
                
                # Currency display with coin icon
                currency_font = pygame.font.Font(None, 42)
                currency_bg = pygame.Rect(upgrade_x + 20, upgrade_y + 90, upgrade_width - 40, 40)
                pygame.draw.rect(self.screen, (80, 120, 40), currency_bg)
                pygame.draw.rect(self.screen, (120, 180, 60), currency_bg, 2)
                
                # Coin icon
                pygame.draw.circle(self.screen, (255, 215, 0), (upgrade_x + 45, upgrade_y + 110), 12)
                pygame.draw.circle(self.screen, (255, 255, 100), (upgrade_x + 45, upgrade_y + 110), 8)
                
                currency_text = currency_font.render(f"Currency: {self.player.currency}", True, WHITE)
                self.screen.blit(currency_text, (upgrade_x + 70, upgrade_y + 95))
                
                # Upgrade options with enhanced styling
                damage_cost = self.player.weapon_damage * 10
                fire_rate_cost = (11 - self.player.weapon_fire_rate) * 20
                projectile_cost = self.player.weapon_projectile_size * 15
                
                upgrade_data = [
                    ("⚔ Damage", self.player.weapon_damage, damage_cost, (255, 100, 100)),
                    ("⚡ Fire Rate", f"{11 - self.player.weapon_fire_rate}/10", fire_rate_cost, (100, 255, 100)),
                    ("💥 Projectile Size", self.player.weapon_projectile_size, projectile_cost, (100, 100, 255)),
                    ("← Back", "", 0, (200, 200, 200))
                ]
                
                option_font = pygame.font.Font(None, 36)
                stat_font = pygame.font.Font(None, 28)
                
                for i, (name, current_val, cost, base_color) in enumerate(upgrade_data):
                    option_y = upgrade_y + 160 + i * 70
                    
                    # Option background
                    option_rect = pygame.Rect(upgrade_x + 30, option_y - 15, upgrade_width - 60, 60)
                    
                    if i == self.upgrade_menu_selection:
                        # Selected option styling
                        pygame.draw.rect(self.screen, (80, 80, 120), option_rect)
                        pygame.draw.rect(self.screen, (150, 150, 200), option_rect, 3)
                        text_color = WHITE
                        
                        # Selection arrow
                        arrow_points = [
                            (upgrade_x + 40, option_y + 10),
                            (upgrade_x + 55, option_y + 20),
                            (upgrade_x + 40, option_y + 30)
                        ]
                        pygame.draw.polygon(self.screen, (255, 255, 100), arrow_points)
                    else:
                        # Unselected option styling
                        pygame.draw.rect(self.screen, (50, 50, 70), option_rect)
                        pygame.draw.rect(self.screen, (100, 100, 130), option_rect, 1)
                        
                        # Check affordability
                        if i < 3 and self.player.currency < cost:
                            text_color = (120, 120, 120)  # Grayed out
                            base_color = (80, 80, 80)
                        else:
                            text_color = (220, 220, 220)
                    
                    # Draw option text
                    option_text = option_font.render(name, True, text_color)
                    self.screen.blit(option_text, (upgrade_x + 70, option_y - 5))
                    
                    # Draw current value and cost for upgrade options
                    if i < 3:
                        current_text = stat_font.render(f"Current: {current_val}", True, base_color)
                        cost_text = stat_font.render(f"Cost: {cost}", True, (255, 215, 0))
                        self.screen.blit(current_text, (upgrade_x + 70, option_y + 20))
                        self.screen.blit(cost_text, (upgrade_x + 300, option_y + 20))
                        
                        # Affordability indicator
                        if self.player.currency >= cost:
                            pygame.draw.circle(self.screen, (0, 255, 0), (upgrade_x + 500, option_y + 20), 8)
                            pygame.draw.circle(self.screen, WHITE, (upgrade_x + 500, option_y + 20), 5)
                        else:
                            pygame.draw.circle(self.screen, (255, 0, 0), (upgrade_x + 500, option_y + 20), 8)
                            pygame.draw.line(self.screen, WHITE, (upgrade_x + 495, option_y + 15), (upgrade_x + 505, option_y + 25), 2)
                
                # Enhanced controls help
                controls_font = pygame.font.Font(None, 28)
                controls_bg = pygame.Rect(upgrade_x + 20, upgrade_y + upgrade_height - 50, upgrade_width - 40, 30)
                pygame.draw.rect(self.screen, (40, 40, 60), controls_bg)
        elif self.game_state == "main_menu":
            # Main menu background
            self.screen.fill((20, 30, 50))
            
            # Main menu
            menu_width = 400
            menu_height = 300
            menu_x = SCREEN_WIDTH//2 - menu_width//2
            menu_y = SCREEN_HEIGHT//2 - menu_height//2
            
            # Menu background
            menu_bg = pygame.Surface((menu_width, menu_height))
            menu_bg.fill((40, 60, 100))
            menu_bg.set_alpha(220)
            self.screen.blit(menu_bg, (menu_x, menu_y))
            
            # Menu border
            pygame.draw.rect(self.screen, (100, 150, 255), (menu_x - 3, menu_y - 3, menu_width + 6, menu_height + 6), 3)
            
            # Title
            title_font = pygame.font.Font(None, 84)
            title_text = title_font.render("PLATFORMER", True, (255, 255, 100))
            self.screen.blit(title_text, (SCREEN_WIDTH//2 - 160, menu_y + 30))
            
            # Menu options
            menu_options = ["Start Game", "Quit Game"]
            option_font = pygame.font.Font(None, 48)
            
            for i, option in enumerate(menu_options):
                option_y = menu_y + 150 + i * 60
                
                # Highlight selected option
                if i == self.main_menu_selection:
                    select_rect = pygame.Rect(menu_x + 50, option_y - 15, menu_width - 100, 50)
                    pygame.draw.rect(self.screen, (100, 150, 255), select_rect)
                    color = WHITE
                else:
                    color = (200, 200, 200)
                
                option_text = option_font.render(option, True, color)
                self.screen.blit(option_text, (menu_x + 80, option_y))
        elif self.game_state == "weapon_select":
            # Weapon selection screen
            self.screen.fill((30, 20, 50))
            
            select_width = 800
            select_height = 600
            select_x = SCREEN_WIDTH//2 - select_width//2
            select_y = SCREEN_HEIGHT//2 - select_height//2
            
            # Selection background
            select_bg = pygame.Surface((select_width, select_height))
            select_bg.fill((50, 40, 80))
            select_bg.set_alpha(240)
            self.screen.blit(select_bg, (select_x, select_y))
            
            # Selection border
            pygame.draw.rect(self.screen, (150, 100, 255), (select_x - 4, select_y - 4, select_width + 8, select_height + 8), 4)
            
            # Title
            title_font = pygame.font.Font(None, 84)
            title_text = title_font.render("SELECT WEAPON", True, (255, 200, 100))
            self.screen.blit(title_text, (SCREEN_WIDTH//2 - 200, select_y + 30))
            
            # Weapon options
            weapons = list(self.weapon_types.keys())
            weapon_font = pygame.font.Font(None, 42)
            stat_font = pygame.font.Font(None, 28)
            
            for i, weapon in enumerate(weapons):
                weapon_stats = self.weapon_types[weapon]
                weapon_y = select_y + 150 + i * 100
                
                # Highlight selected weapon
                if i == self.weapon_select_selection:
                    weapon_rect = pygame.Rect(select_x + 50, weapon_y - 20, select_width - 100, 80)
                    pygame.draw.rect(self.screen, (100, 150, 255), weapon_rect)
                    pygame.draw.rect(self.screen, (150, 200, 255), weapon_rect, 2)
                    color = WHITE
                else:
                    color = (200, 200, 200)
                
                # Weapon name
                weapon_text = weapon_font.render(weapon.title(), True, color)
                self.screen.blit(weapon_text, (select_x + 70, weapon_y - 10))
                
                # Weapon stats
                stats_text = f"Damage: {weapon_stats['damage']} | Fire Rate: {weapon_stats['fire_rate']} | Size: {weapon_stats['size']}"
                stats_surface = stat_font.render(stats_text, True, (180, 180, 180))
                self.screen.blit(stats_surface, (select_x + 70, weapon_y + 25))
        
        pygame.display.flip()
    
    def select_weapon(self, weapon_key):
        weapon_stats = self.weapon_types[weapon_key]
        self.player.weapon_type = weapon_key
        self.player.weapon_damage = weapon_stats["damage"]
        self.player.weapon_fire_rate = weapon_stats["fire_rate"]
        self.player.weapon_accuracy = weapon_stats["accuracy"]
        self.player.weapon_projectile_size = weapon_stats["size"]
        self.game_state = "playing"
        self.level_gen.generate_initial_level()
    
    def handle_weapon_select_hover(self, mouse_pos):
        select_width = 800
        select_height = 600
        select_x = SCREEN_WIDTH//2 - select_width//2
        select_y = SCREEN_HEIGHT//2 - select_height//2
        
        weapons = list(self.weapon_types.keys())
        for i in range(len(weapons)):
            weapon_y = select_y + 150 + i * 100
            weapon_rect = pygame.Rect(select_x + 50, weapon_y - 20, select_width - 100, 80)
            if weapon_rect.collidepoint(mouse_pos):
                self.weapon_select_selection = i
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return
        
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def handle_weapon_select_click(self, mouse_pos):
        select_width = 800
        select_height = 600
        select_x = SCREEN_WIDTH//2 - select_width//2
        select_y = SCREEN_HEIGHT//2 - select_height//2
        
        weapons = list(self.weapon_types.keys())
        for i in range(len(weapons)):
            weapon_y = select_y + 150 + i * 100
            weapon_rect = pygame.Rect(select_x + 50, weapon_y - 20, select_width - 100, 80)
            if weapon_rect.collidepoint(mouse_pos):
                self.select_weapon(weapons[i])
                break
    
    def handle_main_menu_hover(self, mouse_pos):
        menu_width = 400
        menu_height = 300
        menu_x = SCREEN_WIDTH//2 - menu_width//2
        menu_y = SCREEN_HEIGHT//2 - menu_height//2
        
        for i in range(2):  # 2 menu options: Start Game, Quit
            option_y = menu_y + 150 + i * 60
            option_rect = pygame.Rect(menu_x + 50, option_y - 15, menu_width - 100, 50)
            if option_rect.collidepoint(mouse_pos):
                self.main_menu_selection = i
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return
        
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def handle_main_menu_click(self, mouse_pos):
        menu_width = 400
        menu_height = 300
        menu_x = SCREEN_WIDTH//2 - menu_width//2
        menu_y = SCREEN_HEIGHT//2 - menu_height//2
        
        for i in range(2):  # 2 menu options: Start Game, Quit
            option_y = menu_y + 150 + i * 60
            option_rect = pygame.Rect(menu_x + 50, option_y - 15, menu_width - 100, 50)
            if option_rect.collidepoint(mouse_pos):
                if i == 0:  # Start Game
                    self.game_state = "weapon_select"
                elif i == 1:  # Quit
                    self.running = False
                break
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()