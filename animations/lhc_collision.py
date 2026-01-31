from manim import *
import numpy as np
import os


class LHCCollision(Scene):
    def construct(self):
        # 0. Background Audio check
        audio_path = "assets/ambient.mp3"
        if os.path.exists(audio_path):
            pass # We handle audio in post-processing now!

        # === PART 1: THE ACCELERATOR (TOPOLOGY) ===
        
        # Geometry setup
        lhc_radius = 2.2
        sps_radius = 0.6
        
        # LHC Ring (Main)
        lhc_ring = Circle(radius=lhc_radius, color=BLUE_E, stroke_width=4).shift(RIGHT * 1.5)
        
        # SPS Ring (Injector) - Tangent to LHC at LEFT side
        # LHC Left point is: center + radius * LEFT = (1.5, 0) + (-2.2, 0) = (-0.7, 0)
        # SPS Right point must be (-0.7, 0)
        # SPS Center = SPS Right + radius * LEFT = (-0.7, 0) + (-0.6, 0) = (-1.3, 0)
        lhc_left_point = lhc_ring.point_at_angle(PI)
        sps_center = lhc_left_point + LEFT * sps_radius
        sps_ring = Circle(radius=sps_radius, color=GRAY, stroke_width=4).move_to(sps_center)
        
        # Labels
        sps_label = Text("SPS", font_size=20, color=GRAY).next_to(sps_ring, UP)
        lhc_label = Text("Large Hadron Collider\n(27 km circumference)", font_size=24, color=BLUE)
        lhc_label.next_to(lhc_ring, UP)

        title = Text("The Particle Hunt", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.play(Create(sps_ring), Write(sps_label))
        self.play(Create(lhc_ring), Write(lhc_label))
        self.wait(0.5)

        # Physics Formula
        formula_lorentz = MathTex(r"\vec{F} = q(\vec{v} \times \vec{B})", font_size=32, color=YELLOW)
        formula_lorentz.to_corner(UL).shift(DOWN * 0.5)
        expl_lorentz = Text("Magnetic fields bend the path", font_size=20, color=YELLOW).next_to(formula_lorentz, DOWN)
        
        self.play(Write(formula_lorentz), FadeIn(expl_lorentz))

        # === PART 2: INJECTION & ACCELERATION ===
        
        # Visualizing a "bunch" of protons
        proton = Dot(point=sps_ring.point_at_angle(0), color=YELLOW, radius=0.1)
        
        # 1. Spin in SPS
        self.play(MoveAlongPath(proton, sps_ring, run_time=1.5, rate_func=linear))
        self.play(MoveAlongPath(proton, sps_ring, run_time=1.0, rate_func=linear))
        
        # 2. Inject into LHC (Split into two beams)
        beam_cw = Dot(point=lhc_left_point, color=BLUE_A, radius=0.08) # Clockwise
        beam_ccw = Dot(point=lhc_left_point, color=RED_A, radius=0.08) # Counter-Clockwise
        
        self.play(
            ReplacementTransform(proton, beam_cw),
            FadeIn(beam_ccw),
            FadeOut(sps_label), FadeOut(sps_ring)
        )
        
        # Energy Formula
        formula_energy = MathTex(r"E_{beam} = 6.5\text{ TeV}", font_size=32, color=RED).to_corner(UR).shift(DOWN * 0.5)
        self.play(Write(formula_energy))

        # 3. Accelerate in opposite directions
        # We need a reversed path for CCW
        # Manim's MoveAlongPath follows strict point ordering. 
        # Trick: Rotate the mobject along the center? Or create a reversed path copy.
        lhc_path_cw = lhc_ring.copy().set_opacity(0)
        lhc_path_ccw = lhc_ring.copy().set_opacity(0).reverse_direction() # Does reverse_points work?
        # Actually standard Circle starts at 0 (Right). We are at PI (Left).
        # To make it smooth, let's rotate path so start point matches current pos
        lhc_path_cw.rotate(PI) 
        lhc_path_ccw.rotate(PI) 
        # Note: Circle points start at 0 radians (Right). We want to start at PI (Left).
        
        # Speed up animation
        for speed in [2, 1, 0.5, 0.25]:
            self.play(
                MoveAlongPath(beam_cw, lhc_path_cw, run_time=speed, rate_func=linear),
                MoveAlongPath(beam_ccw, lhc_path_ccw, run_time=speed, rate_func=linear),
            )
            
        # === PART 3: THE COLLISION ===
        
        # Move title out
        self.play(FadeOut(title), FadeOut(lhc_label), FadeOut(lhc_ring), 
                  FadeOut(formula_lorentz), FadeOut(expl_lorentz), FadeOut(formula_energy))
        
        # Zoom effect setup: Bring beams to center collision point
        # Let's say collision happens at center of screen
        collision_point = ORIGIN
        
        self.play(
            beam_cw.animate.move_to(LEFT * 4).scale(2),
            beam_ccw.animate.move_to(RIGHT * 4).scale(2),
        )
        
        # SLOW MOTION SMASH
        self.play(
            beam_cw.animate.move_to(ORIGIN),
            beam_ccw.animate.move_to(ORIGIN),
            run_time=0.5, rate_func=rush_into
        )
        
        # EXPLOSION
        flash = Flash(ORIGIN, color=WHITE, flash_radius=0.5, num_lines=20)
        
        # Particle Tracks (random paths out)
        np.random.seed(1)
        tracks = VGroup()
        for _ in range(15):
            angle = np.random.uniform(0, TAU)
            length = np.random.uniform(2, 4)
            end = np.array([np.cos(angle)*length, np.sin(angle)*length, 0])
            track = Line(ORIGIN, end, color=random_color())
            tracks.add(track)
            
        # The Higgs Decay (2 Photons)
        # H -> gamma gamma (dashed straight lines, back to back)
        h_angle = PI / 3 # arbitrary angle
        gamma1_end = np.array([np.cos(h_angle)*3, np.sin(h_angle)*3, 0])
        gamma2_end = np.array([np.cos(h_angle+PI)*3, np.sin(h_angle+PI)*3, 0])
        
        gamma1 = DashedLine(ORIGIN, gamma1_end, color=YELLOW, dashed_ratio=0.5)
        gamma2 = DashedLine(ORIGIN, gamma2_end, color=YELLOW, dashed_ratio=0.5)
        
        # Higgs Label
        label_h = MathTex(r"H \to \gamma\gamma", color=YELLOW, font_size=36).next_to(gamma1, UP, buff=0.1)
        
        # Animate Explosion
        self.play(
            FadeOut(beam_cw), FadeOut(beam_ccw),
            flash,
            Create(tracks, run_time=0.5),
        )
        self.play(
            Create(gamma1), Create(gamma2), Write(label_h),
            tracks.animate.set_opacity(0.3) # Fade background tracks
        )
        self.wait(1)
        
        # === PART 4: THE DATA (THE BUMP) ===
        
        # Transition to plot
        plot_group = VGroup()
        
        # Axes
        ax = Axes(
            x_range=[100, 160, 10],
            y_range=[0, 1000, 200],
            x_length=9, y_length=6,
            axis_config={"include_tip": False}
        )
        x_lbl = ax.get_x_axis_label(Text("Mass (GeV)", font_size=20))
        y_lbl = ax.get_y_axis_label(Text("Events", font_size=20).rotate(90 * DEGREES))
        
        # Background Noise (Exponential decay)
        def bg_func(x):
            return 800 * np.exp(-0.02 * (x - 100))
            
        bg_curve = ax.plot(bg_func, x_range=[100, 160], color=GRAY)
        
        # Signal (Gaussian Bump at 125)
        def signal_func(x):
            return bg_func(x) + 150 * np.exp(-0.1 * (x - 125)**2)
            
        signal_curve = ax.plot(signal_func, x_range=[100, 160], color=YELLOW)
        
        plot_group.add(ax, x_lbl, y_lbl, bg_curve, signal_curve)
        
        self.play(
            FadeOut(tracks), FadeOut(gamma1), FadeOut(gamma2), FadeOut(label_h),
            FadeIn(plot_group)
        )
        
        # Animate "Data Collection" (Curve fills up)
        self.play(Create(signal_curve, run_time=2))
        
        # Highlight Bump
        bump_arrow = Arrow(ax.c2p(125, signal_func(125) + 200), ax.c2p(125, signal_func(125)), color=RED)
        bump_text = Text("Discovery!\n125 GeV", color=RED, font_size=24).next_to(bump_arrow, UP)
        
        self.play(GrowArrow(bump_arrow), Write(bump_text))
        self.wait(2)
        
        final_text = Text("The Standard Model is Complete?", font_size=32).to_edge(UP)
        self.play(Write(final_text))
        self.wait(2)
