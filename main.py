"""
Manim Math Visualizations

Run examples with:
    uv run manim -pql main.py CircleExample
    
Flags:
    -p  Preview when done
    -ql Low quality (480p, quick render)
    -qm Medium quality (720p)
    -qh High quality (1080p)
"""

from manim import *


class CircleExample(Scene):
    """Simple example: Drawing a circle with a label."""

    def construct(self):
        circle = Circle(color=BLUE, fill_opacity=0.5)
        label = MathTex(r"x^2 + y^2 = 1").next_to(circle, DOWN)

        self.play(Create(circle))
        self.play(Write(label))
        self.wait()


class PythagoreanTheorem(Scene):
    """Visual proof of the Pythagorean theorem."""

    def construct(self):
        # Create the right triangle
        triangle = Polygon(
            ORIGIN, 3 * RIGHT, 3 * RIGHT + 4 * UP,
            color=WHITE, fill_opacity=0.3
        )

        # Labels for sides
        a_label = MathTex("a").next_to(triangle, DOWN)
        b_label = MathTex("b").next_to(triangle, RIGHT)
        c_label = MathTex("c").move_to(triangle.get_center() + 0.5 * UL)

        # The formula
        formula = MathTex(r"a^2 + b^2 = c^2").to_edge(UP)

        self.play(Create(triangle))
        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.wait(0.5)
        self.play(Write(formula))
        self.wait()


class FourierSeries(Scene):
    """Visualize a Fourier series approximation of a square wave."""

    def construct(self):
        title = Text("Fourier Series: Square Wave", font_size=36).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-PI, PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=4,
        ).shift(DOWN * 0.5)
        self.play(Create(axes))

        # Build up the Fourier series
        colors = [BLUE, GREEN, YELLOW, ORANGE, RED]

        def fourier_approx(n_terms):
            def f(x):
                result = 0
                for n in range(1, n_terms + 1, 2):
                    result += (4 / (n * PI)) * np.sin(n * x)
                return result
            return f

        current_graph = None
        for i, n in enumerate([1, 3, 5, 9, 21]):
            graph = axes.plot(
                fourier_approx(n),
                color=colors[i % len(colors)]
            )
            label = MathTex(f"n = {n}").to_edge(RIGHT).shift(UP)

            if current_graph is None:
                self.play(Create(graph), Write(label))
            else:
                self.play(
                    Transform(current_graph, graph),
                    Transform(current_label, label)
                )
            current_graph = current_graph or graph
            current_label = current_label if i > 0 else label
            self.wait(0.5)

        self.wait()
