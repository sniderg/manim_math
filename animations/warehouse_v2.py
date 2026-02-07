from manim import *
from animations.map_builder import MapBuilder
import numpy as np

class WarehouseOptimizationV2(MovingCameraScene):
    def construct(self):
        # 1. Build Map
        self.map_builder = MapBuilder("assets/ontario.geojson")
        ontario_map = self.map_builder.build_map_mobjects(
            fill_color="#222222", 
            stroke_color="#555555"
        )
        self.add(ontario_map)
        
        # 2. Setup Cities using Real Lat/Lon
        self.setup_locations()
        
        # 3. Cinematic Setup (Fixed on Southern Ontario)
        # Calculate bounds of interest (Windsor to Ottawa)
        lats = [c[0] for c in self.city_mobjects.values()]
        lons = [c[1] for c in self.city_mobjects.values()] # Wait, stored as points/mobjects not latlon
        
        # Get points from city_mobjects dictionary
        points = list(self.city_mobjects.values())
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        # Set camera to frame Southern Ontario nicely
        # Width roughly 6-7 units to cover Windsor (-3ish) to Ottawa (+3ish)
        self.camera.frame.move_to([center_x, center_y, 0])
        self.camera.frame.set(width=7.5) 
        
        self.play(
            LaggedStart(*[FadeIn(w, shift=UP) for w in self.warehouses], lag_ratio=0.2),
            LaggedStart(*[GrowFromCenter(c) for c in self.customers], lag_ratio=0.05),
            run_time=2
        )
        self.wait(1)
        
        # 4. Equations (Overlay)
        # Position equations in top-left (Lake Huron area / Empty space)
        obj_func = MathTex(r"\min Z = \sum c_{ij} x_{ij}", color=WHITE, font_size=28)
        constraint = MathTex(r"\sum x_{ij} = 1", color=WHITE, font_size=28)
        
        equations = VGroup(
            Text("Optimization Model", font_size=32, color=BLUE),
            obj_func,
            constraint
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # Move relative to camera frame
        equations.move_to(self.camera.frame.get_corner(UL) + [2.5, -1.0, 0])
        
        self.play(Write(equations), run_time=2)
        self.wait(2)
        
        # 5. Animate Network
        # Initialize lines (all-to-all)
        self.create_initial_lines()
        
        self.play(Create(self.lines), run_time=2)
        
        # Cost text
        self.cost_text = VGroup(
            Text("Total Cost:", font_size=24, color=RED),
            DecimalNumber(1542000, num_decimal_places=0, unit=" \\$", font_size=24, color=RED)
        ).arrange(RIGHT).to_corner(UL)
        
        # Fade out equations to make room for cost or keep them?
        # User said "pan out to where it is now when you start to add equations"
        # Using FadeOut to clear clutter before optimization
        self.play(
            FadeOut(equations),
            Write(self.cost_text)
        )
        self.wait(1)

        self.play_optimization()

    def create_initial_lines(self):
        self.lines = VGroup()
        for node in self.all_nodes:
            if node['type'] == 'customer':
                # Line to every hub
                for hub_name in self.warehouse_hubs:
                    hub_pos = self.city_mobjects[hub_name]
                    line = Line(node['pos'], hub_pos, stroke_width=0.5, color=GREY, stroke_opacity=0.3)
                    self.lines.add(line)

    def play_initial_network(self):
        pass # Deprecated, logic moved to construct for better flow


    def setup_locations(self):
        # Real Coordinates
        cities = {
            "Toronto": (43.6532, -79.3832),
            "Ottawa": (45.4215, -75.6972),
            "London": (42.9849, -81.2453),
            "Windsor": (42.3149, -83.0477),
            "Kingston": (44.2312, -76.4860),
            "Sudbury": (46.4917, -81.0140),
        }
        
        self.warehouse_hubs = ["Toronto", "Ottawa", "London"]
        
        self.city_mobjects = {}
        self.warehouses = VGroup()
        self.customers = VGroup()
        
        self.all_nodes = []
        
        for name, (lat, lon) in cities.items():
            point = self.map_builder.lat_lon_to_point(lat, lon)
            
            if name in self.warehouse_hubs:
                # Warehouse
                mob = Square(side_length=0.25, color=BLUE, fill_opacity=0.8).move_to(point)
                lbl = Text(name, font_size=16, color=WHITE).next_to(mob, UP, buff=0.1)
                self.warehouses.add(VGroup(mob, lbl))
                self.city_mobjects[name] = point
                self.all_nodes.append({"pos": point, "type": "hub", "id": name})
            else:
                # Customer / Other City
                mob = Dot(point=point, color=GREEN, radius=0.08)
                lbl = Text(name, font_size=14, color=GRAY).next_to(mob, UR, buff=0.05)
                self.customers.add(VGroup(mob, lbl))
                self.city_mobjects[name] = point
                self.all_nodes.append({"pos": point, "type": "customer", "id": name})

        # Add some random customers around hubs to fill space
        np.random.seed(42)
        for _ in range(15):
            # Pick a random hub to be near
            hub_name = np.random.choice(list(cities.keys()))
            hub_lat, hub_lon = cities[hub_name]
            
            # Add random noise
            r_lat = hub_lat + np.random.normal(0, 0.5)
            r_lon = hub_lon + np.random.normal(0, 0.5)
            
            point = self.map_builder.lat_lon_to_point(r_lat, r_lon)
            
            # Simple check if inside map would be hard without Shapely
            # Just plotting them for now
            dot = Dot(point=point, color=GREEN_B, radius=0.05)
            self.customers.add(dot)
            self.all_nodes.append({"pos": point, "type": "customer", "id": "random"})

    def play_initial_network(self):
        # Show map
        self.wait(0.5)
        
        # Show nodes
        self.play(
            LaggedStart(*[FadeIn(w, shift=UP) for w in self.warehouses], lag_ratio=0.2),
            LaggedStart(*[GrowFromCenter(c) for c in self.customers], lag_ratio=0.05),
            run_time=2
        )
        
        # Connect everything to start (Messy)
        self.lines = VGroup()
        for node in self.all_nodes:
            if node['type'] == 'customer':
                # Line to every hub
                for hub_name in self.warehouse_hubs:
                    hub_pos = self.city_mobjects[hub_name]
                    line = Line(node['pos'], hub_pos, stroke_width=0.5, color=GREY, stroke_opacity=0.3)
                    self.lines.add(line)
        
        self.play(Create(self.lines), run_time=2)
        
        # Initial Cost text
        self.cost_text = VGroup(
            Text("Total Cost:", font_size=24, color=RED),
            DecimalNumber(1542000, num_decimal_places=0, unit=" \\$", font_size=24, color=RED)
        ).arrange(RIGHT).to_corner(UL)
        
        self.play(Write(self.cost_text))
        self.wait(1)

    def play_optimization(self):
        # Optimize: Each customer chooses closest hub
        
        new_lines = VGroup()
        trucks = VGroup()
        
        total_dist = 0
        
        for node in self.all_nodes:
            if node['type'] == 'customer':
                # Find closest hub
                closest_dist = float('inf')
                closest_hub_pos = None
                
                start_pos = node['pos']
                
                for hub_name in self.warehouse_hubs:
                    hub_pos = self.city_mobjects[hub_name]
                    dist = np.linalg.norm(start_pos - hub_pos)
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_hub_pos = hub_pos
                
                # Create optimized line
                line = Line(start_pos, closest_hub_pos, stroke_width=2, color=YELLOW, stroke_opacity=0.8)
                new_lines.add(line)
                
                total_dist += closest_dist
                
                # Truck animation
                truck = Dot(color=ORANGE, radius=0.06)
                truck.move_to(closest_hub_pos)
                # Animate truck going FROM hub TO customer
                trucks.add(truck)
                truck.target_path = Line(closest_hub_pos, start_pos)

        # Transformation
        self.play(
            Transform(self.lines, new_lines),
            self.cost_text[1].animate.set_value(total_dist * 5000).set_color(GREEN),
            self.cost_text[0].animate.set_color(GREEN),
            run_time=2
        )
        
        # Animate flow (trucks)
        self.play(
            *[MoveAlongPath(t, t.target_path, rate_func=linear) for t in trucks],
            run_time=2,
            rate_func=there_and_back
        )
        self.wait(1)
