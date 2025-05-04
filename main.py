import tkinter as tk
from tkinter import messagebox
from eldoria.simulation import EldoriaSimulation
from eldoria.enums import EntityType, TreasureType

class EldoriaGUI:
    COLORS = {
        EntityType.EMPTY: 'white',
        EntityType.TREASURE: {
            TreasureType.BRONZE: '#CD7F32',
            TreasureType.SILVER: '#C0C0C0',
            TreasureType.GOLD: '#FFD700'
        },
        EntityType.HUNTER: 'blue',
        EntityType.KNIGHT: 'red',
        EntityType.HIDEOUT: 'green'
    }

    def __init__(self, root):
        self.root = root
        self.sim = EldoriaSimulation(size=15)
        self.setup_ui()
        self.running = False
        self.speed = 300  # ms between steps
        self.game_speed = 1.0
        self.draw_world()

    def setup_ui(self):
        """Initialize GUI components"""
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg='white')
        self.canvas.pack()

        # Control panel
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        # Score display
        self.score_label = tk.Label(control_frame, text="Score: 0", font=('Arial', 12))
        self.score_label.pack(side=tk.LEFT, padx=10)

        # Stamina display
        self.stamina_label = tk.Label(control_frame, text="Stamina: 100%", font=('Arial', 12))
        self.stamina_label.pack(side=tk.LEFT, padx=10)

        # Control buttons
        btn_frame = tk.Frame(control_frame)
        btn_frame.pack(side=tk.RIGHT)

        tk.Button(btn_frame, text="▶ Start", command=self.start_simulation).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="❚❚ Pause", command=self.pause_simulation).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="+ Speed", command=self.increase_speed).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="- Speed", command=self.decrease_speed).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="🔄 Reset", command=self.reset_simulation).pack(side=tk.LEFT)

        # Key bindings
        self.root.bind('<Up>', lambda e: self.move_hunter(0, -1))
        self.root.bind('<Down>', lambda e: self.move_hunter(0, 1))
        self.root.bind('<Left>', lambda e: self.move_hunter(-1, 0))
        self.root.bind('<Right>', lambda e: self.move_hunter(1, 0))
        self.root.bind('<space>', lambda e: self.toggle_simulation())

    def draw_world(self):
        """Draw the current game state"""
        self.canvas.delete("all")
        cell_size = 600 // self.sim.grid.size

        # Draw grid cells
        for x in range(self.sim.grid.size):
            for y in range(self.sim.grid.size):
                entity = self.sim.grid.cells[x][y]
                color = self.COLORS.get(entity, 'white')

                # Handle treasure with value display
                if entity == EntityType.TREASURE:
                    for treasure in self.sim.treasures:
                        if (x, y) == (treasure.x, treasure.y):
                            color = self.COLORS[EntityType.TREASURE][treasure.type]
                            # Draw treasure value
                            self.canvas.create_text(
                                x * cell_size + cell_size//2,
                                y * cell_size + cell_size//2,
                                text=f"{treasure.value:.1f}",
                                fill='black'
                            )
                            break

                # Draw cell
                self.canvas.create_rectangle(
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    fill=color, outline='black'
                )

        # Update displays
        self.score_label.config(text=f"Score: {int(self.sim.score)}")
        if self.sim.hunters:
            stamina = int(self.sim.hunters[0].stamina)
            self.stamina_label.config(text=f"Stamina: {stamina}%")

        # Game over message
        if self.sim.game_over:
            self.running = False
            messagebox.showinfo(
                "Game Over",
                f"Final Score: {int(self.sim.score)}\n\n"
                "Press Reset to play again"
            )

    def move_hunter(self, dx, dy):
        """Move hunter in specified direction"""
        if self.sim.game_over or not self.sim.hunters or not self.running:
            return

        hunter = self.sim.hunters[0]
        new_x = (hunter.x + dx) % self.sim.grid.size
        new_y = (hunter.y + dy) % self.sim.grid.size

        # Check if target cell is walkable
        target_entity = self.sim.grid.cells[new_x][new_y]
        if target_entity not in [EntityType.EMPTY, EntityType.TREASURE]:
            return

        # Update positions
        self.sim.grid.cells[hunter.x][hunter.y] = EntityType.EMPTY
        hunter.x, hunter.y = new_x, new_y
        self.sim.grid.cells[new_x][new_y] = EntityType.HUNTER

        # Run simulation step
        self.sim.run_step()
        self.draw_world()

    def start_simulation(self):
        """Start automatic simulation"""
        if not self.running and not self.sim.game_over:
            self.running = True
            self.run_simulation()

    def pause_simulation(self):
        """Pause simulation"""
        self.running = False

    def toggle_simulation(self):
        """Toggle simulation running state"""
        if self.running:
            self.pause_simulation()
        else:
            self.start_simulation()

    def run_simulation(self):
        """Run simulation steps at intervals"""
        if self.running and not self.sim.game_over:
            self.sim.run_step()
            self.draw_world()
            self.root.after(int(self.speed / self.game_speed), self.run_simulation)

    def increase_speed(self):
        """Increase simulation speed"""
        self.game_speed = min(3.0, self.game_speed + 0.5)

    def decrease_speed(self):
        """Decrease simulation speed"""
        self.game_speed = max(0.5, self.game_speed - 0.5)

    def reset_simulation(self):
        """Reset simulation to initial state"""
        self.running = False
        self.sim = EldoriaSimulation(size=15)
        self.game_speed = 1.0
        self.draw_world()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Knights of Eldoria")
    gui = EldoriaGUI(root)
    root.mainloop()