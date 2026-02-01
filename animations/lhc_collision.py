from manim import *
import numpy as np
import os

class LHCCollision(Scene):
    def construct(self):
        # 0. SETUP
        # Disable Manim's default wait time for shorter development loops if needed, 
        # but we want ~60s total.

        # === THEME: DARK PHYSICS ===
        self.camera.background_color = "#111111"

        # ==========================================
        # PART 1: THE THEORY (THE HIGGS FIELD) (~15s)
        # ==========================================
        
        # Grid representing the field
        # Create a grid of small dots
        rows = 15
        cols = 25
        grid = VGroup()
        for x in range(-7, 8):
            for y in range(-4, 5):
                grid.add(Dot(point=[x, y, 0], radius=0.03, color=GRAY_D))
        
        field_title = Text("The Higgs Field", font_size=40, color=BLUE_B).to_edge(UP)
        field_desc = Text("Particles gain mass by interacting with the field", font_size=24, color=GRAY).next_to(field_title, DOWN)
        
        self.play(FadeIn(grid), Write(field_title))
        self.play(Write(field_desc))
        self.wait(1)
        
        # Particle 1: Photon (Massless) - Zips through
        photon = Dot(color=YELLOW, radius=0.1)
        photon.move_to(LEFT * 6 + UP * 2)
        photon_trail = TracedPath(photon.get_center, dissipating_time=0.5, stroke_opacity=[1, 0], stroke_width=3, stroke_color=YELLOW)
        self.add(photon_trail)
        
        # Centered label just below the photon path (which is at UP*2)
        photon_label = Text("Photon (Massless)", font_size=24, color=YELLOW).move_to(UP * 0.8)
        
        self.play(FadeIn(photon_label, run_time=0.3))
        self.play(
            MoveAlongPath(photon, Line(LEFT*6+UP*2, RIGHT*6+UP*2), run_time=2.0, rate_func=linear),
        )
        self.play(FadeOut(photon), FadeOut(photon_trail), FadeOut(photon_label))
        
        # Particle 2: Heavy Quark (Massive) - Drags through
        # We simulate interaction by making nearby grid points light up/move towards it
        quark = Dot(color=RED, radius=0.15)
        quark.move_to(LEFT * 4 + DOWN * 1)
        # Centered label just below the quark path (which is at DOWN*1)
        quark_label = Text("Top Quark (Massive)", font_size=24, color=RED).move_to(DOWN * 2.2)
        
        tracer = TracedPath(quark.get_center, dissipating_time=2.0, stroke_opacity=[1, 0], stroke_width=5, stroke_color=RED) 
        self.add(tracer)

        # Move slower
        self.play(FadeIn(quark_label, run_time=0.3))
        self.play(
            MoveAlongPath(quark, Line(LEFT*4+DOWN*1, RIGHT*6+DOWN*1), run_time=5, rate_func=linear),
        )
        
        # Formula & Date
        lagrangian = MathTex(r"\mathcal{L} \supset -g H \bar{\psi} \psi", font_size=36, color=BLUE).to_edge(DOWN).shift(UP*0.5)
        proposal_date = Text("Proposed: 1964 (Higgs, Englert, Brout)", font_size=24, color=GRAY).next_to(lagrangian, DOWN)
        
        self.play(Write(lagrangian), Write(proposal_date))
        self.wait(2)
        
        # Transition
        self.play(
            FadeOut(grid), FadeOut(field_title), FadeOut(field_desc), 
            FadeOut(quark), FadeOut(quark_label), FadeOut(lagrangian), FadeOut(proposal_date), FadeOut(tracer)
        )

        # ==========================================
        # PART 2: THE MACHINE (ACCELERATOR) (~25s)
        # ==========================================
        
        # Geometry
        lhc_radius = 2.5
        sps_radius = 0.7
        
        lhc_ring = Circle(radius=lhc_radius, color=BLUE_E, stroke_width=4).shift(RIGHT * 1.5)
        lhc_left = lhc_ring.point_at_angle(PI)
        
        sps_ring = Circle(radius=sps_radius, color=GRAY, stroke_width=4)
        sps_ring.move_to(lhc_left + LEFT * sps_radius)
        
        # Detailed Labels
        sps_label = Text("SPS (7 km)", font_size=16, color=GRAY).next_to(sps_ring, UP)
        lhc_label = Text("LHC (27 km)", font_size=16, color=BLUE_D).next_to(lhc_ring, DOWN)
        lhc_bold = Text("Large Hadron Collider", font_size=28, color=BLUE_B).to_corner(UL)
        lhc_dates = Text("Operations: 2008 – Present", font_size=18, color=GRAY).next_to(lhc_bold, DOWN, aligned_edge=LEFT)
        
        self.play(
            Create(sps_ring), Write(sps_label),
            Create(lhc_ring), Write(lhc_label), Write(lhc_bold), Write(lhc_dates)
        )
        
        # PROTON BUNCH INJECTION
        # Start slow to avoid aliasing visuals
        proton = Dot(point=sps_ring.point_at_angle(0), color=YELLOW, radius=0.08)
        proton_lbl = Text("Proton Bunch", font_size=16, color=YELLOW).next_to(sps_ring, DOWN)
        
        # Proper trail for smooth motion look
        trail = TracedPath(proton.get_center, dissipating_time=0.4, stroke_opacity=[1, 0], stroke_width=4, stroke_color=YELLOW)
        self.add(trail)
        
        # SPS Phase
        self.play(
            MoveAlongPath(proton, sps_ring, run_time=2, rate_func=linear),
            Write(proton_lbl)
        )
        self.play(MoveAlongPath(proton, sps_ring, run_time=1, rate_func=linear))
        
        # Transfer to LHC
        # Split into two beams
        beam1 = Dot(point=lhc_left, color=BLUE_A, radius=0.08)
        beam2 = Dot(point=lhc_left, color=RED_A, radius=0.08)
        
        trail1 = TracedPath(beam1.get_center, dissipating_time=0.5, stroke_opacity=[1, 0], stroke_width=4, stroke_color=BLUE_A)
        trail2 = TracedPath(beam2.get_center, dissipating_time=0.5, stroke_opacity=[1, 0], stroke_width=4, stroke_color=RED_A)
        
        self.remove(proton, trail)
        self.add(beam1, beam2, trail1, trail2)
        
        # Cleanup SPS visuals to focus
        self.play(FadeOut(sps_ring), FadeOut(sps_label), FadeOut(proton), FadeOut(proton_lbl)) # Proton already removed but just in case
        
        info_text = Text("Acceleration Phase", font_size=24, color=YELLOW).next_to(lhc_label, DOWN, buff=0.3)
        beams_text = Text("Counter-Rotating Beams", font_size=20, color=WHITE).next_to(info_text, DOWN)
        self.play(Write(info_text), Write(beams_text))

        # ACCELERATION PHASE
        # We need paths.
        path_cw = lhc_ring.copy().rotate(PI) # Start at Left
        path_ccw = lhc_ring.copy().rotate(PI).reverse_direction()
        
        # Ramp up speed
        # We use a ValueTracker to control the "progress" (alpha) along the path manually?
        # Or just sequence of MoveAlongPath with reducing run_time.
        # To avoid aliasing, the trail length makes it look like a continuous ring eventually.
        
        speeds = [2.0, 1.5, 1.0, 0.7, 0.5, 0.3]
        for t in speeds:
            self.play(
                MoveAlongPath(beam1, path_cw, run_time=t, rate_func=linear),
                MoveAlongPath(beam2, path_ccw, run_time=t, rate_func=linear),
            )
            # Increase trail length as we go faster to simulate motion blur?
            # TracedPath does this automatically based on speed vs dissipating_time!
        
        # Final "light speed" loops
        # At t=0.2, Manim might skip frames if fps is low. But trail bridges gaps.
        for _ in range(4):
             self.play(
                MoveAlongPath(beam1, path_cw, run_time=0.25, rate_func=linear),
                MoveAlongPath(beam2, path_ccw, run_time=0.25, rate_func=linear),
            )

        # ==========================================
        # PART 3: THE COLLISION (~10s)
        # ==========================================
        
        self.play(FadeOut(info_text), FadeOut(beams_text), FadeOut(lhc_bold), FadeOut(lhc_label), FadeOut(lhc_dates), FadeOut(lhc_ring))
        
        # Setup Collision View
        detector_ring_1 = Circle(radius=1.5, color=GREY, stroke_width=2) # Tracker
        detector_ring_2 = Circle(radius=2.5, color=GREY, stroke_width=2) # ECAL
        detector_ring_3 = Circle(radius=3.5, color=GREY, stroke_width=2) # Muon
        detector_label = Text("ATLAS Detector View", font_size=24).to_edge(UP)
        
        self.play(
            FadeIn(detector_ring_1), FadeIn(detector_ring_2), FadeIn(detector_ring_3), Write(detector_label),
            beam1.animate.move_to(LEFT * 4).scale(1.5),
            beam2.animate.move_to(RIGHT * 4).scale(1.5), # Reset position
        )
        
        # Clear trails for the static moment
        trail1.clear_updaters()
        trail2.clear_updaters()
        self.remove(trail1, trail2)
        
        # Add new short trails for the smash
        t1 = TracedPath(beam1.get_center, dissipating_time=0.2, stroke_width=5, stroke_color=BLUE)
        t2 = TracedPath(beam2.get_center, dissipating_time=0.2, stroke_width=5, stroke_color=RED)
        self.add(t1, t2)
        
        # Smash
        self.play(
            beam1.animate.move_to(ORIGIN),
            beam2.animate.move_to(ORIGIN),
            run_time=0.3, rate_func=rush_into
        )
        
        # IMPACT
        self.remove(beam1, beam2, t1, t2)
        flash = Flash(ORIGIN, color=WHITE, line_length=1.0, num_lines=30, flash_radius=0.5)
        
        # SHOWER
        shower = VGroup()
        np.random.seed(42)
        for _ in range(30):
            l = Line(ORIGIN, np.array([np.random.uniform(-3,3), np.random.uniform(-3,3), 0]), color=random_color())
            shower.add(l)
            
        self.play(flash, Create(shower, run_time=0.2))
        self.play(FadeOut(shower, run_time=1))
        
        # HIGGS DECAY
        gamma_l = DashedLine(ORIGIN, LEFT*3 + UP*2, color=YELLOW)
        gamma_r = DashedLine(ORIGIN, RIGHT*3 + DOWN*2, color=YELLOW)
        h_label = MathTex(r"H \to \gamma \gamma").shift(UP*0.5)
        
        self.play(Create(gamma_l), Create(gamma_r), Write(h_label))
        self.wait(2)
        
        # ==========================================
        # PART 4: THE RESULT (~10s)
        # ==========================================
        
        # Clear
        self.play(
            FadeOut(detector_ring_1), FadeOut(detector_ring_2), FadeOut(detector_ring_3),
            FadeOut(gamma_l), FadeOut(gamma_r), FadeOut(h_label), FadeOut(detector_label)
        )
        
        # Plot
        ax = Axes(
            x_range=[100, 160, 10],
            y_range=[0, 1200, 200],
            x_length=9, y_length=6
        )
        labels = ax.get_axis_labels(x_label="Mass [GeV]", y_label="Events")
        
        bg_plot = ax.plot(lambda x: 1000 * np.exp(-0.02*(x-100)), color=GREY)
        sig_plot = ax.plot(lambda x: 1000 * np.exp(-0.02*(x-100)) + 200*np.exp(-0.1*(x-125)**2), color=YELLOW)
        
        self.play(Create(ax), Write(labels))
        self.play(Create(bg_plot))
        self.play(Transform(bg_plot, sig_plot))
        
        sig_label = MathTex(r"5\sigma \text{ Significance}").to_corner(UR)
        date = Text("July 2012", font_size=24, color=YELLOW).next_to(sig_label, DOWN)
        
        self.play(Write(sig_label), Write(date))
        self.wait(2)
        
        conclusion = Text("Standard Model: Complete?", font_size=32).to_edge(UP)
        missing = Text("But what about Gravity & Dark Matter?", font_size=24, color=RED).next_to(conclusion, DOWN)
        
        self.play(FadeOut(ax), FadeOut(labels), FadeOut(bg_plot), FadeOut(sig_plot), FadeOut(sig_label), FadeOut(date))
        self.play(Write(conclusion))
        self.wait(1)
        self.play(Write(missing))
        
        # Cosmology Images
        bh_image = ImageMobject("assets/images/black_hole.png").scale(0.8)
        galaxy_image = ImageMobject("assets/images/galaxy.png").scale(0.8)
        
        # Arrange side by side
        img_group = Group(bh_image, galaxy_image).arrange(RIGHT, buff=1.0)
        img_group.next_to(missing, DOWN, buff=0.5)
        
        self.play(FadeIn(img_group))
        self.wait(3)

