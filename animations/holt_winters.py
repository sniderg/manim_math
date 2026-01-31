"""
Holt-Winters Exponential Smoothing - Educational Animation

Run with:
    uv run manim -pql holt_winters.py HoltWintersExplained
    uv run manim -pqh holt_winters.py HoltWintersExplained  # high quality
"""

from manim import *
import numpy as np
import os


class HoltWintersExplained(Scene):
    """Educational visualization of Holt-Winters triple exponential smoothing."""

    def construct(self):
        # Title
        title = Text("Holt-Winters Exponential Smoothing", font_size=40)
        subtitle = Text("Level + Trend + Seasonality", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Generate synthetic seasonal data
        np.random.seed(42)
        n_points = 48  # 4 years of monthly data
        t = np.arange(n_points)

        # Components
        level = 100
        trend = 0.5
        seasonal_period = 12
        seasonality = 15 * np.sin(2 * np.pi * t / seasonal_period)
        noise = np.random.normal(0, 3, n_points)

        # Combined signal
        y = level + trend * t + seasonality + noise

        # Create axes
        axes = Axes(
            x_range=[0, n_points, 12],
            y_range=[60, 160, 20],
            x_length=11,
            y_length=5,
            axis_config={"include_tip": False},
        ).shift(DOWN * 0.5)

        x_label = Text("Time (months)", font_size=20).next_to(axes, DOWN)
        y_label = Text("Value", font_size=20).rotate(PI / 2).next_to(axes, LEFT)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Plot the raw data as dots
        dots = VGroup(*[
            Dot(axes.c2p(i, y[i]), radius=0.04, color=WHITE)
            for i in range(n_points)
        ])

        raw_label = Text("Raw Data", font_size=20, color=WHITE).to_edge(UP).shift(LEFT * 4)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.02),
            Write(raw_label)
        )
        self.wait(0.5)

        # === DECOMPOSITION: Peel away each component ===
        component_title = Text("Decomposing the Signal", font_size=28).to_edge(UP)
        self.play(FadeOut(raw_label), Write(component_title))
        self.wait(0.5)

        # Store original y values
        y_original = y.copy()

        # --- STEP 1: Remove Level (shift down toward 0) ---
        step1_label = Text("Step 1: Remove Level (baseline)", font_size=22, color=BLUE).to_edge(UP)
        self.play(Transform(component_title, step1_label))

        # Create new axes centered around 0
        detrend_axes = Axes(
            x_range=[0, n_points, 12],
            y_range=[-40, 60, 20],
            x_length=11,
            y_length=5,
            axis_config={"include_tip": False},
        ).shift(DOWN * 0.5)

        # Data with level removed
        y_no_level = y_original - level  # Now centered around 0 + trend + seasonality

        new_dots_1 = VGroup(*[
            Dot(detrend_axes.c2p(i, y_no_level[i]), radius=0.04, color=BLUE)
            for i in range(n_points)
        ])

        # Show the subtraction
        level_text = MathTex(r"y_t - \ell", font_size=32, color=BLUE).to_edge(DR)

        self.play(
            Transform(axes, detrend_axes),
            Transform(dots, new_dots_1),
            FadeOut(x_label), FadeOut(y_label),
            Write(level_text),
            run_time=2
        )
        self.wait(0.5)

        # --- STEP 2: Remove Trend (flatten the slope) ---
        step2_label = Text("Step 2: Remove Trend (flatten)", font_size=22, color=GREEN).to_edge(UP)
        self.play(Transform(component_title, step2_label))

        # Data with level and trend removed
        y_no_trend = y_original - level - trend * t  # Now just seasonality + noise

        # Axes for deseasonalized (smaller range)
        seasonal_axes = Axes(
            x_range=[0, n_points, 12],
            y_range=[-30, 30, 10],
            x_length=11,
            y_length=5,
            axis_config={"include_tip": False},
        ).shift(DOWN * 0.5)

        new_dots_2 = VGroup(*[
            Dot(seasonal_axes.c2p(i, y_no_trend[i]), radius=0.04, color=GREEN)
            for i in range(n_points)
        ])

        # Show the subtraction
        trend_text = MathTex(r"y_t - \ell - b \cdot t", font_size=32, color=GREEN).to_edge(DR)

        self.play(
            Transform(axes, seasonal_axes),
            Transform(dots, new_dots_2),
            Transform(level_text, trend_text),
            run_time=2
        )
        self.wait(0.5)

        # --- STEP 3: Remove Seasonality (reveal residuals) ---
        step3_label = Text("Step 3: Remove Seasonality (residuals)", font_size=22, color=ORANGE).to_edge(UP)
        self.play(Transform(component_title, step3_label))

        # Data with everything removed = just noise
        y_residual = y_original - level - trend * t - seasonality  # Just noise

        # Show the seasonal wave we're subtracting
        seasonal_wave = seasonal_axes.plot(
            lambda x: 15 * np.sin(2 * np.pi * x / seasonal_period),
            x_range=[0, n_points],
            color=ORANGE, stroke_width=2
        )
        self.play(Create(seasonal_wave))
        self.wait(0.3)

        # Axes for residuals (larger range to avoid over-zooming on noise)
        residual_axes = Axes(
            x_range=[0, n_points, 12],
            y_range=[-50, 50, 10],
            x_length=11,
            y_length=5,
            axis_config={"include_tip": False},
        ).shift(DOWN * 0.5)

        new_dots_3 = VGroup(*[
            Dot(residual_axes.c2p(i, y_residual[i]), radius=0.04, color=ORANGE)
            for i in range(n_points)
        ])

        residual_text = MathTex(r"y_t - \ell - b \cdot t - s_t = \epsilon_t", font_size=32, color=ORANGE).to_edge(DR)

        self.play(
            Transform(axes, residual_axes),
            Transform(dots, new_dots_3),
            FadeOut(seasonal_wave),
            Transform(level_text, residual_text),
            run_time=2
        )
        self.wait(0.5)

        # Zero line to show residuals are centered
        zero_line = DashedLine(
            residual_axes.c2p(0, 0),
            residual_axes.c2p(n_points, 0),
            color=WHITE, dash_length=0.1
        )
        zero_label = Text("ε ≈ 0", font_size=20).next_to(zero_line, RIGHT)
        self.play(Create(zero_line), Write(zero_label))
        self.wait(0.5)

        # --- STEP 4: Recombine everything ---
        step4_label = Text("Recombine: Level + Trend + Seasonality", font_size=22, color=YELLOW).to_edge(UP)
        self.play(Transform(component_title, step4_label))

        # Return to original axes
        original_axes = Axes(
            x_range=[0, n_points, 12],
            y_range=[60, 160, 20],
            x_length=11,
            y_length=5,
            axis_config={"include_tip": False},
        ).shift(DOWN * 0.5)

        original_dots = VGroup(*[
            Dot(original_axes.c2p(i, y_original[i]), radius=0.04, color=WHITE)
            for i in range(n_points)
        ])

        recombine_text = MathTex(r"y_t = \ell + b \cdot t + s_t + \epsilon_t", font_size=32, color=YELLOW).to_edge(DR)

        self.play(
            Transform(axes, original_axes),
            Transform(dots, original_dots),
            FadeOut(zero_line), FadeOut(zero_label),
            Transform(level_text, recombine_text),
            run_time=2
        )

        # Add back axis labels
        x_label = Text("Time (months)", font_size=20).next_to(original_axes, DOWN)
        y_label = Text("Value", font_size=20).rotate(PI / 2).next_to(original_axes, LEFT)
        self.play(Write(x_label), Write(y_label))
        self.wait(0.5)

        # Clean up for next section
        self.play(FadeOut(component_title), FadeOut(level_text))

        # === SHOW SMOOTHING PROCESS ===
        smooth_title = Text("Smoothing follows the data", font_size=28).to_edge(UP)
        self.play(Write(smooth_title))

        # Compute Holt-Winters manually (additive)
        alpha, beta, gamma = 0.3, 0.1, 0.3
        m = 12  # seasonal period

        # Initialize
        l = np.zeros(n_points)
        b = np.zeros(n_points)
        s = np.zeros(n_points + m)

        # Initial values
        l[0] = np.mean(y[:m])
        b[0] = (np.mean(y[m:2*m]) - np.mean(y[:m])) / m
        for i in range(m):
            s[i] = y[i] - l[0]

        # Holt-Winters iteration
        fitted = np.zeros(n_points)
        fitted[0] = l[0] + b[0] + s[0]

        for t in range(1, n_points):
            l[t] = alpha * (y[t] - s[t]) + (1 - alpha) * (l[t-1] + b[t-1])
            b[t] = beta * (l[t] - l[t-1]) + (1 - beta) * b[t-1]
            s[t + m] = gamma * (y[t] - l[t]) + (1 - gamma) * s[t]
            fitted[t] = l[t] + b[t] + s[t + m]

        # Animate the fitted line being drawn
        fitted_line = VMobject(color=YELLOW, stroke_width=3)
        fitted_line.set_points_smoothly([axes.c2p(i, fitted[i]) for i in range(n_points)])

        hw_label = Text("Holt-Winters Fit", font_size=20, color=YELLOW).to_edge(UR).shift(DOWN)

        self.play(Create(fitted_line, run_time=3), Write(hw_label))
        self.wait(0.5)

        # === FORECAST ===
        forecast_title = Text("Forecasting into the future", font_size=28).to_edge(UP)
        self.play(Transform(smooth_title, forecast_title))

        # Generate forecast
        n_forecast = 12
        forecast = np.zeros(n_forecast)
        for h in range(1, n_forecast + 1):
            forecast[h-1] = l[-1] + h * b[-1] + s[n_points + (h - 1) % m]

        # Create NEW expanded axes
        new_axes = Axes(
            x_range=[0, n_points + n_forecast, 12],
            y_range=[60, 160, 20],
            x_length=11,
            y_length=5,
            axis_config={"include_tip": False},
        ).shift(DOWN * 0.5)

        new_x_label = Text("Time (months)", font_size=20).next_to(new_axes, DOWN)
        new_y_label = Text("Value", font_size=20).rotate(PI / 2).next_to(new_axes, LEFT)

        # Reposition dots on new axes
        new_dots = VGroup(*[
            Dot(new_axes.c2p(i, y[i]), radius=0.04, color=WHITE)
            for i in range(n_points)
        ])

        # Reposition fitted line on new axes
        new_fitted_line = VMobject(color=YELLOW, stroke_width=3)
        new_fitted_line.set_points_smoothly([new_axes.c2p(i, fitted[i]) for i in range(n_points)])

        # Animate the axes expansion (everything scales smoothly)
        self.play(
            Transform(axes, new_axes),
            Transform(x_label, new_x_label),
            Transform(y_label, new_y_label),
            Transform(dots, new_dots),
            Transform(fitted_line, new_fitted_line),
            run_time=1.5
        )

        # Dashed line for forecast region boundary
        forecast_region = DashedLine(
            new_axes.c2p(n_points, 60),
            new_axes.c2p(n_points, 160),
            color=GRAY
        )

        # Now create forecast line on the NEW axes
        forecast_line = VMobject(color=RED, stroke_width=3)
        forecast_points = [new_axes.c2p(n_points + i, forecast[i]) for i in range(n_forecast)]
        forecast_line.set_points_smoothly(forecast_points)

        forecast_label = Text("Forecast", font_size=20, color=RED)
        forecast_label.next_to(new_axes.c2p(n_points + n_forecast, forecast[-1]), RIGHT)

        self.play(Create(forecast_region))
        self.play(Create(forecast_line, run_time=2), Write(forecast_label))
        self.wait(1)

        # Final summary
        self.play(FadeOut(smooth_title))
        summary = VGroup(
            MathTex(r"\alpha", r" = \text{level smoothing}", font_size=28),
            MathTex(r"\beta", r" = \text{trend smoothing}", font_size=28),
            MathTex(r"\gamma", r" = \text{seasonal smoothing}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)
        summary[0][0].set_color(BLUE)
        summary[1][0].set_color(GREEN)
        summary[2][0].set_color(ORANGE)

        self.play(Write(summary))
        self.wait(2)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Final message
        final = Text("Any Questions?", font_size=48)
        self.play(Write(final))
        self.wait(2)
