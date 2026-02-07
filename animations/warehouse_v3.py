
from manim import *
from animations.map_builder import MapBuilder
from animations.orc_data import DEMAND_ZONES, CANDIDATE_WAREHOUSES, OPTIMAL_SET
import numpy as np

class WarehouseOptimizationV3(MovingCameraScene):
    def construct(self):
        # 1. Build Map
        self.map_builder = MapBuilder("assets/ontario.geojson")
        ontario_map = self.map_builder.build_map_mobjects(
            fill_color="#1a1a1a", 
            stroke_color="#444444"
        )
        self.add(ontario_map)
        
        # 2. Setup Camera (Southern Ontario focus)
        # Bounding box roughly covers Windsor (-83) to Ottawa (-75)
        # Calculate center point in Manim coordinates
        center_point = self.map_builder.lat_lon_to_point(43.8, -79.5)
        self.camera.frame.move_to(center_point)
        # Initial width to see the whole region
        self.camera.frame.set(width=8.0) 
        
        # 3. Visualization Setup
        zones = VGroup()
        candidates = VGroup()
        
        # Data Mobjects storage
        self.zone_mobjects = {} # id -> mobject
        self.candidate_mobjects = {} # id -> mobject
        
        # A. Plot Demand Zones
        for z_id, name, lat, lon, pop in DEMAND_ZONES:
            point = self.map_builder.lat_lon_to_point(lat, lon)
            
            # Scale radius by population (log scale for visibility)
            radius = 0.04 + (np.log(pop) / 300) 
            
            dot = Dot(point=point, color=BLUE_C, radius=radius, fill_opacity=0.6)
            self.zone_mobjects[z_id] = dot
            zones.add(dot)
            
        # B. Plot Candidate Warehouses
        for w_id, name, lat, lon in CANDIDATE_WAREHOUSES:
            point = self.map_builder.lat_lon_to_point(lat, lon)
            
            # Hollow square for candidate
            square = Square(side_length=0.2, color=WHITE, stroke_width=2, fill_opacity=0)
            square.move_to(point)
            
            # Label
            label = Text(w_id, font_size=12, color=GREY_B).next_to(square, UP, buff=0.05)
            
            group = VGroup(square, label)
            self.candidate_mobjects[w_id] = group
            candidates.add(group)

        # Animation Sequence
        
        # Intro: Show Zones
        self.play(img_fade_in_zones := LaggedStart(*[GrowFromCenter(z) for z in zones], lag_ratio=0.02, run_time=2))
        self.wait(0.5)
        
        # Intro: Show Candidates
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN) for c in candidates], lag_ratio=0.1, run_time=2))
        self.wait(1)
        
        # 4. Optimization Info Overlay
        info_box = VGroup(
            Text("Network Optimization", font_size=36, color=WHITE),
            Text("Objective: Minimize Fixed + Transport Costs", font_size=24, color=GREY_A),
            Text("Constraints: 90% Service Level", font_size=24, color=GREY_A),
            MathTex(r"\min \sum f_j y_j + \sum c_{ij} x_{ij}", font_size=28, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # Pin to camera corner
        # We need a fixed position relative to camera, so we use add_fixed_in_frame_mobjects if we were doing HUD
        # But for MovingCameraScene, we usually just move it to the frame corner.
        # Let's put it in the top left 'empty' space (Lake Huronish)
        info_box.move_to(self.camera.frame.get_corner(UL) + [3.5, -1.5, 0])
        
        self.play(Write(info_box), run_time=2)
        self.wait(2)
        
        # 5. Run Optimization (Visual Effect)
        # Flash connections to candidates randomly to simulate "solving"
        
        # Create a few temporary lines
        temp_lines = VGroup()
        for _ in range(20):
             # Random zone to random candidate
            z_id = np.random.choice([z[0] for z in DEMAND_ZONES])
            w_id = np.random.choice([w[0] for w in CANDIDATE_WAREHOUSES])
            
            start = self.zone_mobjects[z_id].get_center()
            end = self.candidate_mobjects[w_id][0].get_center()
            
            line = Line(start, end, stroke_width=0.5, color=YELLOW, stroke_opacity=0.3)
            temp_lines.add(line)
            
        self.play(
            ShowPassingFlash(temp_lines.copy().set_color(YELLOW), time_width=0.5),
            run_time=2
        )
        
        # 6. Reveal Solution
        
        # Identify Optimal vs Rejected
        optimal_mobjects = VGroup()
        rejected_mobjects = VGroup()
        
        for w_id, group in self.candidate_mobjects.items():
            square = group[0]
            label = group[1]
            if w_id in OPTIMAL_SET:
                # Transform to Filled Green Square
                target = Square(side_length=0.25, color=GREEN, fill_opacity=1, stroke_width=0)
                target.move_to(square.get_center())
                
                label_target = Text(w_id, font_size=14, color=GREEN_A).next_to(target, UP, buff=0.05)
                
                optimal_mobjects.add(group)
                
                # We animate the change in place
                self.play(
                    Transform(square, target),
                    Transform(label, label_target),
                    run_time=0.1
                )
            else:
                # Fade out rejected slightly
                rejected_mobjects.add(group)
                self.play(
                    group.animate.set_opacity(0.2),
                    run_time=0.05
                )

        self.wait(1)
        
        # 7. Assignment Lines
        # Draw lines from every zone to closest OPTIMAL warehouse
        assignment_lines = VGroup()
        
        text_cost = DecimalNumber(0, unit="M", font_size=36, color=GREEN).next_to(info_box, DOWN, buff=0.5)
        text_label = Text("Total Cost: $", font_size=36, color=GREEN).next_to(text_cost, LEFT, buff=0.1)
        
        final_cost = 702 # From paper
        
        for z_id in self.zone_mobjects:
            z_pos = self.zone_mobjects[z_id].get_center()
            
            closest_dist = float('inf')
            closest_w_pos = None
            
            for w_id in OPTIMAL_SET:
                w_pos = self.candidate_mobjects[w_id][0].get_center() # Use the square's center
                dist = np.linalg.norm(z_pos - w_pos)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_w_pos = w_pos
            
            if closest_w_pos is not None:
                line = Line(z_pos, closest_w_pos, stroke_width=1, color=GREEN_B, stroke_opacity=0.5)
                assignment_lines.add(line)
        
        # Animate lines expanding from warehouses to zones
        self.play(
            Create(assignment_lines, lag_ratio=0.01),
            FadeOut(info_box),
            Write(text_label),
            ChangeDecimalToValue(text_cost, final_cost),
            run_time=3
        )
        
        self.wait(2)
        
        # 8. Service Level Badge
        badge = VGroup(
            RoundedRectangle(corner_radius=0.1, color=GREEN, fill_opacity=0.2, width=3, height=1),
            Text("Service Level: 100%", font_size=24, color=WHITE)
        ).move_to(self.camera.frame.get_corner(UR) + [-2, -1, 0])
        
        self.play(FadeIn(badge, shift=LEFT))
        self.wait(2)
        
        # 9. Final Zoom Out
        zoom_out_center = self.map_builder.lat_lon_to_point(44, -79)
        self.play(
            self.camera.frame.animate.set(width=12).move_to(zoom_out_center),
            run_time=3
        )
        self.wait(1)

