from manim import *

class PolymerDemo(Scene):
    def construct(self):
        # 1. Title
        title = Text("Polymers: From Monomer to Chain", font_size=36)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # 2. Define Helper for Molecules
        # Simple representation: Carbon (Black/Grey), Hydrogen (White)
        def create_ethylene(position=ORIGIN):
            # C=C Double bond
            c1 = Circle(radius=0.4, color=GREY, fill_opacity=1).move_to(position + LEFT*0.6)
            c2 = Circle(radius=0.4, color=GREY, fill_opacity=1).move_to(position + RIGHT*0.6)
            
            # Double bond lines
            b1 = Line(c1.get_center() + UP*0.15, c2.get_center() + UP*0.15)
            b2 = Line(c1.get_center() + DOWN*0.15, c2.get_center() + DOWN*0.15)
            
            # Hydrogens (approx 120 degrees generic placement)
            h1 = Circle(radius=0.2, color=WHITE, fill_opacity=1).move_to(c1.get_center() + LEFT*0.6 + UP*0.6)
            h2 = Circle(radius=0.2, color=WHITE, fill_opacity=1).move_to(c1.get_center() + LEFT*0.6 + DOWN*0.6)
            h3 = Circle(radius=0.2, color=WHITE, fill_opacity=1).move_to(c2.get_center() + RIGHT*0.6 + UP*0.6)
            h4 = Circle(radius=0.2, color=WHITE, fill_opacity=1).move_to(c2.get_center() + RIGHT*0.6 + DOWN*0.6)
            
            # C-H Bonds
            b_h1 = Line(c1.get_center(), h1.get_center(), z_index=-1)
            b_h2 = Line(c1.get_center(), h2.get_center(), z_index=-1)
            b_h3 = Line(c2.get_center(), h3.get_center(), z_index=-1)
            b_h4 = Line(c2.get_center(), h4.get_center(), z_index=-1)
            
            return VGroup(c1, c2, b1, b2, h1, h2, h3, h4, b_h1, b_h2, b_h3, b_h4)

        # 3. Create Monomers
        monomer_text = Text("Ethylene Monomers (C₂H₄)", font_size=24, color=BLUE).next_to(title, DOWN, buff=0.5)
        self.play(Write(monomer_text))

        m1 = create_ethylene(LEFT * 4)
        m2 = create_ethylene(ORIGIN)
        m3 = create_ethylene(RIGHT * 4)
        
        self.play(FadeIn(m1), FadeIn(m2), FadeIn(m3))
        self.wait(1)
        
        # 4. Polymerization Animation
        # "Break" the double bond and link them
        
        # Label for process
        poly_label = Text("Polymerization: Polyethylene", font_size=24, color=GREEN).move_to(monomer_text)
        
        self.play(FadeOut(monomer_text), FadeIn(poly_label))
        
        # Transition: 
        # 1. Rotate C-H bonds to make room (90 deg)
        # 2. Transform Double bond to single bond
        # 3. Create new bonds between units
        
        # This is hardcoded for the demo look
        # We'll just shift them closer and add connecting lines for simplicity/effect
        
        self.play(
            m1.animate.shift(RIGHT * 1.2),
            m3.animate.shift(LEFT * 1.2),
            run_time=1.5
        )
        
        # Add connecting bonds (Yellow for emphasis)
        link1 = Line(m1.get_center() + RIGHT*1.0, m2.get_center() + LEFT*1.0, color=YELLOW, stroke_width=6)
        link2 = Line(m2.get_center() + RIGHT*1.0, m3.get_center() + LEFT*1.0, color=YELLOW, stroke_width=6)
        
        self.play(Create(link1), Create(link2))
        
        # Change double bonds to single in the graphic (cheating by fading out one line from each)
        # The structure of create_ethylene returned: 
        # VGroup(c1, c2, b1, b2, h1, h2, h3, h4, b_h1, b_h2, b_h3, b_h4)
        # indices: 0   1   2   3   ...
        # b1 is at index 2, b2 is at index 3
        
        bonds_to_remove = VGroup(m1[3], m2[3], m3[3]) # Remove bottom bond line from each
        self.play(FadeOut(bonds_to_remove))
        
        # Center bond line shift (approx)
        center_bonds = VGroup(m1[2], m2[2], m3[2])
        self.play(center_bonds.animate.shift(DOWN * 0.15)) # Centering the remaining single bond
        
        self.wait(2)
        
        # 5. Result
        result_text = Text("[ ... - CH₂ - CH₂ - CH₂ - ... ]", font_size=32).next_to(m2, DOWN, buff=1.5)
        self.play(Write(result_text))
        self.wait(3)
