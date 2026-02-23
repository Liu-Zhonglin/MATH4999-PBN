from manim import *
from manim_slides.slide import Slide
import numpy as np


class Section1IntroductionMotivation(Slide):
    def construct(self):
        # ========================================
        # SLIDE 1: TITLE PAGE (Frame 1)
        # ========================================

        # Main title with proper line breaks
        main_title = Tex(
            r"\textbf{Optimal Control Policy for}\\",
            r"\textbf{Probabilistic Boolean Networks}\\",
            r"\textbf{with Hard Constraints}",
            font_size=42, color=BLUE
        ).move_to(UP * 1.8)

        # Authors
        authors = Tex(
            r"Ching et al., IET Systems Biology (2009)",
            font_size=32, color=WHITE
        ).move_to(UP * 0.6)

        # Presentation info
        presentation = Tex(
            r"MATH4999 Presentation",
            font_size=28, color=GREEN
        ).move_to(DOWN * 0.5)

        presenter = Tex(
            r"Liu Zhonglin",
            font_size=28, color=GREEN
        ).move_to(DOWN * 1.1)

        uid = Tex(
            r"UID: 3035974614",
            font_size=28, color=GREEN
        ).move_to(DOWN * 1.7)

        # Background decoration
        bg_rect = Rectangle(
            width=config.frame_width - 0.8,
            height=config.frame_height - 0.8,
            stroke_color=BLUE,
            stroke_width=2,
            fill_opacity=0
        )

        self.wait()
        self.next_slide()

        # ==== TITLE PAGE ANIMATION ====
        self.play(Create(bg_rect), run_time=1)

        self.play(DrawBorderThenFill(main_title, shift=DOWN * 0.5, scale=0.8), run_time=2)

        self.play(FadeIn(authors, shift=RIGHT * 2), run_time=1.5)


        self.play(
            FadeIn(presentation, shift=UP * 1),
            FadeIn(presenter, shift=UP * 1),
            FadeIn(uid, shift=UP * 1),
            run_time=1.5
        )
        self.wait()
        self.next_slide()

        # Clear screen for next slide
        self.play(FadeOut(VGroup(
            bg_rect, main_title, authors, presentation, presenter, uid
        )))

        # ========================================
        # SLIDE 2: OUTLINE (Frame 2)
        # ========================================

        outline_title = Tex(r"\textbf{Outline}", font_size=48, color=BLUE)
        outline_title.move_to(UP * 3.2)

        # Outline items - UPDATED TO 4 SECTIONS
        outline_items = [
            r"1. Introduction and Motivation",
            r"2. Hard Constraints",
            r"3. Dynamic Programming Solution",
            r"4. Approximation, Results and Conclusion"
        ]

        colors = [GREEN, ORANGE, RED, PURPLE]
        text_left_edge = -3.5

        bullets, outline_texts, boxes = [], [], []

        for i, (item, color) in enumerate(zip(outline_items, colors)):
            bullet = Tex(r"$\bullet$", font_size=40, color=color)
            bullet.move_to([text_left_edge - 0.5, 2.2 - i * 1.1, 0])
            bullets.append(bullet)

            text = Tex(item, font_size=32, color=color)
            text.next_to(bullet, RIGHT, buff=0.3)
            outline_texts.append(text)

            # Box
            content_group = VGroup(bullet, text)
            box = Rectangle(
                width=content_group.width + 1.0,
                height=0.8,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.1
            )
            box.move_to(content_group.get_center())
            boxes.append(box)

        # ========= OUTLINE ANIMATION =========
        self.play(Write(outline_title), run_time=1.5)
        self.wait(0.5)

        # Show each item one slide at a time
        for i, (box, bullet, text) in enumerate(zip(boxes, bullets, outline_texts)):
            self.play(
                DrawBorderThenFill(box),
                Create(bullet),
                run_time=1
            )
            self.play(FadeIn(text, shift=LEFT * 0.5), run_time=1)
            self.wait(0.3)
            # Each outline point gets its own slide transition
            self.next_slide()

        # Optional highlight flashing
        self.play(
            *[box.animate.set_stroke_width(4) for box in boxes],
            run_time=0.8
        )
        self.play(
            *[box.animate.set_stroke_width(2) for box in boxes],
            run_time=0.8
        )

        # Elegant fade-out
        all_outline_elements = VGroup(
            outline_title, *outline_texts, *bullets, *boxes
        )
        self.play(
            LaggedStart(
                *[
                    element.animate.rotate(PI / 4).scale(0).set_opacity(0)
                    for element in all_outline_elements
                ],
                lag_ratio=0.1,
                run_time=2.5
            )
        )

        self.next_slide()

        # ========================================
        # CREATE PERSISTENT SECTION TITLE
        # ========================================
        section_title = Tex(
            r"\textbf{Section 1: The Setup (PBNs \& Motivation)}",
            font_size=44, color=GREEN
        )
        section_title.to_edge(UP, buff=0.3)

        # Show section title - it will remain throughout Section 1
        self.play(Write(section_title), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        # ========================================
        # SLIDE 3: WHAT IS A PBN
        # ========================================

        # Subsection: What is a PBN
        subsection_title = Tex(
            r"\textbf{What is a Probabilistic Boolean Network (PBN)?}",
            font_size=36, color=BLUE
        )
        subsection_title.next_to(section_title, DOWN, buff=0.4)

        # Definition
        definition = Tex(
            r"A \textbf{stochastic ensemble} of Boolean networks;\\",
            r"induces a \textbf{Markov chain} on $2^n$ Boolean states.",
            font_size=30, color=WHITE
        )
        definition.next_to(subsection_title, DOWN, buff=0.5)

        # Visual: Boolean Network Example
        gene_labels = [Tex(r"$x_1$", font_size=28),
                       Tex(r"$x_2$", font_size=28),
                       Tex(r"$x_3$", font_size=28)]

        gene_circles = []
        positions = [LEFT * 3, ORIGIN, RIGHT * 3]

        for i, (label, pos) in enumerate(zip(gene_labels, positions)):
            circle = Circle(radius=0.5, color=YELLOW, fill_opacity=0.3, stroke_width=3)
            circle.move_to(pos + UP * 0.5)
            label.move_to(circle.get_center())
            gene_circles.append(VGroup(circle, label))

        # Add arrows showing interactions
        arrow1 = Arrow(gene_circles[0].get_right(), gene_circles[1].get_left(),
                       buff=0.5, stroke_width=3, color=ORANGE)
        arrow2 = Arrow(gene_circles[1].get_right(), gene_circles[2].get_left(),
                       buff=0.5, stroke_width=3, color=ORANGE)
        arrow3 = CurvedArrow(gene_circles[2].get_center(), gene_circles[0].get_center(),
                             angle=-TAU / 4, stroke_width=3, color=ORANGE,
                             tip_length=0.2)

        network_visual = VGroup(*gene_circles, arrow1, arrow2, arrow3)
        network_visual.move_to(DOWN * 0.8)

        # State space visualization
        state_text = Tex(
            r"\textbf{State space:} $\{0,1\}^n \rightarrow 2^n$ states",
            font_size=26, color=YELLOW
        )
        state_text.next_to(network_visual, DOWN, buff=0.6)

        example_states = MathTex(
            r"\text{Example: } n=3 \Rightarrow 2^3=8 \text{ states: }",
            r"000, 001, 010, \ldots, 111",
            font_size=24, color=WHITE
        )
        example_states.next_to(state_text, DOWN, buff=0.3)

        # Animation
        self.play(Write(subsection_title), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(definition, shift=DOWN * 0.3), run_time=2)
        self.wait(0.5)
        self.next_slide()

        # Show network visual
        self.play(
            LaggedStart(
                *[FadeIn(gc, scale=0.5) for gc in gene_circles],
                lag_ratio=0.3
            ),
            run_time=2
        )
        self.play(
            GrowArrow(arrow1),
            GrowArrow(arrow2),
            Create(arrow3),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        self.play(
            Write(state_text),
            Write(example_states),
            run_time=2
        )
        self.wait(1)
        self.next_slide()

        # Clear for next slide (but keep section_title!)
        slide3_elements = VGroup(
            subsection_title, definition,
            network_visual, state_text, example_states
        )
        self.play(FadeOut(slide3_elements))

        # ========================================
        # SLIDE 4: DISTRIBUTION DYNAMICS
        # ========================================

        subsection_title2 = Tex(
            r"\textbf{Distribution Dynamics}",
            font_size=36, color=BLUE
        )
        subsection_title2.next_to(section_title, DOWN, buff=0.4)

        # Key idea
        key_idea = Tex(
            r"Work with the \textbf{state distribution} $v(t) \in \mathbb{R}^{2^n}$\\",
            r"rather than a single Boolean state.",
            font_size=30, color=WHITE, tex_environment='minipage}{9cm}'
        )
        key_idea.next_to(subsection_title2, DOWN, buff=0.5)

        # Transition matrix
        transition_box = Rectangle(
            width=11, height=2.5,
            stroke_color=ORANGE, stroke_width=2,
            fill_color=ORANGE, fill_opacity=0.1
        )
        transition_box.move_to(DOWN * 0.2)

        transition_formula = MathTex(
            r"P_0 = \sum_{j=1}^{N} p_j A_j,",
            r"\qquad",
            r"v(t+1) = P_0 \, v(t).",
            font_size=36, color=WHITE
        )
        transition_formula.move_to(transition_box.get_center())

        explanation = Tex(
            r"$P_0$: natural transition matrix (weighted average of $N$ Boolean networks)\\",
            r"$p_j$: selection probability for network $j$, $A_j$: its transition matrix\\",
            r"$v(t)$: probability distribution over $2^n$ states at time $t$",
            font_size=24, color=YELLOW, tex_environment='minipage}{12cm}'
        )
        explanation.next_to(transition_box, DOWN, buff=0.5)

        # Animation
        self.play(Write(subsection_title2), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(key_idea, shift=DOWN * 0.3), run_time=2)
        self.wait(0.5)
        self.next_slide()

        self.play(
            DrawBorderThenFill(transition_box),
            Write(transition_formula),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(explanation, shift=UP * 0.3), run_time=2)
        self.wait(1)
        self.next_slide()

        # Clear for next slide (but keep section_title!)
        slide4_elements = VGroup(
            subsection_title2, key_idea,
            transition_box, transition_formula, explanation
        )
        self.play(FadeOut(slide4_elements))

        # ========================================
        # SLIDE 5: WHY CONTROL
        # ========================================

        subsection_title3 = Tex(
            r"\textbf{Why Control?}",
            font_size=36, color=BLUE
        )
        subsection_title3.next_to(section_title, DOWN, buff=0.4)

        motivation = Tex(
            r"\textbf{Interventions} (e.g., therapy) bias the dynamics\\",
            r"away from \textbf{undesirable regimes}\\",
            r"toward \textbf{desirable regimes}.",
            font_size=30, color=WHITE, tex_environment='minipage}{9cm}'
        )
        motivation.next_to(subsection_title3, DOWN, buff=0.5)

        # Visual: trajectory comparison
        axes_left = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.5],
            x_length=4,
            y_length=2.5,
            tips=False,
            axis_config={"include_numbers": False}
        ).move_to(LEFT * 3 + DOWN * 1)

        axes_left_title = Tex(r"\textbf{No Control}", font_size=26, color=RED)
        axes_left_title.next_to(axes_left, UP, buff=0.2)

        uncontrolled_curve = axes_left.plot(
            lambda t: 0.3 + 0.4 * np.sin(t) - 0.05 * t,
            x_range=[0, 5],
            color=RED,
            stroke_width=3
        )

        bad_region = Rectangle(
            width=4, height=1,
            stroke_color=RED, stroke_width=2,
            fill_color=RED, fill_opacity=0.2
        ).move_to(axes_left.c2p(2.5, 0.25))

        bad_label = Tex(r"\textbf{Undesirable}", font_size=20, color=RED)
        bad_label.move_to(bad_region.get_center())

        # Controlled trajectory
        axes_right = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.5],
            x_length=4,
            y_length=2.5,
            tips=False,
            axis_config={"include_numbers": False}
        ).move_to(RIGHT * 3 + DOWN * 1)

        axes_right_title = Tex(r"\textbf{With Control}", font_size=26, color=GREEN)
        axes_right_title.next_to(axes_right, UP, buff=0.2)

        controlled_curve = axes_right.plot(
            lambda t: 0.3 + 0.2 * np.sin(t) + 0.1 * t,
            x_range=[0, 5],
            color=GREEN,
            stroke_width=3
        )

        good_region = Rectangle(
            width=4, height=1,
            stroke_color=GREEN, stroke_width=2,
            fill_color=GREEN, fill_opacity=0.2
        ).move_to(axes_right.c2p(2.5, 0.75))

        good_label = Tex(r"\textbf{Desirable}", font_size=20, color=GREEN)
        good_label.move_to(good_region.get_center())

        # Intervention markers
        intervention_dots = VGroup(*[
            Dot(axes_right.c2p(t, 0.3 + 0.2 * np.sin(t) + 0.1 * t),
                color=YELLOW, radius=0.08)
            for t in [1, 2, 3, 4]
        ])

        # Animation
        self.play(Write(subsection_title3), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(motivation, shift=DOWN * 0.3), run_time=2)
        self.wait(0.5)
        self.next_slide()

        # Show uncontrolled scenario
        self.play(
            Create(axes_left),
            Write(axes_left_title),
            run_time=1.5
        )
        self.play(
            FadeIn(bad_region),
            Write(bad_label),
            run_time=1
        )
        self.play(Create(uncontrolled_curve), run_time=2, rate_func=linear)
        self.wait(0.5)
        self.next_slide()

        # Show controlled scenario
        self.play(
            Create(axes_right),
            Write(axes_right_title),
            run_time=1.5
        )
        self.play(
            FadeIn(good_region),
            Write(good_label),
            run_time=1
        )
        self.play(Create(controlled_curve), run_time=2, rate_func=linear)
        self.play(FadeIn(intervention_dots), run_time=1)
        self.wait(1)
        self.next_slide()

        # Clear for next slide (but keep section_title!)
        slide5_elements = VGroup(
            subsection_title3, motivation,
            axes_left, axes_left_title, uncontrolled_curve, bad_region, bad_label,
            axes_right, axes_right_title, controlled_curve, good_region, good_label,
            intervention_dots
        )
        self.play(FadeOut(slide5_elements))

        # ========================================
        # SLIDE 6: CONTROL MODEL
        # ========================================

        subsection_title4 = Tex(
            r"\textbf{Control Model (One Control Type)}",
            font_size=36, color=BLUE
        )
        subsection_title4.next_to(section_title, DOWN, buff=0.4)

        # Control equation box
        control_box = Rectangle(
            width=12, height=2.5,
            stroke_color=PURPLE, stroke_width=2,
            fill_color=PURPLE, fill_opacity=0.1
        )
        control_box.move_to(UP * 0.3)

        control_formula = MathTex(
            r"u_t \in \{0, 1\},",
            r"\qquad",
            r"v(t+1) = P_{u_t} \, v(t)",
            font_size=36, color=WHITE
        )
        control_formula.move_to(control_box.get_center())

        control_explanation = Tex(
            r"$P_0$: natural (no intervention),\quad $P_1$: controlled (with intervention)\\",
            r"$u_t = 0$: no treatment at time $t$,\quad $u_t = 1$: apply treatment",
            font_size=26, color=YELLOW, tex_environment='minipage}{12cm}'
        )
        control_explanation.next_to(control_box, DOWN, buff=0.4)



        # Animation
        self.play(Write(subsection_title4), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(
            DrawBorderThenFill(control_box),
            Write(control_formula),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(control_explanation, shift=UP * 0.3), run_time=2)
        self.wait(0.5)
        self.next_slide()







        # Clear for next slide (but keep section_title!)
        slide6_elements = VGroup(
            subsection_title4, control_box,
            control_formula, control_explanation,
        )
        self.play(FadeOut(slide6_elements))

        # ========================================
        # SLIDE 7: GOAL
        # ========================================

        subsection_title5 = Tex(
            r"\textbf{Goal: Steering Toward Target Distribution}",
            font_size=36, color=BLUE
        )
        subsection_title5.next_to(section_title, DOWN, buff=0.4)

        # Goal statement
        goal_statement = Tex(
            r"Steer $v(t)$ toward a \textbf{target distribution} $z$\\",
            r"($z$ is a unit vector or mixture),\\",
            r"measured by $\|v(t) - z\|$.",
            font_size=30, color=WHITE, tex_environment='minipage}{12cm}'
        )
        goal_statement.next_to(subsection_title5, DOWN, buff=0.5)

        # Objective box
        objective_box = Rectangle(
            width=4, height=1.5,
            stroke_color=RED, stroke_width=3,
            fill_color=RED, fill_opacity=0.15
        )
        objective_box.move_to(DOWN * 0.2)

        objective_formula = MathTex(
            r"\text{Minimize: } \|v(t) - z\|",
            font_size=36, color=RED
        )
        objective_formula.move_to(objective_box.get_center())

        # Visual: convergence to target
        num_states = 8
        bar_width = 0.35
        bar_positions = np.linspace(-3.5, 3.5, num_states)

        # Initial distribution (spread out)
        initial_heights = np.random.random(num_states) * 0.5 + 0.3
        initial_heights /= initial_heights.sum()

        # Target distribution (peaked)
        target_heights = np.zeros(num_states)
        target_heights[3] = 0.7
        target_heights[4] = 0.3

        bars_initial = VGroup(*[
            Rectangle(
                width=bar_width,
                height=h * 3,
                fill_color=BLUE,
                fill_opacity=0.6,
                stroke_width=1,
                stroke_color=WHITE
            ).align_to(ORIGIN + DOWN * 2, DOWN).shift(RIGHT * pos)
            for pos, h in zip(bar_positions, initial_heights)
        ]).shift(DOWN * 1)

        bars_target = VGroup(*[
            Rectangle(
                width=bar_width,
                height=h * 3,
                fill_color=GREEN,
                fill_opacity=0.6,
                stroke_width=2,
                stroke_color=GREEN
            ).align_to(ORIGIN + DOWN * 2, DOWN).shift(RIGHT * pos)
            for pos, h in zip(bar_positions, target_heights)
        ]).shift(DOWN * 1)

        initial_label = MathTex(r"v(0)", font_size=26, color=BLUE)
        initial_label.next_to(bars_initial, DOWN + LEFT * 0.3, buff=0.3)

        target_label = MathTex(r"z \text{ (target)}", font_size=26, color=GREEN)
        target_label.next_to(bars_target, DOWN + RIGHT * 0.3, buff=0.3)

        arrow_convergence = Arrow(
            bars_initial.get_center() + LEFT * 2,
            bars_target.get_center() + RIGHT * 2,
            stroke_width=4, color=YELLOW, buff=0.5
        )
        arrow_label = Tex(r"\textbf{Control}", font_size=24, color=YELLOW)
        arrow_label.next_to(arrow_convergence, UP, buff=0.1)

        # Animation
        self.play(Write(subsection_title5), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(goal_statement, shift=DOWN * 0.3), run_time=2)
        self.wait(0.5)
        self.next_slide()

        self.play(
            DrawBorderThenFill(objective_box),
            Write(objective_formula),
            run_time=2
        )

        # Flash objective to emphasize
        for _ in range(2):
            self.play(objective_box.animate.set_stroke_color(YELLOW), run_time=0.3)
            self.play(objective_box.animate.set_stroke_color(RED), run_time=0.3)

        self.wait(0.5)
        self.next_slide()

        # Show convergence visual
        self.play(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in bars_initial],
                lag_ratio=0.1
            ),
            FadeIn(initial_label),
            run_time=2
        )
        self.wait(0.5)

        self.play(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in bars_target],
                lag_ratio=0.1
            ),
            FadeIn(target_label),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        self.play(
            GrowArrow(arrow_convergence),
            Write(arrow_label),
            run_time=1.5
        )

        # Animate convergence
        self.play(
            Transform(bars_initial, bars_target),
            run_time=2.0,
            rate_func=smooth
        )
        self.wait(1)
        self.next_slide()

        # Final emphasis
        self.play(
            Circumscribe(objective_formula, Rectangle, color=YELLOW,
                         fade_out=True, time_width=1.5),
            run_time=2
        )
        self.wait(1)
        self.next_slide()

        # NOW fade out everything INCLUDING section_title at the very end
        everything = VGroup(
            section_title,  # NOW included in final fadeout
            subsection_title5, goal_statement,
            objective_box, objective_formula,
            bars_initial, bars_target, initial_label, target_label,
            arrow_convergence, arrow_label
        )
        self.play(FadeOut(everything))
        self.wait(0.5)

        self.next_slide()





class Section2HardConstraint(Slide):
    def construct(self):
        # ========================================
        # PERSISTENT SECTION TITLE
        # ========================================
        section_title = Tex(
            r"\textbf{Section 2: The Constraint (Hard Limit on Interventions)}",
            font_size=44, color=BLUE
        )
        section_title.to_edge(UP, buff=0.3)

        self.play(DrawBorderThenFill(section_title), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        # ========================================
        # SLIDE 1: HARD CONSTRAINT DEFINITION
        # ========================================

        subsection_title1 = Tex(
            r"\textbf{What is the Hard Constraint?}",
            font_size=36, color=GREEN
        )
        subsection_title1.next_to(section_title, DOWN, buff=0.4)

        # Explanation
        explanation = Tex(
            r"We can apply \textbf{at most $K$ interventions} over the entire horizon $T$.\\",
            r"This is a \textbf{hard constraint} (not a penalty).", tex_environment='minipage}{12cm}',
            font_size=30, color=WHITE
        )
        explanation.next_to(subsection_title1, DOWN, buff=0.5)

        # Constraint box - SMALLER
        constraint_box = Rectangle(
            width=7, height=1.5,
            stroke_color=RED, stroke_width=3,
            fill_color=RED, fill_opacity=0.15
        )
        constraint_box.next_to(explanation, DOWN, buff=0.5)

        constraint_formula = MathTex(
            r"\sum_{t=0}^{T-1} u_t \leq K,",
            r"\qquad",
            r"K \leq T",
            font_size=36, color=RED
        )
        constraint_formula.move_to(constraint_box.get_center())

        # Visual: timeline with K interventions
        timeline_label = Tex(
            r"\textbf{Example:} $T=10$ time steps, $K=3$ interventions allowed",
            font_size=26, color=YELLOW
        )
        timeline_label.next_to(constraint_box, DOWN, buff=0.5)

        # Timeline
        T_example = 10
        K_example = 3

        time_dots = VGroup(*[
            Dot(point=np.array([i * 0.9 - 4, -2.8, 0]), radius=0.12, color=GRAY)
            for i in range(T_example)
        ])

        time_labels = VGroup(*[
            MathTex(f"t={i}", font_size=20, color=GRAY).next_to(
                time_dots[i], DOWN, buff=0.15
            )
            for i in range(T_example)
        ])

        # Highlight K intervention times (e.g., t=2, 5, 8)
        intervention_times = [2, 5, 8]
        intervention_dots = VGroup(*[
            Dot(point=time_dots[t].get_center(), radius=0.18, color=RED)
            for t in intervention_times
        ])

        intervention_labels = VGroup(*[
            MathTex(r"u=1", font_size=25, color=RED).next_to(
                intervention_dots[i], UP, buff=0.2
            )
            for i in range(len(intervention_times))
        ])

        # Connecting line
        timeline_line = Line(
            time_dots[0].get_center() + LEFT * 0.3,
            time_dots[-1].get_center() + RIGHT * 0.3,
            stroke_width=2, color=GRAY
        )

        timeline_visual = VGroup(
            timeline_line, time_dots, time_labels,
            intervention_dots, intervention_labels
        )

        # Animation
        self.play(Write(subsection_title1), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(explanation, shift=DOWN * 0.3), run_time=2)
        self.wait(0.5)
        self.next_slide()

        self.play(
            DrawBorderThenFill(constraint_box),
            Write(constraint_formula),
            run_time=2
        )

        # Flash the constraint
        for _ in range(2):
            self.play(constraint_box.animate.set_stroke_color(YELLOW), run_time=0.3)
            self.play(constraint_box.animate.set_stroke_color(RED), run_time=0.3)

        self.wait(0.5)
        self.next_slide()

        # Show timeline example
        self.play(Write(timeline_label), run_time=1.5)
        self.play(
            Create(timeline_line),
            LaggedStart(*[FadeIn(dot, scale=0.5) for dot in time_dots], lag_ratio=0.1),
            run_time=2
        )
        self.play(
            LaggedStart(*[FadeIn(label) for label in time_labels], lag_ratio=0.05),
            run_time=1.5
        )
        self.wait(0.5)
        self.next_slide()

        # Highlight interventions
        self.play(
            LaggedStart(*[FadeIn(dot, scale=1.5) for dot in intervention_dots], lag_ratio=0.3),
            run_time=2
        )
        self.play(
            LaggedStart(*[Write(label) for label in intervention_labels], lag_ratio=0.2),
            run_time=1.5
        )
        self.wait(1)
        self.next_slide()

        # Clear for next slide
        slide1_elements = VGroup(
            subsection_title1, explanation, constraint_box, constraint_formula,
            timeline_label, timeline_visual
        )
        self.play(FadeOut(slide1_elements))

        # ========================================
        # SLIDE 2: COUNTER VARIABLE k
        # ========================================

        subsection_title2 = Tex(
            r"\textbf{Tracking Control Usage: Counter Variable $k$}",
            font_size=36, color=GREEN
        )
        subsection_title2.next_to(section_title, DOWN, buff=0.4)

        # Key idea
        key_idea = Tex(
            r"Introduce a \textbf{state variable} $k$ to track\\",
            r"how many interventions have been used so far.", tex_environment='minipage}{12cm}',
            font_size=30, color=WHITE
        )
        key_idea.next_to(subsection_title2, DOWN, buff=0.5)

        # Augmented state box - SMALLER
        state_box = Rectangle(
            width=8, height=1.3,
            stroke_color=PURPLE, stroke_width=2,
            fill_color=PURPLE, fill_opacity=0.1
        )
        state_box.next_to(key_idea, DOWN, buff=0.5)

        state_formula = MathTex(
            r"\text{DP state: } (v(t), t, k),",
            r"\qquad",
            r"0 \leq k \leq K",
            font_size=32, color=WHITE
        )
        state_formula.move_to(state_box.get_center())

        state_explanation = Tex(
            r"$v(t)$: current distribution \quad $t$: current time\\",
            r"$k$: number of controls used so far (feasibility: $k \leq K$)", tex_environment='minipage}{12cm}',
            font_size=24, color=YELLOW
        )
        state_explanation.next_to(state_box, DOWN, buff=0.4)

        # Visual: state transitions with k incrementing
        # Start state
        start_state = VGroup(
            Circle(radius=0.5, color=BLUE, fill_opacity=0.3, stroke_width=3),
            VGroup(
                MathTex(r"v(t)", font_size=20),
                MathTex(r"k", font_size=20, color=ORANGE)
            ).arrange(DOWN, buff=0.08)
        )
        start_state.move_to(LEFT * 4.5 + DOWN * 2.2)

        # Decision node
        decision = Circle(radius=0.4, color=ORANGE, fill_opacity=0.3, stroke_width=3)
        decision.move_to(LEFT * 2 + DOWN * 2.2)
        decision_label = MathTex(r"u_t?", font_size=22)
        decision_label.move_to(decision.get_center())

        # Branch 0 (no control)
        state0 = VGroup(
            Circle(radius=0.5, color=BLUE, fill_opacity=0.3, stroke_width=3),
            VGroup(
                MathTex(r"P_0v(t)", font_size=18),
                MathTex(r"k", font_size=20, color=ORANGE)
            ).arrange(DOWN, buff=0.08)
        )
        state0.move_to(RIGHT * 1 + DOWN * 3)

        arrow0 = Arrow(
            decision.get_bottom(),
            state0.get_left(),
            buff=0.1, stroke_width=3, color=BLUE, tip_length=0.2
        )
        label0 = MathTex(r"u_t=0", font_size=24, color=BLUE)
        label0.next_to(arrow0, DOWN, buff=0.05)

        # Branch 1 (control applied)
        state1 = VGroup(
            Circle(radius=0.5, color=RED, fill_opacity=0.3, stroke_width=3),
            VGroup(
                MathTex(r"P_1v(t)", font_size=18),
                MathTex(r"k+1", font_size=20, color=ORANGE)
            ).arrange(DOWN, buff=0.08)
        )
        state1.move_to(RIGHT * 4 + DOWN * 1.4)

        arrow1 = Arrow(
            decision.get_top(),
            state1.get_left(),
            buff=0.1, stroke_width=3, color=RED, tip_length=0.2
        )
        label1 = MathTex(r"u_t=1", font_size=24, color=RED)
        label1.next_to(arrow1, DOWN, buff=0.05)

        # Arrow from start to decision
        arrow_start = Arrow(
            start_state.get_right(),
            decision.get_left(),
            buff=0.1, stroke_width=3, color=WHITE, tip_length=0.2
        )

        state_diagram = VGroup(
            start_state, arrow_start, decision, decision_label,
            arrow0, label0, state0,
            arrow1, label1, state1
        )

        # Animation
        self.play(Write(subsection_title2), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(key_idea, shift=DOWN * 0.3), run_time=2)
        self.wait(0.5)
        self.next_slide()

        self.play(
            DrawBorderThenFill(state_box),
            Write(state_formula),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(state_explanation, shift=UP * 0.3), run_time=2)
        self.wait(0.5)
        self.next_slide()

        # Show state diagram
        self.play(FadeIn(start_state, scale=0.5), run_time=1)
        self.play(GrowArrow(arrow_start), run_time=1)
        self.play(
            DrawBorderThenFill(decision),
            Write(decision_label),
            run_time=1.5
        )
        self.wait(0.3)
        self.next_slide()

        # Show branches
        self.play(
            GrowArrow(arrow0),
            Write(label0),
            FadeIn(state0, shift=UP * 0.5),
            run_time=1.5
        )
        self.wait(0.5)
        self.next_slide()

        self.play(
            GrowArrow(arrow1),
            Write(label1),
            FadeIn(state1, shift=DOWN * 0.5),
            run_time=1.5
        )
        self.wait(1)

        # Highlight k+1
        self.play(
            Circumscribe(state1[1][1], Rectangle, color=ORANGE, fade_out=True),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        # Clear for next slide
        slide2_elements = VGroup(
            subsection_title2, key_idea, state_box, state_formula,
            state_explanation, state_diagram
        )
        self.play(FadeOut(slide2_elements))

        # ========================================
        # SLIDE 3: INFEASIBILITY WHEN k = K
        # ========================================

        subsection_title3 = Tex(
            r"\textbf{Infeasibility: When $k = K$}",
            font_size=36, color=GREEN
        )
        subsection_title3.next_to(section_title, DOWN, buff=0.4)

        # Explanation
        infeasibility_text = Tex(
            r"If we have already used $K$ controls ($k = K$),\\",
            r"then \textbf{no more interventions are allowed}.\\",
            r"Trying to apply control becomes \textbf{infeasible}.", tex_environment='minipage}{12cm}',
            font_size=28, color=WHITE
        )
        infeasibility_text.next_to(subsection_title3, DOWN, buff=0.5)

        # DP modeling box - SMALLER
        dp_box = Rectangle(
            width=7, height=1.2,
            stroke_color=RED, stroke_width=3,
            fill_color=RED, fill_opacity=0.15
        )
        dp_box.next_to(infeasibility_text, DOWN, buff=0.4)

        dp_formula = MathTex(
            r"D(\cdot, t, K+1) = +\infty",
            font_size=36, color=RED
        )
        dp_formula.move_to(dp_box.get_center())

        dp_explanation = Tex(
            r"In the DP recursion, attempting to use more than $K$ controls\\",
            r"results in infinite cost, making that branch infeasible.", tex_environment='minipage}{12cm}',
            font_size=24, color=YELLOW
        )
        dp_explanation.next_to(dp_box, DOWN, buff=0.4)

        # Visual: blocked path when k=K
        # Current state at k=K
        current_state_k = VGroup(
            Circle(radius=0.6, color=ORANGE, fill_opacity=0.3, stroke_width=3),
            VGroup(
                MathTex(r"v(t)", font_size=22),
                MathTex(r"k=K", font_size=22, color=RED)
            ).arrange(DOWN, buff=0.08)
        )
        current_state_k.move_to(LEFT * 4.5 + DOWN * 2.5)

        # Decision node
        decision_k = Circle(radius=0.4, color=ORANGE, fill_opacity=0.3, stroke_width=3)
        decision_k.move_to(LEFT * 2 + DOWN * 2.5)
        decision_label_k = MathTex(r"u_t?", font_size=22)
        decision_label_k.move_to(decision_k.get_center())

        arrow_to_decision = Arrow(
            current_state_k.get_right(),
            decision_k.get_left(),
            buff=0.1, stroke_width=3, color=WHITE
        )

        # Branch 0 (allowed)
        state0_k = VGroup(
            Circle(radius=0.6, color=GREEN, fill_opacity=0.3, stroke_width=3),
            VGroup(
                MathTex(r"P_0v(t)", font_size=20),
                MathTex(r"k=K", font_size=20, color=ORANGE)
            ).arrange(DOWN, buff=0.08)
        )
        state0_k.move_to(RIGHT * 1 + DOWN * 3.2)

        arrow0_k = Arrow(
            decision_k.get_bottom(),
            state0_k.get_top(),
            buff=0.1, stroke_width=3, color=GREEN
        )
        label0_k = MathTex(r"u_t=0 \;\checkmark", font_size=18, color=GREEN)
        label0_k.next_to(arrow0_k, LEFT, buff=0.1)

        # Branch 1 (blocked!)
        blocked_symbol = VGroup(
            Line(LEFT * 0.4, RIGHT * 0.4, stroke_width=5, color=RED),
            Line(DOWN * 0.4, UP * 0.4, stroke_width=5, color=RED)
        ).move_to(RIGHT * 4.2 + DOWN * 1.8)

        arrow1_k = Arrow(
            decision_k.get_top(),
            blocked_symbol.get_left(),
            buff=0.15, stroke_width=3, color=RED
        )
        label1_k = MathTex(r"u_t=1 \;\times", font_size=18, color=RED)
        label1_k.next_to(arrow1_k, UP, buff=0.1)

        infeasible_label = Tex(
            r"\textbf{INFEASIBLE}\\",
            r"$D = +\infty$",
            font_size=20, color=RED
        )
        infeasible_label.next_to(blocked_symbol, RIGHT, buff=0.25)

        # Animation
        self.play(Write(subsection_title3), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(infeasibility_text, shift=DOWN * 0.3), run_time=2)
        self.wait(0.5)
        self.next_slide()

        self.play(
            DrawBorderThenFill(dp_box),
            Write(dp_formula),
            run_time=2
        )

        # Flash infinity
        for _ in range(2):
            self.play(dp_formula.animate.set_color(YELLOW), run_time=0.3)
            self.play(dp_formula.animate.set_color(RED), run_time=0.3)

        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(dp_explanation, shift=UP * 0.3), run_time=2)
        self.wait(0.5)
        self.next_slide()

        self.wait(0.3)
        self.next_slide()

        # Final fadeout - including section title
        everything = VGroup(
            section_title,
            subsection_title3, infeasibility_text, dp_box, dp_formula,
            dp_explanation
        )
        self.play(FadeOut(everything))
        self.wait(0.5)
        self.next_slide()


class Section3_DPSolution(Slide):
    def construct(self):
        # ========================================
        # PERSISTENT SECTION TITLE
        # ========================================
        section_title = Tex(
            r"\textbf{Section 3: Dynamic Programming Solution}",
            font_size=44, color=BLUE
        )
        section_title.to_edge(UP, buff=0.3)

        self.play(DrawBorderThenFill(section_title), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        # ========================================
        # SLIDE 1: REACHABLE PREDICTED DISTRIBUTIONS
        # ========================================

        subsection_title1 = Tex(
            r"\textbf{Reachable Predicted Distributions}",
            font_size=36, color=GREEN
        )
        subsection_title1.next_to(section_title, DOWN, buff=0.4)

        # Control history explanation
        control_history_text = Tex(
            r"A \textbf{control history string:}",
            font_size=30, color=WHITE
        )
        control_history_text.next_to(subsection_title1, DOWN, buff=0.5)

        control_history_formula = MathTex(
            r"w_t = u_{t-1} \cdots u_1 u_0",
            font_size=36
        )
        control_history_formula.next_to(control_history_text, DOWN, buff=0.3)

        # Generated distribution
        generated_text = Tex(
            r"generates the \textbf{predicted distribution:}",
            font_size=30, color=WHITE
        )
        generated_text.next_to(control_history_formula, DOWN, buff=0.4)

        generated_formula = MathTex(
            r"v(w_t) = P_{u_{t-1}} \cdots P_{u_0} v_0",
            font_size=36
        )
        generated_formula.next_to(generated_text, DOWN, buff=0.3)

        # Feasibility constraint box
        feasibility_box = Rectangle(
            width=10, height=1.5,
            stroke_color=RED, stroke_width=3,
            fill_color=RED, fill_opacity=0.15
        )
        feasibility_box.next_to(generated_formula, DOWN, buff=0.5)

        feasibility_constraint = MathTex(
            r"\text{Feasibility: } \sum_{i=0}^{t-1} u_i \leq K",
            font_size=32, color=RED
        )
        feasibility_constraint.move_to(feasibility_box.get_center())

        # Animation
        self.play(Write(subsection_title1), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(control_history_text, shift=DOWN * 0.3), run_time=1.5)
        self.play(Write(control_history_formula), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(generated_text, shift=DOWN * 0.3), run_time=1.5)
        self.play(Write(generated_formula), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        self.play(
            DrawBorderThenFill(feasibility_box),
            Write(feasibility_constraint),
            run_time=2
        )

        # Flash constraint
        for _ in range(2):
            self.play(feasibility_box.animate.set_stroke_color(YELLOW), run_time=0.3)
            self.play(feasibility_box.animate.set_stroke_color(RED), run_time=0.3)

        self.wait(0.5)
        self.next_slide()

        # Clear for next slide
        slide1_elements = VGroup(
            subsection_title1, control_history_text, control_history_formula,
            generated_text, generated_formula, feasibility_box, feasibility_constraint
        )
        self.play(FadeOut(slide1_elements))

        # ========================================
        # SLIDE 2: TWO OBJECTIVES
        # ========================================

        subsection_title2 = Tex(
            r"\textbf{Two Objectives in the Paper}",
            font_size=36, color=GREEN
        )
        subsection_title2.next_to(section_title, DOWN, buff=0.4)

        # Terminal objective box
        terminal_box = Rectangle(
            width=10, height=2.2,
            stroke_color=ORANGE, stroke_width=2,
            fill_color=ORANGE, fill_opacity=0.1
        )
        terminal_box.move_to(UP * 0.8)

        terminal_content = VGroup(
            Tex(r"\textbf{Terminal-only objective (Eq. 4):}",
                font_size=28, color=ORANGE),
            MathTex(r"\min_{w_T} \|v(w_T) - z\|", font_size=34),
            Tex(r"subject to $\sum u_t \leq K$", font_size=24, color=GRAY)
        ).arrange(DOWN, buff=0.2)
        terminal_content.move_to(terminal_box.get_center())

        # Average objective box
        average_box = Rectangle(
            width=10, height=2.2,
            stroke_color=PURPLE, stroke_width=2,
            fill_color=PURPLE, fill_opacity=0.1
        )
        average_box.move_to(DOWN * 1.5)

        average_content = VGroup(
            Tex(r"\textbf{Average-over-time objective (Eq. 5):}",
                font_size=28, color=PURPLE),
            MathTex(r"\min_{w_T} \frac{1}{T} \sum_{t=1}^{T} \|v(w_t) - z\|",
                    font_size=34),
            Tex(r"subject to $\sum u_t \leq K$", font_size=24, color=GRAY)
        ).arrange(DOWN, buff=0.2)
        average_content.move_to(average_box.get_center())

        # Focus note
        focus_note = Tex(
            r"\textbf{Focus:} average objective with DP formulation",
            font_size=26, color=YELLOW
        )
        focus_note.next_to(average_box, DOWN, buff=0.5)

        # Animation
        self.play(Write(subsection_title2), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(
            DrawBorderThenFill(terminal_box),
            FadeIn(terminal_content, shift=DOWN * 0.3),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        self.play(
            DrawBorderThenFill(average_box),
            FadeIn(average_content, shift=DOWN * 0.3),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        self.play(Write(focus_note), run_time=1.5)

        # Highlight focus
        self.play(
            Circumscribe(average_content[1], Rectangle, color=YELLOW,
                         fade_out=True, time_width=1.5),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        # Clear for DP formulation
        slide2_elements = VGroup(
            subsection_title2, terminal_box, terminal_content,
            average_box, average_content, focus_note
        )
        self.play(FadeOut(slide2_elements))

        # ========================================
        # SLIDE: DP FORMULATION - AUGMENTED STATE (3-COLUMN)
        # ========================================

        subsection_title = Tex(
            r"\textbf{DP Formulation: Augmented State}",
            font_size=36, color=GREEN
        )
        subsection_title.next_to(section_title, DOWN, buff=0.4)

        # Main description
        aug_desc = Tex(
            r"Augment DP state with \textbf{used-controls counter:}",
            font_size=28
        )
        aug_desc.next_to(subsection_title, DOWN, buff=0.5)

        # ========================================
        # THREE COLUMNS
        # ========================================

        # COLUMN 1: State
        state_box = Rectangle(
            width=4.2, height=4,
            stroke_color=PURPLE, stroke_width=2,
            fill_color=PURPLE, fill_opacity=0.1
        )
        state_box.move_to(LEFT * 4.5 + DOWN * 1)

        state_title = Tex(
            r"\textbf{State:}",
            font_size=26, color=PURPLE
        )
        state_title.next_to(state_box.get_top(), DOWN, buff=0.3)

        state_content = MathTex(
            r"(t, k)",
            font_size=32
        )
        state_content.next_to(state_title, DOWN, buff=0.4)

        state_desc = Tex(
            r"where $k =$ controls\\used so far",
            font_size=22
        )
        state_desc.next_to(state_content, DOWN, buff=0.3)

        # COLUMN 2: Cost-to-go
        ctg_box = Rectangle(
            width=4.2, height=4,
            stroke_color=BLUE, stroke_width=2,
            fill_color=BLUE, fill_opacity=0.1
        )
        ctg_box.move_to(DOWN * 1)

        ctg_title = Tex(
            r"\textbf{Cost-to-go:}",
            font_size=26, color=BLUE
        )
        ctg_title.next_to(ctg_box.get_top(), DOWN, buff=0.3)

        ctg_equation = MathTex(
            r"D(v(w_t), t, k)",
            font_size=26
        )
        ctg_equation.next_to(ctg_title, DOWN, buff=0.3)

        ctg_def = MathTex(
            r":= \min \sum_{\tau=t+1}^{T}\|v(w_\tau) - z\|",
            font_size=22
        )
        ctg_def.next_to(ctg_equation, DOWN, buff=0.3)

        # COLUMN 3: Boundary
        bc_box = Rectangle(
            width=4.2, height=4,
            stroke_color=RED, stroke_width=2,
            fill_color=RED, fill_opacity=0.1
        )
        bc_box.move_to(RIGHT * 4.5 + DOWN * 1)

        bc_title = Tex(
            r"\textbf{Boundary:}",
            font_size=26, color=RED
        )
        bc_title.next_to(bc_box.get_top(), DOWN, buff=0.3)

        bc_equation = MathTex(
            r"D(v(w_T), T, k)",
            font_size=26
        )
        bc_equation.next_to(bc_title, DOWN, buff=0.3)

        bc_equals = MathTex(
            r"= \|v(w_T) - z\|",
            font_size=26
        )
        bc_equals.next_to(bc_equation, DOWN, buff=0.3)

        # Animation
        self.play(Write(subsection_title), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(aug_desc, shift=DOWN * 0.3), run_time=1)
        self.wait(0.5)
        self.next_slide()

        # Show all three columns
        self.play(
            DrawBorderThenFill(state_box),
            DrawBorderThenFill(ctg_box),
            DrawBorderThenFill(bc_box),
            run_time=1.5
        )
        self.wait(0.3)
        self.next_slide()

        # Fill in column 1
        self.play(
            Write(state_title),
            Write(state_content),
            Write(state_desc),
            run_time=1.5
        )
        self.wait(0.3)
        self.next_slide()

        # Fill in column 2
        self.play(
            Write(ctg_title),
            Write(ctg_equation),
            Write(ctg_def),
            run_time=1.5
        )
        self.wait(0.3)
        self.next_slide()

        # Fill in column 3
        self.play(
            Write(bc_title),
            Write(bc_equation),
            Write(bc_equals),
            run_time=1.5
        )
        self.wait(0.5)
        self.next_slide()

        # Clear for next slide
        slide_elements = VGroup(
            subsection_title, aug_desc,
            state_box, state_title, state_content, state_desc,
            ctg_box, ctg_title, ctg_equation, ctg_def,
            bc_box, bc_title, bc_equation, bc_equals
        )
        self.play(FadeOut(slide_elements))

        # ========================================
        # SLIDE 4: BELLMAN RECURSION
        # ========================================

        subsection_title4 = Tex(
            r"\textbf{Bellman Recursion (Eq. 6)}",
            font_size=36, color=GREEN
        )
        subsection_title4.next_to(section_title, DOWN, buff=0.4)

        # Main recursion equation box
        bellman_box = Rectangle(
            width=12, height=3,
            stroke_color=ORANGE, stroke_width=3,
            fill_color=ORANGE, fill_opacity=0.1
        )
        bellman_box.move_to(UP * 0.3)

        bellman_eq = MathTex(
            r"D(v(w_t), t, k) = \min \begin{cases} "
            r"\|P_0 v(w_t) - z\| + D(P_0 v(w_t), t+1, k) \\ "
            r"\|P_1 v(w_t) - z\| + D(P_1 v(w_t), t+1, k+1) "
            r"\end{cases}",
            font_size=26
        )
        bellman_eq.move_to(bellman_box.get_center())

        # Explanation boxes for two choices
        no_control_box = Rectangle(
            width=5, height=1.5,
            stroke_color=BLUE, stroke_width=2,
            fill_color=BLUE, fill_opacity=0.1
        )
        no_control_box.move_to(LEFT * 3 + DOWN * 2)

        no_control_text = VGroup(
            Tex(r"\textbf{No control} $(u_t = 0)$:", font_size=24, color=BLUE),
            Tex(r"Use $P_0$, keep $k$ unchanged", font_size=22)
        ).arrange(DOWN, buff=0.15)
        no_control_text.move_to(no_control_box.get_center())

        with_control_box = Rectangle(
            width=5, height=1.5,
            stroke_color=RED, stroke_width=2,
            fill_color=RED, fill_opacity=0.1
        )
        with_control_box.move_to(RIGHT * 3 + DOWN * 2)

        with_control_text = VGroup(
            Tex(r"\textbf{Apply control} $(u_t = 1)$:", font_size=24, color=RED),
            Tex(r"Use $P_1$, increment $k \to k+1$", font_size=22)
        ).arrange(DOWN, buff=0.15)
        with_control_text.move_to(with_control_box.get_center())

        # Hard constraint note
        constraint_note = Tex(
            r"\textbf{If } $k = K$: second option rejected ($D(\cdot,t+1,K+1) = \infty$)",
            font_size=24, color=RED
        )
        constraint_note.to_edge(DOWN, buff=0.5)

        # Animation
        self.play(Write(subsection_title4), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(
            DrawBorderThenFill(bellman_box),
            Write(bellman_eq),
            run_time=2.5
        )
        self.wait(0.5)
        self.next_slide()

        # Show choice explanations
        self.play(
            DrawBorderThenFill(no_control_box),
            FadeIn(no_control_text, shift=RIGHT * 0.3),
            run_time=2
        )
        self.wait(0.3)
        self.next_slide()

        self.play(
            DrawBorderThenFill(with_control_box),
            FadeIn(with_control_text, shift=LEFT * 0.3),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        self.play(Write(constraint_note), run_time=2)

        # Flash constraint
        for _ in range(2):
            self.play(constraint_note.animate.set_color(YELLOW), run_time=0.3)
            self.play(constraint_note.animate.set_color(RED), run_time=0.3)

        self.wait(0.5)
        self.next_slide()

        # Clear for algorithm visualization
        slide4_elements = VGroup(
            subsection_title4, bellman_box, bellman_eq,
            no_control_box, no_control_text,
            with_control_box, with_control_text,
            constraint_note
        )
        self.play(FadeOut(slide4_elements))

        # ========================================
        # SLIDE 5: FANCY ALGORITHM VISUALIZATION
        # ========================================

        subsection_title5 = Tex(
            r"\textbf{Algorithm: Backward Induction}",
            font_size=36, color=GREEN
        )
        subsection_title5.next_to(section_title, DOWN, buff=0.4)

        # Algorithm pseudocode box with gradient effect
        algo_frame = Rectangle(
            width=13, height=5.5,
            stroke_color=PURPLE, stroke_width=3,
            fill_color=PURPLE, fill_opacity=0.05
        )
        algo_frame.move_to(DOWN * 0.3)

        # Title bar for algorithm
        algo_title_bar = Rectangle(
            width=13, height=0.6,
            stroke_width=0,
            fill_color=PURPLE, fill_opacity=0.3
        )
        algo_title_bar.next_to(algo_frame.get_top(), DOWN, buff=0)

        algo_title = Tex(
            r"\texttt{ALGORITHM: DP with Hard Constraints}",
            font_size=26, color=PURPLE
        )
        algo_title.move_to(algo_title_bar.get_center())

        # Step-by-step algorithm content
        algo_steps = VGroup(
            # Initialization
            MathTex(
                r"\textbf{Initialize:} \quad D(v(w_T), T, k) = \|v(w_T) - z\|",
                font_size=24
            ),
            MathTex(
                r"\phantom{\textbf{Initialize:}} \quad D(\cdot, t, K+1) = +\infty \text{ for all } t",
                font_size=24, color=RED
            ),

            # Main loop
            Tex(
                r"\textbf{For } $t = T-1, T-2, \ldots, 0$:",
                font_size=24, color=BLUE
            ),
            Tex(
                r"$\quad$ \textbf{For each} reachable $(v(w_t), k)$ with $k \leq K$:",
                font_size=22
            ),

            # Decision computation
            MathTex(
                r"\qquad \text{Compute: } "
                r"c_0 = \|P_0 v(w_t) - z\| + D(P_0 v(w_t), t+1, k)",
                font_size=20
            ),
            MathTex(
                r"\qquad \text{Compute: } "
                r"c_1 = \|P_1 v(w_t) - z\| + D(P_1 v(w_t), t+1, k+1)",
                font_size=20
            ),

            # Optimal decision
            MathTex(
                r"\qquad u^*_t(v,k) = \arg\min\{c_0, c_1\}",
                font_size=22, color=GREEN
            ),
            MathTex(
                r"\qquad D(v(w_t), t, k) = \min\{c_0, c_1\}",
                font_size=22, color=GREEN
            ),

            # Output
            Tex(
                r"\textbf{Return:} Optimal policy $\{u^*_t\}_{t=0}^{T-1}$",
                font_size=24, color=ORANGE
            )
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        algo_steps.next_to(algo_title_bar, DOWN, buff=0.3)

        # Animation
        self.play(Write(subsection_title5), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(
            DrawBorderThenFill(algo_frame),
            FadeIn(algo_title_bar),
            Write(algo_title),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        # Animate each step appearing
        for i, step in enumerate(algo_steps):
            if i in [0, 2, 8]:  # Highlight important steps
                self.play(
                    FadeIn(step, shift=DOWN * 0.2),
                    step.animate.set_color(YELLOW),
                    run_time=1.5
                )
                self.play(step.animate.set_color(WHITE), run_time=0.5)
            else:
                self.play(FadeIn(step, shift=DOWN * 0.2), run_time=1)

            self.wait(0.3)
            if i in [1, 3, 7]:  # Add slides at key points
                self.next_slide()

        self.wait(0.5)
        self.next_slide()

        # Add decorative elements
        decorative_dots = VGroup(*[
            Dot(color=PURPLE, radius=0.05).move_to(
                algo_frame.get_corner(UL) + RIGHT * (0.5 + i * 0.3) + DOWN * 0.3
            )
            for i in range(3)
        ])

        self.play(FadeIn(decorative_dots), run_time=0.5)
        self.wait(0.5)
        self.next_slide()

        # Clear for complexity analysis
        slide5_elements = VGroup(
            subsection_title5, algo_frame, algo_title_bar,
            algo_title, algo_steps, decorative_dots
        )
        self.play(FadeOut(slide5_elements))

        # ========================================
        # SLIDE 6: COMPLEXITY & KEY PROPERTIES (2-COLUMN FORMAT)
        # ========================================

        subsection_title6 = Tex(
            r"\textbf{Algorithm Properties}",
            font_size=36, color=GREEN
        )
        subsection_title6.next_to(section_title, DOWN, buff=0.4)

        # LEFT COLUMN: Complexity
        complexity_box = Rectangle(
            width=6, height=2.2,
            stroke_color=ORANGE, stroke_width=3,
            fill_color=ORANGE, fill_opacity=0.1
        )
        complexity_box.move_to(LEFT * 3 + UP * 0.8)

        complexity_content = VGroup(
            Tex(r"\textbf{Time Complexity:}", font_size=26, color=ORANGE),
            MathTex(
                r"O(T \cdot K \cdot |\text{Reachable}(t)|)",
                font_size=28
            ),
            Tex(
                r"where $|\text{Reachable}(t)|$ is\\number of distributions at time $t$",
                font_size=20, color=GRAY
            )
        ).arrange(DOWN, buff=0.2)
        complexity_content.move_to(complexity_box.get_center())

        # RIGHT COLUMN: Three property boxes stacked
        property_boxes = []
        property_contents = []

        props = [
            (r"\textbf{Optimality}",
             r"Bellman optimality principle\\guarantees global optimum",
             BLUE),
            (r"\textbf{Feasibility}",
             r"Hard constraint $\sum u_t \leq K$\\enforced via $D(\cdot,\cdot,K+1)=\infty$",
             RED),
            (r"\textbf{Tractability}",
             r"Exponential in $n$ (state space size)\\but polynomial in $T$, $K$",
             PURPLE)
        ]

        y_positions = [1.3, 0, -1.3]

        for i, ((title, desc, color), y_pos) in enumerate(zip(props, y_positions)):
            box = Rectangle(
                width=6, height=1.1,
                stroke_color=color, stroke_width=2,
                fill_color=color, fill_opacity=0.1
            )
            box.move_to(RIGHT * 3 + y_pos * UP)

            content = VGroup(
                Tex(title, font_size=22, color=color),
                Tex(desc, font_size=19)
            ).arrange(DOWN, buff=0.12)
            content.move_to(box.get_center())

            property_boxes.append(box)
            property_contents.append(content)

        # Animation
        self.play(Write(subsection_title6), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        # Show left column (complexity)
        self.play(
            DrawBorderThenFill(complexity_box),
            run_time=1.5
        )
        for item in complexity_content:
            self.play(FadeIn(item, shift=DOWN * 0.3), run_time=1)
            self.wait(0.2)

        self.wait(0.5)
        self.next_slide()

        # Show right column properties one by one
        for box, content in zip(property_boxes, property_contents):
            self.play(
                DrawBorderThenFill(box),
                FadeIn(content, shift=LEFT * 0.3),
                run_time=1.5
            )
            self.wait(0.3)
            self.next_slide()

        # Clear for summary
        slide6_elements = VGroup(
            subsection_title6, complexity_box, complexity_content,
            *property_boxes, *property_contents
        )
        self.play(FadeOut(slide6_elements))

        # ========================================
        # SLIDE 7: SUMMARY WITH VISUAL FLOW
        # ========================================

        summary_title = Tex(
            r"\textbf{Summary: DP with Hard Constraints}",
            font_size=38, color=GREEN
        )
        summary_title.next_to(section_title, DOWN, buff=0.5)

        # Create flow diagram
        flow_boxes = []
        flow_labels = []
        flow_arrows = []

        steps_data = [
            (r"Augment\\State", r"(t, k)", PURPLE, LEFT * 4.5 + UP * 0.5),
            (r"Define\\Cost-to-Go", r"D(v,t,k)", BLUE, LEFT * 1.5 + UP * 0.5),
            (r"Bellman\\Equation", r"\min\{c_0,c_1\}", ORANGE, RIGHT * 1.5 + UP * 0.5),
            (r"Backward\\Induction", r"t=T-1\to 0", RED, RIGHT * 4.5 + UP * 0.5)
        ]

        for i, (title, formula, color, pos) in enumerate(steps_data):
            box = RoundedRectangle(
                width=2, height=1.5,
                corner_radius=0.2,
                stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.15
            )
            box.move_to(pos)

            label = VGroup(
                Tex(title, font_size=20, color=color),
                MathTex(formula, font_size=24)
            ).arrange(DOWN, buff=0.15)
            label.move_to(box.get_center())

            flow_boxes.append(box)
            flow_labels.append(label)

            if i < len(steps_data) - 1:
                arrow = Arrow(
                    box.get_right(),
                    steps_data[i + 1][3] + LEFT * 1,
                    buff=0.1, stroke_width=4,
                    color=YELLOW
                )
                flow_arrows.append(arrow)

        # Result box
        result_box = RoundedRectangle(
            width=10, height=1.8,
            corner_radius=0.3,
            stroke_color=GREEN, stroke_width=4,
            fill_color=GREEN, fill_opacity=0.2
        )
        result_box.move_to(DOWN * 1.5)

        result_text = VGroup(
            Tex(r"\textbf{Output:}", font_size=28, color=GREEN),
            Tex(r"Optimal policy $\{u^*_t\}_{t=0}^{T-1}$ respecting $\sum u_t \leq K$",
                font_size=24)
        ).arrange(DOWN, buff=0.2)
        result_text.move_to(result_box.get_center())

        # Final arrow to result
        final_arrow = Arrow(
            flow_boxes[-1].get_bottom(),
            result_box.get_top(),
            buff=0.1, stroke_width=5,
            color=GREEN, tip_length=0.2
        )

        # Animation
        self.play(Write(summary_title), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        # Animate flow
        for i, (box, label) in enumerate(zip(flow_boxes, flow_labels)):
            self.play(
                DrawBorderThenFill(box),
                FadeIn(label, scale=0.8),
                run_time=1.2
            )
            if i < len(flow_arrows):
                self.play(GrowArrow(flow_arrows[i]), run_time=0.8)
            self.wait(0.3)
            self.next_slide()

        # Show result
        self.play(GrowArrow(final_arrow), run_time=1)
        self.play(
            DrawBorderThenFill(result_box),
            FadeIn(result_text, shift=UP * 0.3),
            run_time=2
        )

        # Flash result
        for _ in range(2):
            self.play(result_box.animate.set_stroke_color(YELLOW), run_time=0.4)
            self.play(result_box.animate.set_stroke_color(GREEN), run_time=0.4)

        self.wait(1)
        self.next_slide()

        # Clean exit
        everything = VGroup(
            section_title, summary_title,
            *flow_boxes, *flow_labels, *flow_arrows,
            final_arrow, result_box, result_text
        )

        self.play(
            LaggedStart(
                *[FadeOut(obj, shift=DOWN * 0.5) for obj in everything],
                lag_ratio=0.05
            ),
            run_time=2.5
        )
        self.wait(0.5)
        self.next_slide()





class Section4_ApproximationResults(Slide):
    def construct(self):
        # ========================================
        # PERSISTENT SECTION TITLE
        # ========================================
        section_title = Tex(
            r"\textbf{Section 4: Approximation, Results, and Conclusion}",
            font_size=44, color=BLUE
        )
        section_title.to_edge(UP, buff=0.3)

        self.play(DrawBorderThenFill(section_title), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        # ========================================
        # SLIDE 1: WHY APPROXIMATE?
        # ========================================

        subsection_title1 = Tex(
            r"\textbf{Why Approximate?}",
            font_size=36, color=GREEN
        )
        subsection_title1.next_to(section_title, DOWN, buff=0.4)

        # Problem statement
        problem = Tex(
            r"Computing $P_0 = \sum_{i=1}^{N} p_i A_i$ is expensive when $N$ is large",
            font_size=28
        )
        problem.next_to(subsection_title1, DOWN, buff=0.5)

        # Key observation box
        observation_box = Rectangle(
            width=10, height=2,
            stroke_color=YELLOW, stroke_width=3,
            fill_color=YELLOW, fill_opacity=0.15
        )
        observation_box.next_to(problem, DOWN, buff=0.6)

        observation = Tex(
            r"\textbf{Key Observation:}\\",
            r"Many BNs have very small selection probabilities $p_i$\\",
            r"$\Rightarrow$ Can be safely ignored",
            font_size=26, color=WHITE,tex_environment='minipage}{10cm}'
        )
        observation.move_to(observation_box.get_center())

        # Animation
        self.play(Write(subsection_title1), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(problem, shift=DOWN * 0.3), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        self.play(
            DrawBorderThenFill(observation_box),
            FadeIn(observation,shift=UP*1),
            run_time=1.5
        )
        self.wait(1)
        self.next_slide()

        # Clear
        slide1_elements = VGroup(
            subsection_title1, problem, observation_box, observation
        )
        self.play(FadeOut(slide1_elements))

        # ========================================
        # SLIDE 2: APPROXIMATION PROCEDURE
        # ========================================

        subsection_title2 = Tex(
            r"\textbf{Approximation Procedure}",
            font_size=36, color=GREEN
        )
        subsection_title2.next_to(section_title, DOWN, buff=0.4)

        # Original formula
        step1_title = Tex(
            r"\textbf{Step 1:} Original uncontrolled matrix",
            font_size=28, color=BLUE
        )
        step1_title.next_to(subsection_title2, DOWN, buff=0.5)

        step1_formula = MathTex(
            r"P_0 = \sum_{i=1}^{N} p_i A_i",
            font_size=36
        )
        step1_formula.next_to(step1_title, DOWN, buff=0.3)

        # Animation
        self.play(Write(subsection_title2), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(step1_title,shift=DOWN*1), run_time=1.5)
        self.play(Write(step1_formula), run_time=2)
        self.wait(0.5)
        self.next_slide()

        # Step 2: Remove small BNs
        step2_title = Tex(
            r"\textbf{Step 2:} Remove BNs with $p_i < \tau$ (threshold)",
            font_size=28, color=BLUE
        )
        step2_title.next_to(step1_formula, DOWN, buff=0.6)

        # Visual: show filtering
        threshold_line = Line(LEFT * 5, RIGHT * 5, color=RED, stroke_width=3)
        threshold_line.next_to(step2_title, DOWN, buff=1.5)
        threshold_label = MathTex(r"\tau", font_size=28, color=RED)
        threshold_label.next_to(threshold_line, LEFT, buff=0.2)

        # Probability bars
        n_bars = 8
        probs = [0.3, 0.25, 0.15, 0.12, 0.08, 0.04, 0.02, 0.01]
        bar_positions = np.linspace(-4, 4, n_bars)

        bars = VGroup(*[
            Rectangle(
                width=0.6,
                height=p * 4,
                fill_color=BLUE if p >= 0.08 else GRAY,
                fill_opacity=0.7,
                stroke_width=2,
                stroke_color=WHITE
            ).align_to(threshold_line.get_start() + DOWN * 0.5, DOWN).shift(RIGHT * pos)
            for pos, p in zip(bar_positions, probs)
        ])

        self.play(FadeIn(step2_title,shift=DOWN*1), run_time=1.5)
        self.play(
            Write(threshold_line),
            Write(threshold_label),
            run_time=1.5
        )
        self.wait(0.3)
        self.next_slide()

        self.play(
            LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.1),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        # Highlight removed bars
        removed_bars = VGroup(*[bars[i] for i in range(4, 8)])
        self.play(
            *[bar.animate.set_fill_color(RED).set_fill_opacity(0.3) for bar in removed_bars],
            run_time=1.5
        )
        self.wait(0.5)
        self.next_slide()

        # Clear
        slide2_elements = VGroup(
            subsection_title2, step1_title, step1_formula,
            step2_title, threshold_line, threshold_label, bars
        )
        self.play(FadeOut(slide2_elements))

        # ========================================
        # SLIDE 3: RENORMALIZATION
        # ========================================

        subsection_title3 = Tex(
            r"\textbf{Step 3: Renormalize}",
            font_size=36, color=GREEN
        )
        subsection_title3.next_to(section_title, DOWN, buff=0.4)

        renorm_text = Tex(
            r"Ensure columns of $\widetilde{P}_0$ still sum to 1",
            font_size=28
        )
        renorm_text.next_to(subsection_title3, DOWN, buff=0.5)

        # Result box
        result_box = Rectangle(
            width=8, height=2.5,
            stroke_color=PURPLE, stroke_width=3,
            fill_color=PURPLE, fill_opacity=0.15
        )
        result_box.next_to(renorm_text, DOWN, buff=0.6)

        result_formula = VGroup(
            MathTex(r"\widetilde{P}_0 = \text{approximated matrix}", font_size=28, color=YELLOW),
            MathTex(r"S = P_0 - \widetilde{P}_0", font_size=28),
            Tex(r"($S$ = discarded probability mass)", font_size=24, color=GRAY)
        ).arrange(DOWN, buff=0.3)
        result_formula.move_to(result_box.get_center())

        # Note
        note = Tex(
            r"\textbf{Important:} Only $P_0$ is approximated; $P_1$ (control) kept exact",
            font_size=24, color=ORANGE
        )
        note.next_to(result_box, DOWN, buff=0.4)

        # Animation
        self.play(Write(subsection_title3), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(renorm_text, shift=DOWN * 0.3), run_time=1.2)
        self.wait(0.3)
        self.next_slide()

        self.play(
            Create(result_box),
            DrawBorderThenFill(result_formula),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        self.play(FadeIn(note,shift=UP*1), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        # Clear
        slide3_elements = VGroup(
            subsection_title3, renorm_text, result_box, result_formula, note
        )
        self.play(FadeOut(slide3_elements))

        # ========================================
        # SLIDE 4: ERROR BOUNDS - SIMPLE VERSION
        # ========================================

        subsection_title4 = Tex(
            r"\textbf{Error Bounds (Proposition 1)}",
            font_size=36, color=GREEN
        )
        subsection_title4.next_to(section_title, DOWN, buff=0.4)

        # Error matrix
        error_def = MathTex(
            r"S := P_0 - \widetilde{P}_0",
            font_size=32, color=YELLOW
        )
        error_def.next_to(subsection_title4, DOWN, buff=0.5)

        # When small
        when_small = Tex(
            r"\textbf{When $\|S\|_1 \approx 0$ (small discarded mass):}",
            font_size=28, color=PURPLE
        )
        when_small.next_to(error_def, DOWN, buff=0.6)

        # Bounds box
        bounds_box = Rectangle(
            width=10, height=3,
            stroke_color=PURPLE, stroke_width=2,
            fill_color=PURPLE, fill_opacity=0.1
        )
        bounds_box.next_to(when_small, DOWN, buff=0.5)

        bounds_content = VGroup(
            Tex(r"\textbf{Terminal objective error:}", font_size=26, color=ORANGE),
            MathTex(r"\lesssim (T - k) \|S\|_1", font_size=32),
            Tex(r"\textbf{Average objective error:}", font_size=26, color=ORANGE),
            MathTex(r"\lesssim \frac{\|S\|_1}{2T}(T - k)(T + k + 1)", font_size=32)
        ).arrange(DOWN, buff=0.25)
        bounds_content.move_to(bounds_box.get_center())

        k_note = Tex(
            r"where $k$ = number of controls applied",
            font_size=22, color=GRAY
        )
        k_note.next_to(bounds_box, DOWN, buff=0.3)

        # Animation
        self.play(Write(subsection_title4), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(Write(error_def), run_time=2)
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(when_small,shift=UP*1), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(DrawBorderThenFill(bounds_box), run_time=1.5)
        self.play(
            DrawBorderThenFill(bounds_content[0]),

            run_time=2
        )
        self.play(Write(bounds_content[1],run_time=2))
        self.wait(0.3)
        self.next_slide()

        self.play(
            DrawBorderThenFill(bounds_content[2]),

            run_time=1.5
        )
        self.play(
            DrawBorderThenFill(bounds_content[3]),

            run_time=2.5
        )
        self.wait(0.3)
        self.next_slide()

        self.play(FadeIn(k_note, shift=DOWN * 0.2), run_time=1)
        self.wait(0.5)
        self.next_slide()

        # Clear
        slide4_elements = VGroup(
            subsection_title4, error_def, when_small,
            bounds_box, bounds_content, k_note
        )
        self.play(FadeOut(slide4_elements))

        # ========================================
        # SLIDE 5: KEY INSIGHT
        # ========================================

        subsection_title5 = Tex(
            r"\textbf{Key Insight}",
            font_size=36, color=GREEN
        )
        subsection_title5.next_to(section_title, DOWN, buff=0.4)

        insight_box = Rectangle(
            width=10, height=3,
            stroke_color=YELLOW, stroke_width=4,
            fill_color=YELLOW, fill_opacity=0.2
        )
        insight_box.move_to(ORIGIN)

        insight_text = Tex(
            r"\textbf{Error scales linearly with $\|S\|_1$}\\[0.5cm]",
            r"Small discarded probability mass\\",
            r"$\Downarrow$\\",
            r"Small approximation error",
            font_size=32, color=WHITE
        )
        insight_text.move_to(insight_box.get_center())

        # Animation
        self.play(Write(subsection_title5), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(
            DrawBorderThenFill(insight_box),
            FadeIn(insight_text,scale=0.7),
            run_time=2
        )



        self.wait(1)
        self.next_slide()

        # Clear
        slide5_elements = VGroup(
            subsection_title5, insight_box, insight_text
        )
        self.play(FadeOut(slide5_elements))

        # ========================================
        # SLIDE 6: EXPERIMENT SETUP
        # ========================================

        subsection_title6 = Tex(
            r"\textbf{Numerical Experiment}",
            font_size=36, color=GREEN
        )
        subsection_title6.next_to(section_title, DOWN, buff=0.4)

        setup_title = Tex(
            r"\textbf{Setup: 3-Gene Network}",
            font_size=32, color=BLUE
        )
        setup_title.next_to(subsection_title6, DOWN, buff=0.5)

        # Setup parameters in boxes
        params = VGroup(
            VGroup(
                Tex(r"Number of genes:", font_size=24),
                MathTex(r"n = 3", font_size=28, color=YELLOW)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Tex(r"Boolean networks:", font_size=24),
                MathTex(r"N = 4", font_size=28, color=YELLOW)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Tex(r"Time horizon:", font_size=24),
                MathTex(r"T = 15", font_size=28, color=YELLOW)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Tex(r"State space size:", font_size=24),
                MathTex(r"2^3 = 8 \text{ states}", font_size=28, color=YELLOW)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        params.next_to(setup_title, DOWN, buff=0.6)

        # Objective
        objective_text = Tex(
            r"\textbf{Objective:} Terminal distance $\|v(w_T) - z\|$ (1-norm)",
            font_size=26, color=ORANGE
        )
        objective_text.next_to(params, DOWN, buff=0.8)

        # Question
        question = Tex(
            r"\textbf{Question:} How does varying $K$ affect performance?",
            font_size=28, color=RED
        )
        question.next_to(objective_text, DOWN, buff=0.5)

        # Animation
        self.play(Write(subsection_title6), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(Write(setup_title), run_time=1.2)
        self.wait(0.3)
        self.next_slide()

        for param in params:
            self.play(FadeIn(param, shift=DOWN * 0.2), run_time=0.8)
            self.wait(0.2)

        self.next_slide()

        self.play(FadeIn(objective_text,shift=DOWN*0.5), run_time=1)
        self.wait(0.3)
        self.next_slide()

        self.play(DrawBorderThenFill(question), run_time=1.5)



        self.wait(0.5)
        self.next_slide()

        # Clear
        slide6_elements = VGroup(
            subsection_title6, setup_title, params, objective_text, question
        )
        self.play(FadeOut(slide6_elements))

        # ========================================
        # SLIDE 8: BAR CHART - PERFORMANCE VS K
        # ========================================

        subsection_title8 = Tex(
            r"\textbf{Performance vs. Number of Controls}",
            font_size=36, color=GREEN
        )
        subsection_title8.next_to(section_title, DOWN, buff=0.4)

        # Data from Table 2 (1-norm column) - these are RATIOS
        k_values = [1, 2, 3, 4, 5]
        objective_ratios = [0.9470, 0.8902, 0.8123, 0.7108, 0.5588]
        unconstrained_ratio = 0.3831  # This is also a ratio (baseline)

        # Create axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 1.0, 0.2],
            x_length=7,
            y_length=4,
            axis_config={"color": BLUE},
            x_axis_config={
                "numbers_to_include": [1, 2, 3, 4, 5],
                "include_numbers": True
            },
            y_axis_config={
                "numbers_to_include": [0, 0.2, 0.4, 0.6, 0.8, 1.0],
                "include_numbers": True
            },
            tips=False,
        )
        axes.next_to(subsection_title8, DOWN, buff=0.5)

        # Labels
        x_label = Tex(r"Number of Controls ($K$)", font_size=24)
        x_label.next_to(axes, DOWN, buff=0.3)

        # Correct y-axis label with the formula
        y_label = MathTex(
            r"\frac{\|\mathbf{v}(i_T, i_{T-1}, \ldots, i_1) - \mathbf{z}\|}{\|P_0^{15}\mathbf{v}_0 - \mathbf{z}\|}",
            font_size=28
        )
        y_label.rotate(90 * DEGREES)
        y_label.next_to(axes, LEFT, buff=0.5)

        # Create bars - CORRECTED positioning
        bars = VGroup()
        bar_width = 0.4

        for k, obj in zip(k_values, objective_ratios):
            # Calculate bar height in axes coordinates
            bar_height_axes = obj  # This is the y-value

            # Get the bottom and top positions in scene coordinates
            bottom_point = axes.c2p(k, 0)
            top_point = axes.c2p(k, bar_height_axes)

            # Calculate actual height in scene units
            bar_height_scene = top_point[1] - bottom_point[1]

            # Create bar
            bar = Rectangle(
                width=bar_width,
                height=bar_height_scene,
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_color=WHITE,
                stroke_width=2
            )

            # Position bar: center x at k, bottom at y=0
            bar.move_to(bottom_point, DOWN)

            # Add value label on top
            value_label = Tex(f"{obj:.4f}", font_size=18)
            value_label.next_to(bar, UP, buff=0.1)

            bars.add(VGroup(bar, value_label))

        # Add unconstrained reference line
        unconstrained_line = DashedLine(
            axes.c2p(0.01, unconstrained_ratio),
            axes.c2p(5.5, unconstrained_ratio),
            color=GREEN, stroke_width=3
        )
        unconstrained_label = Tex(
            r"Unconstrained $= 0.3831$",
            font_size=20, color=GREEN
        )
        unconstrained_label.next_to(axes.c2p(5.5, unconstrained_ratio), RIGHT, buff=0.2)

        # Animation
        self.play(Write(subsection_title8), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        self.play(DrawBorderThenFill(axes) ,run_time=1.5)
        self.play(FadeIn(VGroup(x_label, y_label),
                         shift=UP*0.5), run_time=1.5)
        self.wait(0.3)
        self.next_slide()

        # Show bars one by one
        for bar_group in bars:
            self.play(
                GrowFromEdge(bar_group[0], DOWN),
                FadeIn(bar_group[1], shift=DOWN * 0.2),
                run_time=0.8
            )
            self.wait(0.2)

        self.next_slide()

        # Add unconstrained reference
        self.play(
            Write(unconstrained_line),
            Write(unconstrained_label),
            run_time=1.5
        )
        self.wait(0.5)
        self.next_slide()

        # Add arrow showing trend
        trend_arrow = Arrow(
            bars[0][0].get_top() + UP * 0.3,
            bars[-1][0].get_top() + UP * 0.3,
            color=YELLOW, stroke_width=5, buff=0.2
        )
        trend_text = VGroup(
            Tex(r"Increasing $K$ improves", font_size=22, color=YELLOW),
            Tex(r"performance (lower ratio)", font_size=22, color=YELLOW)
        ).arrange(DOWN, buff=0.05)
        trend_text.next_to(trend_arrow, UP,buff=0.01)

        self.play(
            GrowArrow(trend_arrow),
            Write(trend_text),
            run_time=2
        )
        self.wait(1)
        self.next_slide()

        # Clear
        slide8_elements = VGroup(
            subsection_title8, axes, x_label, y_label, bars,
            unconstrained_line, unconstrained_label,
            trend_arrow, trend_text
        )
        self.play(FadeOut(slide8_elements))

        # ========================================
        # SLIDE 10: CONCLUSIONS AND FUTURE DIRECTIONS
        # ========================================

        subsection_title10 = Tex(
            r"\textbf{Conclusions and Future Directions}",
            font_size=36, color=GREEN
        )
        subsection_title10.next_to(section_title, DOWN, buff=0.4)

        # Create two-column layout
        # LEFT COLUMN: Key Contributions
        contrib_heading = Tex(
            r"\underline{Key Contributions:}",
            font_size=32, color=YELLOW
        )

        contributions = VGroup(
            Tex(r"$\bullet$ \textbf{Hard Constraints:}", font_size=24, color=WHITE),
            Tex(r"Maximum number of controls $K$", font_size=22, color=LIGHT_GRAY),
            Tex(r"$\bullet$ \textbf{Distance-Based:}", font_size=24, color=WHITE),
            Tex(r"No need to define control/terminal costs", font_size=22, color=LIGHT_GRAY),
            Tex(r"$\bullet$ \textbf{State-Independent:}", font_size=24, color=WHITE),
            Tex(r"Uses prediction, not state detection", font_size=22, color=LIGHT_GRAY),
            Tex(r"$\bullet$ \textbf{Approximation Method:}", font_size=24, color=WHITE),
            Tex(r"Efficient computation with error bounds", font_size=22, color=LIGHT_GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        left_column = VGroup(contrib_heading, contributions).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        left_column.next_to(subsection_title10, DOWN, buff=0.6)
        left_column.to_edge(LEFT, buff=1.0)

        # RIGHT COLUMN: Future Directions
        future_heading = Tex(
            r"\underline{Future Directions:}",
            font_size=32, color=YELLOW
        )

        future_points = VGroup(
            Tex(r"$\circ$ \textbf{Large-Scale Systems:}", font_size=24, color=WHITE),
            Tex(r"Efficient algorithms for high-dimensional", font_size=22, color=LIGHT_GRAY),
            Tex(r"state spaces", font_size=22, color=LIGHT_GRAY),
            Tex(r"$\circ$ \textbf{Continuous-Time:}", font_size=24, color=WHITE),
            Tex(r"Extension to continuous-time models", font_size=22, color=LIGHT_GRAY),
            Tex(r"and hybrid systems", font_size=22, color=LIGHT_GRAY),
            Tex(r"$\circ$ \textbf{Clinical Integration:}", font_size=24, color=WHITE),
            Tex(r"Real-time decision support systems", font_size=22, color=LIGHT_GRAY),
            Tex(r"with patient-specific adaptation", font_size=22, color=LIGHT_GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        right_column = VGroup(future_heading, future_points).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        right_column.next_to(subsection_title10, DOWN, buff=0.6)
        right_column.to_edge(RIGHT, buff=1.0)

        # Vertical separator line
        separator = Line(
            start=UP * 2.5,
            end=DOWN * 2.5,
            color=BLUE,
            stroke_width=2
        )
        separator.move_to(ORIGIN)

        # === ANIMATIONS ===

        # Title
        self.play(
            Write(subsection_title10),
            run_time=1.5
        )
        self.wait(0.3)
        self.next_slide()

        # Show separator
        self.play(
            Create(separator),
            run_time=1.0
        )
        self.wait(0.3)

        # Left column heading with flash
        self.play(
            Write(contrib_heading),
            Flash(contrib_heading, color=YELLOW, flash_radius=0.8),
            run_time=1.2
        )
        self.wait(0.3)
        self.next_slide()

        # Contributions appear in pairs (bullet + description)
        for i in range(0, len(contributions), 2):
            bullet = contributions[i]
            description = contributions[i + 1] if i + 1 < len(contributions) else None

            if description:
                self.play(
                    FadeIn(bullet, shift=RIGHT * 0.3),
                    FadeIn(description, shift=RIGHT * 0.3),
                    run_time=0.8
                )
            else:
                self.play(
                    FadeIn(bullet, shift=RIGHT * 0.3),
                    run_time=0.8
                )
            self.wait(0.3)

        self.next_slide()

        # Right column heading with flash
        self.play(
            Write(future_heading),
            Flash(future_heading, color=YELLOW, flash_radius=0.8),
            run_time=1.2
        )
        self.wait(0.3)
        self.next_slide()

        # Future directions appear in groups (bullet + descriptions)
        indices = [0, 3, 6]  # Start indices for each main point
        for idx in indices:
            group_items = []
            # Get bullet and its descriptions
            for j in range(3 if idx < 6 else 3):
                if idx + j < len(future_points):
                    group_items.append(future_points[idx + j])

            self.play(
                *[FadeIn(item, shift=LEFT * 0.3) for item in group_items],
                run_time=0.8
            )
            self.wait(0.3)

        self.next_slide()

        # Final emphasis - highlight both columns
        self.play(
            left_column.animate.set_color(WHITE),
            right_column.animate.set_color(WHITE),
            rate_func=there_and_back,
            run_time=1.5
        )
        self.wait(1)
        self.next_slide()

        # Clear with fade out from center
        slide10_elements = VGroup(
            subsection_title10,
            separator,
            left_column,
            right_column
        )

        self.play(
            FadeOut(slide10_elements, scale=0.9),
            run_time=2.0
        )


        # ========================================
        # FINAL SLIDE: THANK YOU
        # ========================================

        self.play(FadeOut(section_title))

        thank_you = Tex(
            r"\textbf{Thank You!}",
            font_size=80, color=BLUE
        )
        thank_you.move_to(ORIGIN)

        subtitle = Tex(
            r"Questions?",
            font_size=40, color=WHITE
        )
        subtitle.next_to(thank_you, DOWN, buff=0.8)

        self.play(
            Write(thank_you),
            run_time=2
        )
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1)
        self.wait(2)
        self.next_slide()

        self.play(FadeOut(VGroup(thank_you, subtitle)))
