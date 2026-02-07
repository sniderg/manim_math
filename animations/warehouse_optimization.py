from manim import *
import numpy as np

class WarehouseOptimization(Scene):
    def construct(self):
        # 1. Setup Map
        self.setup_map()
        
        # 2. Define Locations
        self.setup_locations()
        
        # 3. Initial Network
        self.create_initial_network()
        
        self.wait(2)
        
        # 4. Optimization Process
        self.animate_optimization()

    def setup_map(self):
        # Load the map image
        # Note: Manim looks for assets in specific directories or relative paths
        # We copied the map to 'assets/southern_ontario_map.png'
        map_image = ImageMobject("assets/southern_ontario_map.png")
        
        # Scale to fit height (leaving room for title/stats)
        map_image.height = 7.5
        # Ensure it doesn't exceed width
        if map_image.width > 13.5:
             map_image.width = 13.5
             
        self.add(map_image)
        self.map_image = map_image
        
        # Add Title
        title = Text("Warehouse Distribution Optimization", font_size=36)
        title.to_edge(UP)
        title.set_z_index(100) # Ensure on top
        self.play(Write(title), FadeIn(map_image))
        self.wait(1)

    def setup_locations(self):
        # Approximate relative positions based on the map visual analysis
        # Toronto ~ [-0.1, -0.6]
        # Ottawa ~ [3.1, 1.3]
        # London ~ [-1.8, -1.3]
        # Windsor ~ [-3.2, -2.5] (Estimated further SW)
        
        # Warehouses (Squares)
        self.warehouses = {
            "Toronto": {"coords": [-0.1, -0.6, 0], "color": BLUE},
            "London": {"coords": [-1.8, -1.3, 0], "color": BLUE},
            "Ottawa": {"coords": [3.1, 1.3, 0], "color": BLUE},
        }
        
        # Customers (Dots)
        # Creating some synthetic customer locations around these hubs
        self.customers = [
            # Around Toronto (GTA)
            [0.4, -0.4, 0], [-0.5, -0.2, 0], [0.2, -0.1, 0], [-0.3, -0.9, 0],
            # Around London & SW
            [-2.2, -1.5, 0], [-1.5, -1.8, 0], [-2.5, -1.0, 0],
            # Windsor
            [-3.2, -2.5, 0],
            # Around Ottawa & East
            [3.5, 1.0, 0], [2.8, 1.5, 0], [2.5, 0.8, 0],
            # Kingston area (Roughly midway Toronto-Ottawa)
            [2.2, 0.2, 0]
        ]
        
        # Visuals
        self.warehouse_mobjects = VGroup()
        for name, data in self.warehouses.items():
            sq = Square(side_length=0.3, color=data["color"], fill_opacity=0.8)
            sq.move_to(data["coords"])
            label = Text(name, font_size=16).next_to(sq, UP, buff=0.1)
            self.warehouse_mobjects.add(VGroup(sq, label))
            
        self.customer_mobjects = VGroup()
        for coords in self.customers:
            dot = Dot(point=coords, color=GREEN, radius=0.08)
            self.customer_mobjects.add(dot)
            
        self.play(
            LaggedStart(
                *[FadeIn(w, scale=0.5) for w in self.warehouse_mobjects],
                lag_ratio=0.2
            ),
            LaggedStart(
                *[Create(c) for c in self.customer_mobjects],
                lag_ratio=0.05
            )
        )

    def create_initial_network(self):
        # Connect every customer to every warehouse (Dense Network)
        self.initial_edges = VGroup()
        
        for cust_dot in self.customer_mobjects:
            for wh_group in self.warehouse_mobjects:
                wh_sq = wh_group[0]
                line = Line(wh_sq.get_center(), cust_dot.get_center(), stroke_width=1, stroke_opacity=0.3, color=GREY)
                self.initial_edges.add(line)
                
        self.play(Create(self.initial_edges, lag_ratio=0.01), run_time=2)
        
    def animate_optimization(self):
        # 1. Show Cost Calculation
        cost_text = Text("Total Cost: $1,000,000", font_size=24, color=RED)
        cost_text.to_edge(LEFT).shift(UP)
        self.play(Write(cost_text))
        
        # 2. Optimization Logic (Visualized)
        # Select best routes: Closest warehouse for each customer
        best_edges = VGroup()
        unused_edges = VGroup()
        
        total_cost = 0
        
        for cust_dot in self.customer_mobjects:
            # Find closest warehouse
            min_dist = float('inf')
            best_wh = None
            
            for wh_group in self.warehouse_mobjects:
                wh_sq = wh_group[0]
                dist = np.linalg.norm(wh_sq.get_center() - cust_dot.get_center())
                if dist < min_dist:
                    min_dist = dist
                    best_wh = wh_sq
            
            # Create best route line
            # We want to transform the existing line corresponding to this if possible, 
            # but simpler to just draw new one over and fade others
            best_line = Line(best_wh.get_center(), cust_dot.get_center(), stroke_width=3, color=YELLOW)
            best_edges.add(best_line)
            total_cost += min_dist * 1000 # arbitrary cost unit
            
        # 3. Animate Transition
        self.play(
            FadeOut(self.initial_edges),
            FadeIn(best_edges),
            run_time=2
        )
        
        # 4. Update Cost
        new_cost_text = Text(f"Total Cost: ${int(total_cost):,}", font_size=24, color=GREEN)
        new_cost_text.move_to(cost_text)
        
        self.play(Transform(cost_text, new_cost_text))
        self.wait(1)
        
        # 5. Visualize Flow (Trucks)
        # Create dots moving from WH to Customers along best edges
        trucks = VGroup()
        animations = []
        for edge in best_edges:
            truck = Dot(color=YELLOW, radius=0.06)
            trucks.add(truck)
            animations.append(MoveAlongPath(truck, edge, rate_func=linear))
            
        self.play(*animations, run_time=2, rate_func=linear)
        self.play(FadeOut(trucks))
        
