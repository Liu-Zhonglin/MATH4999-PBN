from random import random

from manim import *
from manim_slides.slide import Slide


class TitleAndOverview(Slide):
    def construct(self):
        # ========================================
        # SLIDE 1: TITLE PAGE (Frame 1)
        # ========================================

        # Main title with proper line breaks
        main_title = Tex(
            r"\textbf{Inferring Progressive Disconnection}\\",
            r"\textbf{in Alzheimer's Disease with}\\",
            r"\textbf{Probabilistic Boolean Networks}",
            font_size=42, color=BLUE
        ).move_to(UP * 1.8)

        # Authors with affiliations
        authors = Tex(
            r"Liu Zhonglin\textsuperscript{1} \quad Zhang Louxin\textsuperscript{2} \quad Ching Wai Ki\textsuperscript{1}",
            font_size=32, color=WHITE
        ).move_to(UP * 0.5)

        # Affiliations
        affiliation1 = Tex(
            r"\textsuperscript{1}The University of Hong Kong",
            font_size=24, color=WHITE
        ).move_to(DOWN * 0.2)

        affiliation2 = Tex(
            r"\textsuperscript{2}National University of Singapore",
            font_size=24, color=WHITE
        ).move_to(DOWN * 0.8)

        # Conference info
        conference = Tex(
            r"ICBBE 2025, November 27--30, 2025",
            font_size=28, color=GREEN
        ).move_to(DOWN * 1.6)

        location = Tex(
            r"Tokyo, Japan",
            font_size=28, color=GREEN
        ).move_to(DOWN * 2.2)

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
        self.wait(1)
        self.play(FadeIn(authors, shift=RIGHT * 2), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(affiliation1, affiliation2, shift=UP * 0.8))

        self.play(
            FadeIn(conference, shift=UP * 1),
            FadeIn(location, shift=UP * 1),
            run_time=1.5
        )
        self.wait()
        self.next_slide()

        # Clear screen for next slide
        self.play(FadeOut(VGroup(
            bg_rect, main_title, authors, affiliation1,
            affiliation2, conference, location
        )))

        # ========================================
        # SLIDE 2: OUTLINE (Frame 2)
        # ========================================

        outline_title = Tex(r"\textbf{Outline}", font_size=48, color=BLUE)
        outline_title.move_to(UP * 3.2)

        # Revised outline items
        outline_items = [
            r"1. Introduction and Motivation",
            r"2. Methods",
            r"3. Results",
            r"4. Discussion and Conclusion"
        ]

        colors = [GREEN, ORANGE, RED, PURPLE]
        text_left_edge = -4.5

        bullets, outline_texts, boxes = [], [], []

        for i, (item, color) in enumerate(zip(outline_items, colors)):
            bullet = Tex(r"$\bullet$", font_size=40, color=color)
            bullet.move_to([text_left_edge - 0.5, 1.5 - i * 1.0, 0])
            bullets.append(bullet)

            text = Tex(item, font_size=36, color=color)
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
                run_time=0.8
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




import numpy as np


class BackgroundMotivation(Slide):
    def construct(self):
        # ========================================
        # SLIDE 3: BACKGROUND (Frame 3)
        # ========================================

        # Section title
        section_title = Tex(r"\textbf{Introduction and Motivation}",
                            font_size=44, color=GREEN)
        section_title.to_edge(UP, buff=0.3)

        # Subtitle
        bg_subtitle = Tex(r"\textbf{Background}",
                          font_size=36, color=BLUE)
        bg_subtitle.next_to(section_title, DOWN, buff=0.4)

        # Points
        bg_points_data = [
            ("Alzheimer's disease (AD):",
             "neurodegenerative disorder with progressive\\\\cognitive decline."),
            ("Modern view:",
             "AD as a disconnection syndrome – breakdown\\\\of communication across brain networks."),
            ("Functional MRI (fMRI):",
             "enables in-vivo assessment of network\\\\connectivity."),
            ("Limitation:",
             "conventional connectivity is undirected;\\\\true causal influences remain unknown.")
        ]

        bg_elements = []
        start_y = 1.8
        left_margin = -6.5

        for i, (header, description) in enumerate(bg_points_data):
            bullet = Tex(r"$\bullet$", font_size=28, color=WHITE)
            bullet.move_to([left_margin, start_y - i * 1.0, 0])
            combined_text = f"\\textbf{{{header}}} {description}"
            text_block = Tex(
                f"\\begin{{flushleft}}{combined_text}\\end{{flushleft}}",
                font_size=28, color=WHITE
            )
            text_block.next_to(bullet, RIGHT, buff=0.2)
            text_block.align_to(bullet, UP)

            # Highlight headers
            if i == 0:
                text_block.set_color_by_tex("Alzheimer's disease (AD):", YELLOW)
            elif i == 1:
                text_block.set_color_by_tex("Modern view:", ORANGE)
            elif i == 2:
                text_block.set_color_by_tex("Functional MRI (fMRI):", PURPLE)
            elif i == 3:
                text_block.set_color_by_tex("Limitation:", RED)

            bg_elements.append((bullet, text_block))

        # ========================================
        # BRAIN NETWORK GRAPH (adjustable shift)
        # ========================================

        brain_shift_x = 3.5  # adjust this for graph positioning

        brain_nodes = []
        node_positions = [
            [0, 1.2, 0], [1.2, 0.8, 0], [2, 1.2, 0],
            [-0.5, 0, 0], [1, 0, 0], [2.5, 0, 0],
            [0, -1.2, 0], [1.2, -0.8, 0], [2, -1.2, 0]
        ]

        for pos in node_positions:
            node = Circle(radius=0.18, color=BLUE,
                          fill_opacity=0.7, stroke_width=2)
            node.move_to([pos[0] + brain_shift_x, pos[1], 0])
            brain_nodes.append(node)

        brain_edges = []
        edge_pairs = [
            (0, 1), (1, 2), (0, 3), (1, 4), (2, 5),
            (3, 4), (4, 5), (3, 6), (4, 7), (5, 8),
            (6, 7), (7, 8)
        ]

        for s, e in edge_pairs:
            brain_edges.append(Line(
                brain_nodes[s].get_center(),
                brain_nodes[e].get_center(),
                stroke_width=2.5, color=GREEN
            ))

        disconnection_text = Tex(
            r"\textbf{Disconnection Syndrome}",
            font_size=28, color=RED
        )
        disconnection_text.next_to(VGroup(*brain_nodes), DOWN, buff=0.5)

        # ========================================
        # ANIMATION SEQUENCE
        # ========================================

        self.play(Write(section_title), run_time=2)
        self.play(Write(bg_subtitle), run_time=1)
        self.wait(0.5)
        self.next_slide()

        # --- STEP 1: first two bullet points
        for i in range(2):  # 0: Alzheimer's, 1: Modern view
            bullet, text_block = bg_elements[i]
            self.play(
                Create(bullet),
                FadeIn(text_block, shift=RIGHT * 0.3),
                run_time=1
            )


            # After the 2nd point (Modern view), trigger brain animation
            if i == 1:
                self.next_slide()
                self.play(
                    LaggedStart(
                        *[FadeIn(node, scale=0.8) for node in brain_nodes],
                        lag_ratio=0.2
                    ),
                    run_time=1
                )
                self.play(
                    LaggedStart(
                        *[Write(edge) for edge in brain_edges],
                        lag_ratio=0.08
                    ),
                    run_time=1.2
                )
                self.play(DrawBorderThenFill(disconnection_text), run_time=1.5)
                self.play(
                    *[edge.animate.set_opacity(0.3).set_color(RED)
                      for edge in brain_edges],
                    *[node.animate.set_color(RED)
                      for node in brain_nodes],
                    run_time=1.5
                )
                self.next_slide()

        # --- STEP 2: remaining two bullet points (fMRI + limitation)
        for i in range(2, 4):  # indices for last two items
            bullet, text_block = bg_elements[i]
            self.play(
                Create(bullet),
                FadeIn(text_block, shift=RIGHT * 0.3),
                run_time=1
            )
            self.wait(0.3)

        self.next_slide()

        # Clear screen
        all_bg_elements = VGroup(
            section_title, bg_subtitle, disconnection_text,
            *[b for b, _ in bg_elements],
            *[t for _, t in bg_elements],
            *brain_nodes, *brain_edges
        )
        self.play(FadeOut(all_bg_elements))

        # ========================================
        # SLIDE 4: EXISTING APPROACHES
        # ========================================

        # Title
        approaches_title = Tex(r"\textbf{Existing Approaches and Their Limitations}",
                               font_size=42, color=GREEN)
        approaches_title.to_edge(UP, buff=0.3)

        # Subtitle
        methods_subtitle = Tex(r"\textbf{Common effective connectivity models:}",
                               font_size=32, color=BLUE)
        methods_subtitle.next_to(approaches_title, DOWN, buff=0.5)

        # Method boxes with larger dimensions
        methods = [
            ("SEM", "Structural Equation\nModeling", ORANGE),
            ("MAR", "Multivariate\nAutoregressive", PURPLE),
            ("DCM", "Dynamic Causal\nModeling", YELLOW),
            ("DBN", "Dynamic Bayesian\nNetworks", PINK)
        ]

        method_boxes = []
        method_labels = []

        box_width = 2.5
        box_height = 1.3
        total_width = 4 * box_width + 3 * 0.3
        start_x = -total_width / 2 + box_width / 2

        for i, (abbr, full_name, color) in enumerate(methods):
            box = Rectangle(width=box_width, height=box_height,
                            stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.15)
            box.move_to([start_x + i * (box_width + 0.3), 0.8, 0])

            abbr_text = Tex(f"\\textbf{{{abbr}}}", font_size=32, color=color)
            abbr_text.move_to(box.get_center() + UP * 0.25)

            full_text = Tex(full_name, font_size=18, color=WHITE)
            full_text.move_to(box.get_center() + DOWN * 0.2)

            method_boxes.append(box)
            method_labels.append(VGroup(abbr_text, full_text))

        # Limitations with CENTERED alignment and larger fonts
        limitations_title = Tex(r"\textbf{Limitations:}",
                                font_size=34, color=RED)
        limitations_title.move_to([0, -0.6, 0])

        limitations = [
            "Require long time series and large samples",
            "Assume linear or Gaussian relationships",
            "Computationally intractable for large networks"
        ]

        limitation_elements = []
        start_y_lim = -1.2

        for i, limitation in enumerate(limitations):
            # Create centered bullet + text group
            bullet_text = Tex(
                f"$\\bullet$ {limitation}",
                font_size=28, color=WHITE
            )
            bullet_text.move_to([0, start_y_lim - i * 0.6, 0])  # x=0 centers it

            # Make bullet red
            bullet_text[0][0].set_color(RED)  # First character (bullet) is red

            limitation_elements.append(bullet_text)

        # Need statement with larger font
        need_text = Tex(
            r"\textbf{Need a fast, nonlinear, interpretable framework.}",
            font_size=34, color=GREEN
        )
        need_text.move_to([0, -3.1, 0])

        # Animation sequence
        self.play(DrawBorderThenFill(approaches_title), run_time=1.5)
        self.play(FadeIn(methods_subtitle,shift=RIGHT*2), run_time=1)
        self.wait(0.5)

        for i, (box, label) in enumerate(zip(method_boxes, method_labels)):
            self.play(
                DrawBorderThenFill(box),
                FadeIn(label, shift=UP * 0.3),
                run_time=1
            )
            if i < len(method_boxes) - 1:
                self.wait(0.2)

        self.wait(0.5)

        self.play(Write(limitations_title), run_time=1)

        self.next_slide()

        # Animate centered limitations
        for limitation_element in limitation_elements:
            self.play(
                FadeIn(limitation_element, shift=DOWN * 0.3),
                run_time=0.8
            )
            self.wait(0.3)

        self.next_slide()

        # Show need statement and dim existing methods
        self.play(
            Write(need_text),
            *[box.animate.set_opacity(0.4) for box in method_boxes],
            *[label.animate.set_opacity(0.4) for label in method_labels],
            run_time=2
        )




        # Optional: Add a second circumscribe for emphasis
        self.play(
            Circumscribe(need_text, Rectangle, color=YELLOW, fade_out=True, time_width=1.2),
            run_time=2
        )
        self.wait(1)

        self.next_slide()

        # Clear screen
        all_approaches_elements = VGroup(
            approaches_title, methods_subtitle, limitations_title, need_text,
            *method_boxes, *method_labels, *limitation_elements
        )
        self.play(FadeOut(all_approaches_elements))

        # ========================================
        # SLIDE 5: COMBINED PBN INTRODUCTION AND DEMONSTRATION (FEWER NODES)
        # ========================================

        # Title with larger font
        pbn_title = Tex(r"\textbf{Probabilistic Boolean Networks (PBNs)}",
                        font_size=44, color=GREEN)
        pbn_title.to_edge(UP, buff=0.3)

        # Description with larger font
        desc_text = Tex(
            r"Extend Boolean Networks by adding probabilistic rule selection.",
            font_size=30, color=WHITE
        )
        desc_text.next_to(pbn_title, DOWN, buff=0.4)

        # Equation section with larger fonts
        equation_desc = Tex(
            r"Each node updates by one of several Boolean functions with probability $p_i^k$:",
            font_size=30, color=WHITE
        )
        equation_desc.next_to(desc_text, DOWN, buff=0.5)

        equation = MathTex(
            r"P(x_i(t + 1) = f_i^k(x(t))) = p_i^k",
            font_size=36, color=BLUE
        )
        equation.next_to(equation_desc, DOWN, buff=0.4)

        # Animation for PBN introduction
        self.play(DrawBorderThenFill(pbn_title), run_time=1.5)
        self.play(FadeIn(desc_text,equation_desc,
                         shift=UP*2.5), run_time=1.5)


        self.wait(0.5)

        self.next_slide()
        self.play(Write(equation), run_time=1.5)
        self.wait(1)

        self.next_slide()

        # ========================================
        # PBN EVOLUTION DEMONSTRATION
        # ========================================

        # Create 4 time steps with much larger nodes
        demo_subtitle = Tex(r"\textbf{State Evolution Example:}",
                            font_size=30, color=YELLOW)
        demo_subtitle.next_to(equation, DOWN, buff=0.7)

        # Only 4 nodes for better visibility
        switch_nodes = []
        node_labels = []
        time_labels = []

        node_spacing = 2.8  # Increased spacing
        num_nodes = 4  # Reduced from 6 to 4
        start_x = -(num_nodes - 1) * node_spacing / 2

        for i in range(num_nodes):
            # Much larger node circle
            node = Circle(radius=0.5, stroke_width=5, color=GRAY)
            node.move_to([start_x + i * node_spacing, -1.8, 0])

            # Much larger state label
            label = Tex("?", font_size=32, color=WHITE)
            label.move_to(node.get_center())

            # Larger time label
            time_label = MathTex(f"t_{i}", font_size=24, color=YELLOW)
            time_label.next_to(node, DOWN, buff=0.4)

            switch_nodes.append(node)
            node_labels.append(label)
            time_labels.append(time_label)

        # Much larger arrows with bigger probability labels
        arrows = []
        prob_labels = []
        function_labels = []

        for i in range(num_nodes - 1):
            # Much larger transition arrow
            arrow = CurvedArrow(
                switch_nodes[i].get_center() + RIGHT * 0.5,
                switch_nodes[i + 1].get_center() + LEFT * 0.5,
                angle=0.15, stroke_width=6, color=BLUE,tip_length=0.2
            )
            arrows.append(arrow)

            # Much larger probability labels
            prob_group = VGroup()
            prob1 = MathTex(f"p^1: {np.random.rand():.2f}", font_size=22, color=YELLOW)
            prob2 = MathTex(f"p^2: {np.random.rand():.2f}", font_size=22, color=ORANGE)
            prob1.next_to(arrow, UP, buff=0.15)
            prob2.next_to(prob1, DOWN, buff=0.08)
            prob_group.add(prob1, prob2)
            prob_labels.append(prob_group)

            # Much larger function choice indicators
            func_choice = MathTex(f"f_{{{i + 1}}}^{{?}}", font_size=24, color=GREEN)
            func_choice.next_to(arrow, DOWN, buff=0.3)
            function_labels.append(func_choice)

        # Show demo subtitle
        self.play(Write(demo_subtitle), run_time=1.5)

        # Create enhanced network visualization with larger elements
        self.play(
            LaggedStart(*[DrawBorderThenFill(node) for node in switch_nodes], lag_ratio=0.2),
            LaggedStart(*[Write(label) for label in time_labels], lag_ratio=0.2),
            run_time=2
        )

        self.play(
            LaggedStart(*[Write(arrow) for arrow in arrows], lag_ratio=0.15),
            LaggedStart(*[FadeIn(prob, shift=DOWN * 0.2) for prob in prob_labels], lag_ratio=0.15),
            LaggedStart(*[FadeIn(func,scale=0.6) for func in function_labels], lag_ratio=0.15),
            run_time=2.5
        )

        # Enhanced state evolution with much larger visual effects
        node_states = ["0", "1"]
        node_colors = [RED, GREEN]

        # Show initial random state with much larger visual
        initial_state = np.random.choice([0, 1])
        initial_color = node_colors[initial_state]
        initial_label = node_states[initial_state]

        new_text = Tex(initial_label, font_size=32, color=WHITE)
        new_text.move_to(switch_nodes[0].get_center())

        self.play(
            switch_nodes[0].animate.set_color(initial_color).set_fill(initial_color, opacity=0.5),
            Transform(node_labels[0], new_text),
            run_time=0.8
        )
        self.wait(0.3)

        # Enhanced propagation with much larger decision visualization
        for step in range(num_nodes - 1):  # Show all steps since only 3 transitions
            current_arrow = arrows[step]
            next_node = switch_nodes[step + 1]
            current_probs = prob_labels[step]
            current_func = function_labels[step]

            # Much larger highlight effects
            self.play(
                current_arrow.animate.set_color(YELLOW).set_stroke_width(8),
                current_probs.animate.scale(1.6).set_color(WHITE),
                current_func.animate.scale(1.5),
                run_time=0.5
            )

            # Much larger decision visualization
            decision_circle = Circle(radius=0.7, color=PINK, stroke_width=6)
            decision_circle.move_to(next_node.get_center())

            selected_func = np.random.choice([1, 2])
            func_indicator = MathTex(f"f^{{{selected_func}}}", font_size=26, color=PINK)
            func_indicator.next_to(decision_circle, UP, buff=0.2)

            self.play(
                Create(decision_circle),
                FadeIn(func_indicator, shift=UP * 0.3),
                next_node.animate.scale(1.3),
                run_time=0.7
            )

            # Much larger probability calculation display
            prob_calc = MathTex(f"p^{{{selected_func}}} = {np.random.rand():.2f}",
                                font_size=22, color=WHITE)
            prob_calc.next_to(decision_circle, RIGHT, buff=0.5)

            # self.play(Write(prob_calc), run_time=0.6)

            # State transition with much larger effects
            new_state = np.random.choice([0, 1])
            new_color = node_colors[new_state]
            new_label_text = node_states[new_state]

            new_text = Tex(new_label_text, font_size=32, color=WHITE)
            new_text.move_to(next_node.get_center())

            # Much larger ripple effect
            ripple = Circle(radius=0.8, color=new_color, stroke_width=4, fill_opacity=0.2)
            ripple.move_to(next_node.get_center())

            self.play(
                next_node.animate.set_color(new_color).set_fill(new_color, opacity=0.5).scale(1 / 1.3),
                Transform(node_labels[step + 1], new_text),
                Create(ripple),
                run_time=0.8
            )

            self.play(
                ripple.animate.scale(3).set_stroke_width(1).set_opacity(0.1),
                FadeOut(decision_circle),
                FadeOut(func_indicator),
                # FadeOut(prob_calc),
                run_time=0.7
            )

            self.play(FadeOut(ripple), run_time=0.3)

            # Reset highlighting
            self.play(
                current_arrow.animate.set_color(BLUE).set_stroke_width(6),
                current_probs.animate.scale(1 / 1.6).set_color(YELLOW),
                current_func.animate.scale(1 / 1.5).set_color(GREEN),
                run_time=0.4
            )

            self.wait(0.4)

        self.wait(1)

        self.next_slide()

        # Clear combined PBN slide
        pbn_combined_elements = VGroup(
            pbn_title, desc_text, equation_desc, equation, demo_subtitle,
            *switch_nodes, *node_labels, *time_labels, *arrows,
            *prob_labels, *function_labels
        )
        self.play(FadeOut(pbn_combined_elements))

        # ========================================
        # SLIDE 6: PBN ADVANTAGES — refined + fancier
        # ========================================

        # Title
        advantages_main_title = Tex(
            r"\textbf{Advantages of Probabilistic Boolean Networks}",
            font_size=46,
            color=GREEN
        )
        advantages_main_title.to_edge(UP, buff=0.8)

        # Shorter, cleaner text versions
        advantages = [
            ("Computational Efficiency:", "Fast for short fMRI data"),
            ("Nonlinear Modeling:", "Captures complex interactions"),
            ("Interpretable Results:", "Yields directed, clear links"),
            ("Scalable Framework:", "Handles large brain networks")
        ]

        advantage_elements = []
        start_y_adv = 1.3
        left_margin = -6.3

        for i, (header, body) in enumerate(advantages):
            bullet = Tex(r"$\bullet$", font_size=36, color=GREEN)
            bullet.move_to([left_margin, start_y_adv - i * 1.0, 0])

            combined = f"\\textbf{{{header}}} {body}"
            text = Tex(
                f"\\begin{{flushleft}}{combined}\\end{{flushleft}}",
                font_size=33,
                color=WHITE
            )
            text.next_to(bullet, RIGHT, buff=0.35)
            text.align_to(bullet, UP)

            # Color-code headers
            if i == 0:
                text.set_color_by_tex("Computational Efficiency:", BLUE)
            elif i == 1:
                text.set_color_by_tex("Nonlinear Modeling:", ORANGE)
            elif i == 2:
                text.set_color_by_tex("Interpretable Results:", PURPLE)
            elif i == 3:
                text.set_color_by_tex("Scalable Framework:", PINK)

            advantage_elements.append((bullet, text))

        # ======== ANIMATION SEQUENCE ========

        # Title fade-in with slight bounce
        self.play(
            FadeIn(advantages_main_title, shift=DOWN * 0.6, scale=0.9),
            run_time=1.2
        )
        self.play(advantages_main_title.animate.scale(1.03), run_time=0.5)
        self.play(advantages_main_title.animate.scale(1.0), run_time=0.5)
        self.wait(0.5)

        # Step through each advantage individually
        for i, (bullet, text) in enumerate(advantage_elements):
            self.next_slide()

            # Fancy reveal — bullet pops, text slides softly
            self.play(
                GrowFromCenter(bullet),
                FadeIn(text, shift=RIGHT * 0.3 + UP * 0.1),
                run_time=1.1,
                rate_func=smooth
            )

            # Small attention pulse
            self.play(text.animate.scale(1.05).set_color(YELLOW), run_time=0.3)
            self.play(text.animate.scale(1.0).set_color(WHITE), run_time=0.3)

        # Leave final slide pause
        self.next_slide()

        # Elegant grouped fadeout
        all_elements = VGroup(
            advantages_main_title,
            *[b for b, _ in advantage_elements],
            *[t for _, t in advantage_elements]
        )

        self.play(
            LaggedStart(
                *[FadeOut(elem, shift=UP * 0.5) for elem in all_elements],
                lag_ratio=0.07,
                run_time=2.5
            )
        )

        self.next_slide()





class DatasetMethodology(Slide):
    def construct(self):
        # ========================================
        # SECTION 3: DATASET & METHODOLOGY
        # ========================================

        # ========================================
        # SLIDE 1: DATASET AND OBJECTIVE
        # ========================================

        # Title
        dataset_title = Tex(r"\textbf{Dataset and Objective}",
                            font_size=44, color=BLUE)
        dataset_title.to_edge(UP, buff=0.3)

        # Source information with icon
        adni_logo = Circle(radius=0.5, color=GREEN, fill_opacity=0.2)
        adni_text = Tex(r"\textbf{ADNI}", font_size=20, color=GREEN)
        adni_text.move_to(adni_logo.get_center())
        adni_group = VGroup(adni_logo, adni_text)

        source_text = Tex(r"\textbf{Source:} Alzheimer's Disease Neuroimaging Initiative (ADNI)",
                          font_size=32, color=WHITE)
        source_text.next_to(dataset_title, DOWN, buff=0.8)
        adni_group.next_to(source_text, LEFT, buff=0.3)

        # Data type
        fmri_text = Tex(r"\textbf{Data:} Resting-state fMRI (``Eyes Open'')",
                        font_size=32, color=WHITE)
        fmri_text.next_to(source_text, DOWN, buff=0.5)

        # Participants with animated counters
        participants_title = Tex(r"\textbf{Participants:}",
                                 font_size=32, color=YELLOW)
        participants_title.next_to(fmri_text, DOWN, buff=0.7)

        # Create participant boxes with counters
        groups = [
            ("Normal Control (NC)", "21", GREEN),
            ("Mild Cognitive Impairment (MCI)", "28", YELLOW),
            ("Alzheimer's Disease (AD)", "10", RED)
        ]

        participant_elements = []
        start_y = participants_title.get_y() - 0.8

        for i, (group_name, count, color) in enumerate(groups):
            # Group name
            group_text = Tex(group_name, font_size=28, color=WHITE)
            group_text.move_to([-3, start_y - i * 0.6, 0])

            # Count box
            count_box = Rectangle(width=1, height=0.4,
                                  stroke_color=color, stroke_width=2,
                                  fill_color=color, fill_opacity=0.2)
            count_box.move_to([2, start_y - i * 0.6, 0])

            # Animated counter (starts at 0)
            counter = Integer(0, font_size=24, color=color)
            counter.move_to(count_box.get_center())

            # Arrow connecting
            arrow = Arrow(group_text.get_right(), count_box.get_left(),
                          stroke_width=2, color=color, buff=0.1)

            participant_elements.append((group_text, arrow, count_box, counter, int(count)))

        # Goal section
        goal_title = Tex(r"\textbf{Goal:}", font_size=32, color=ORANGE)
        goal_title.move_to([0, -2.5, 0])

        goal_text = Tex(
            r"Estimate \textbf{directed brain connectivity} with PBNs\\and test \textbf{NC--MCI--AD progression}.",
            font_size=28, color=WHITE
        )
        goal_text.next_to(goal_title, DOWN, buff=0.3)

        # Animation sequence
        self.play(Write(dataset_title), run_time=1.5)
        self.wait(0.5)

        self.play(
            DrawBorderThenFill(source_text),
            FadeIn(adni_group, scale=0.8),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(FadeIn(fmri_text,scale=0.7), run_time=1)
        self.wait(0.5)

        self.next_slide()

        self.play(Write(participants_title), run_time=1)
        self.wait(0.3)

        # Animate participants with counters
        for group_text, arrow, count_box, counter, target_count in participant_elements:
            self.play(
                FadeIn(group_text, shift=RIGHT * 0.3),
                GrowArrow(arrow),
                DrawBorderThenFill(count_box),
                FadeIn(counter),
                run_time=1
            )
            # Animate counter from 0 to target
            self.play(counter.animate.set_value(target_count), run_time=1.5)
            self.wait(0.3)

        self.wait(0.5)
        self.next_slide()

        self.play(
            Write(goal_title),
            DrawBorderThenFill(goal_text),
            run_time=2
        )
        self.wait(1)

        self.next_slide()

        # Clear screen
        all_dataset_elements = VGroup(
            dataset_title, source_text, adni_group, fmri_text,
            participants_title, goal_title, goal_text,
            *[elem for sublist in participant_elements for elem in sublist[:4]]
        )
        self.play(FadeOut(all_dataset_elements))

        # ========================================
        # SLIDE 2: REGIONS OF INTEREST (ROIs)
        # ========================================

        # Title
        roi_title = Tex(
            r"\textbf{Regions of Interest (ROIs)}",
            font_size=44, color=BLUE
        )
        roi_title.to_edge(UP, buff=0.3)

        # Subtitle
        roi_subtitle = Tex(
            r"18 ROIs from AAL3 atlas, grouped into four networks:",
            font_size=30, color=WHITE
        )
        roi_subtitle.next_to(roi_title, DOWN, buff=0.6)

        # Simplified brain outline
        brain_outline = Ellipse(width=4, height=3,
                                color=GRAY, stroke_width=2)
        brain_outline.move_to([0, 0.5, 0])

        # Network definitions
        networks = [
            ("Default Mode Network (DMN)", ["PREC", "ANG", "FMO"], RED, "bilateral"),
            ("Executive Control Network (ECN)", ["FSG", "PARS"], BLUE, "bilateral"),
            ("Salience Network (SN)", ["INS", "SMA"], GREEN, "bilateral"),
            ("Medial Temporal Lobe (MTL)", ["HIPP", "PHC"], YELLOW, "bilateral")
        ]

        # ROI dot positions
        roi_positions = [
            # DMN (red)
            [-1.5, 1.2, 0], [1.5, 1.2, 0],
            [-1.8, 0.3, 0], [1.8, 0.3, 0],
            [-1.2, 1.8, 0], [1.2, 1.8, 0],
            # ECN (blue)
            [-1.0, 0.8, 0], [1.0, 0.8, 0],
            [-1.6, 0.8, 0], [1.6, 0.8, 0],
            # SN (green)
            [-0.8, 0.2, 0], [0.8, 0.2, 0],
            [-0.5, 0.5, 0], [0.5, 0.5, 0],
            # MTL (yellow)
            [-1.2, -0.5, 0], [1.2, -0.5, 0],
            [-1.5, -0.2, 0], [1.5, -0.2, 0]
        ]

        roi_counts = [6, 4, 4, 4]  # #ROIs in each network
        roi_index = 0
        network_elements = []
        network_roi_groups = []

        # Create text and dots for each network block
        legend_start_y = 1.5
        for i, (net_name, rois, color, bilateral) in enumerate(networks):
            title_lines = {
                0: "\\textbf{Default Mode Network (DMN)}\\\\(Default)",
                1: "\\textbf{Executive Control Network (ECN)}\\\\(Executive)",
                2: "\\textbf{Salience Network (SN)}\\\\(Salience)",
                3: "\\textbf{Medial Temporal Lobe (MTL)}\\\\(Medial)"
            }
            net_title = Tex(title_lines[i], font_size=28, color=color)

            # Arrange left/right placement
            if i in [0, 3]:
                net_title.to_edge(RIGHT, buff=0.5)
            else:
                net_title.to_edge(LEFT, buff=0.5)
            net_title.move_to([net_title.get_center()[0],
                               legend_start_y - i * 1.2, 0])

            # ROI list
            roi_text = Tex(", ".join(rois) + f" ({bilateral})",
                           font_size=20, color=WHITE)
            roi_text.next_to(net_title, DOWN, buff=0.1)
            roi_text.align_to(net_title, LEFT)

            group_text = VGroup(net_title, roi_text)
            network_elements.append(group_text)

            # Create ROI dots for this network
            current_dots = []
            for j in range(roi_counts[i]):
                if roi_index < len(roi_positions):
                    dot = Dot(point=roi_positions[roi_index],
                              color=color, radius=0.1)
                    current_dots.append(dot)
                    roi_index += 1
            network_roi_groups.append(current_dots)

        # Preprocessing note
        preprocess_text = Tex(
            r"BOLD signals preprocessed and band-pass filtered (0.01--0.1 Hz)",
            font_size=25, color=LIGHT_GRAY
        )
        preprocess_text.to_edge(DOWN, buff=0.5)

        # ========================================
        # ANIMATION SEQUENCE
        # ========================================

        # Start with title + subtitle
        self.play(DrawBorderThenFill(roi_title), run_time=1.5)
        self.play(FadeIn(roi_subtitle, shift=UP * 3), run_time=1)
        self.wait(0.5)
        self.next_slide()

        # Draw brain
        self.play(Create(brain_outline), run_time=1.5)
        self.wait(0.5)

        # SHOW FOUR NETWORKS – ONE BY ONE
        for i, (net_group, dot_group) in enumerate(zip(network_elements, network_roi_groups)):
            self.next_slide()  # Wait for presenter trigger

            # Animated entrance for legend
            self.play(FadeIn(net_group, shift=LEFT * 0.4), run_time=1)

            # Fade in ROIs with breathing effect
            self.play(
                LaggedStart(
                    *[FadeIn(dot, scale=1.8) for dot in dot_group],
                    lag_ratio=0.15,
                    run_time=1.5
                )
            )

            # Gentle pulse shimmer for focus
            self.play(
                *[dot.animate.scale(1.4).set_opacity(0.8)
                  for dot in dot_group],
                run_time=0.5
            )
            self.play(
                *[dot.animate.scale(1 / 1.4).set_opacity(1)
                  for dot in dot_group],
                run_time=0.4
            )
            self.wait(0.3)

        # Wrap up slide
        self.next_slide()
        self.play(DrawBorderThenFill(preprocess_text), run_time=1.3)
        self.wait(0.8)

        self.next_slide()

        # Final fadeout
        all_content = VGroup(
            roi_title, roi_subtitle, brain_outline, preprocess_text,
            *[grp for grp in network_elements],
            *[dot for sub in network_roi_groups for dot in sub]
        )
        self.play(FadeOut(all_content, shift=UP * 0.5), run_time=2)
        self.next_slide()

        # ========================================
        # SLIDE 3: BINARIZATION VIA HMM
        # ========================================

        # Title with better spacing
        hmm_title = Tex(r"\textbf{Binarization via Hidden Markov Model (HMM)}",
                        font_size=44, color=TEAL)
        hmm_title.to_edge(UP, buff=0.4)

        # Subtitle with better contrast
        hmm_subtitle = Tex(
            r"Converting continuous BOLD signals to binary high/low activation states",
            font_size=26, color=LIGHT_GRAY
        ).next_to(hmm_title, DOWN, buff=0.4)

        # ==========================================
        # MAIN PROCESSING PIPELINE (Top Section)
        # ==========================================

        pipeline_y = 1.5
        box_width = 2.2
        box_height = 1.0

        # Input Box
        input_box = RoundedRectangle(
            width=box_width, height=box_height,
            color=GREEN, stroke_width=2, fill_opacity=0.1
        ).move_to([-4, pipeline_y, 0])

        input_text = VGroup(
            Tex(r"\textbf{fMRI}", font_size=22, color=GREEN),
            Tex(r"\textbf{BOLD}", font_size=22, color=GREEN)
        ).arrange(DOWN, buff=0.1).move_to(input_box.get_center())

        # HMM Processing Box
        hmm_box = RoundedRectangle(
            width=box_width, height=box_height,
            color=ORANGE, stroke_width=2, fill_opacity=0.1
        ).move_to([0, pipeline_y, 0])

        hmm_text = VGroup(
            Tex(r"\textbf{2-State}", font_size=20, color=ORANGE),
            Tex(r"\textbf{HMM}", font_size=22, color=ORANGE)
        ).arrange(DOWN, buff=0.1).move_to(hmm_box.get_center())

        # Output Box
        output_box = RoundedRectangle(
            width=box_width, height=box_height,
            color=RED, stroke_width=2, fill_opacity=0.1
        ).move_to([4, pipeline_y, 0])

        output_text = VGroup(
            Tex(r"\textbf{Binary}", font_size=20, color=RED),
            Tex(r"\textbf{States}", font_size=22, color=RED)
        ).arrange(DOWN, buff=0.1).move_to(output_box.get_center())

        # Pipeline Arrows
        arrow1 = Arrow(
            start=input_box.get_right(),
            end=hmm_box.get_left(),
            color=YELLOW, stroke_width=3, buff=0.1
        )
        arrow1_label = Tex("Process", font_size=25, color=YELLOW)
        arrow1_label.next_to(arrow1, UP)

        arrow2 = Arrow(
            start=hmm_box.get_right(),
            end=output_box.get_left(),
            color=YELLOW, stroke_width=3, buff=0.1
        )
        arrow2_label = Tex("Decode", font_size=25, color=YELLOW)
        arrow2_label.next_to(arrow2, UP)

        # ==========================================
        # SIGNAL TRANSFORMATION (Bottom Section)
        # ==========================================

        transform_y = -0.8

        # Signal transformation title
        transform_title = Tex(r"\textbf{Signal Transformation}", font_size=32, color=PURPLE)
        transform_title.move_to([0, transform_y + 1.2, 0])

        # Create axes for continuous signal (left)
        cont_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-2, 2, 1],
            x_length=3.5,
            y_length=2,
            tips=False,
            axis_config={"color": WHITE, "stroke_width": 2}
        ).move_to([-3.5, transform_y, 0])

        # Continuous BOLD signal
        def bold_func(x):
            return 0.8 * np.sin(2 * x) + 0.3 * np.sin(5 * x) + 0.2 * np.cos(3 * x)

        continuous_signal = cont_axes.plot(
            bold_func,
            x_range=[0, 4],
            color=BLUE,
            stroke_width=3
        )

        # Label for continuous signal
        cont_label = Tex(r"Continuous BOLD", font_size=26, color=BLUE)
        cont_label.next_to(cont_axes, DOWN, buff=0.3)

        # Create axes for binary signal (right)
        bin_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-0.5, 1.5, 0.5],
            x_length=3.5,
            y_length=2,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=False
        ).move_to([3.5, transform_y, 0])

        # Binary signal points
        x_vals = np.linspace(0, 4, 20)
        binary_vals = []

        for x in x_vals:
            signal_val = bold_func(x)
            if signal_val > 0:
                binary_vals.append(1)  # High state
            else:
                binary_vals.append(0)  # Low state

        # Create binary signal as step function
        binary_points = []
        for i, (x, y) in enumerate(zip(x_vals, binary_vals)):
            point = bin_axes.coords_to_point(x, y)
            binary_points.append(point)

        # Create step function for binary signal
        binary_lines = VGroup()
        for i in range(len(binary_points) - 1):
            # Horizontal line
            h_line = Line(
                start=binary_points[i],
                end=[binary_points[i + 1][0], binary_points[i][1], 0],
                color=RED, stroke_width=3
            )
            # Vertical line (transition)
            if binary_vals[i] != binary_vals[i + 1]:
                v_line = Line(
                    start=[binary_points[i + 1][0], binary_points[i][1], 0],
                    end=binary_points[i + 1],
                    color=RED, stroke_width=3
                )
                binary_lines.add(h_line, v_line)
            else:
                binary_lines.add(h_line)

        # Label for binary signal
        bin_label = Tex(r"Binary States", font_size=26, color=RED)
        bin_label.next_to(bin_axes, DOWN, buff=0.3)

        # Transformation arrow
        transform_arrow = Arrow(
            start=cont_axes.get_right() + [0.3, 0, 0],
            end=bin_axes.get_left() + [-0.3, 0, 0],
            color=PURPLE, stroke_width=4, buff=0.1
        )

        transform_arrow_label = Tex("HMM", font_size=26, color=PURPLE)
        transform_arrow_label.next_to(transform_arrow, UP, buff=0.1)

        # ==========================================
        # MATHEMATICAL FORMULATION
        # ==========================================

        math_formula = MathTex(
            r"\text{Emission Model: } b_j(o_t) = \mathcal{N}(o_t \mid \mu_j, \sigma_j^2)",
            font_size=26, color=WHITE
        ).move_to([0, -2.8, 0])

        process_steps = MathTex(
            r"\text{Algorithm: } \text{K-means init} \rightarrow \text{EM training} \rightarrow \text{Viterbi decode} \rightarrow \text{Merge brief states}",
            font_size=22, color=LIGHT_GRAY
        ).move_to([0, -3.3, 0])

        # ==========================================
        # ANIMATION SEQUENCE
        # ==========================================

        self.play(Write(hmm_title), run_time=2)
        self.play(DrawBorderThenFill(hmm_subtitle), run_time=1.5)
        self.wait(0.8)
        self.next_slide()

        # Show processing pipeline
        self.play(
            DrawBorderThenFill(input_box),
            Write(input_text),
            run_time=1.5
        )
        self.wait()

        self.next_slide()

        self.play(
            Write(arrow1),
            Write(arrow1_label),
            run_time=1
        )

        self.play(
            DrawBorderThenFill(hmm_box),
            Write(hmm_text),
            run_time=1.5
        )
        self.wait()
        self.next_slide()

        self.play(
            Write(arrow2),
            Write(arrow2_label),
            run_time=1
        )

        self.play(
            DrawBorderThenFill(output_box),
            Write(output_text),
            run_time=1.5
        )
        self.wait()
        self.next_slide()



        # Show signal transformation
        self.play(Write(transform_title), run_time=1.5)

        # Show continuous signal
        self.play(
            DrawBorderThenFill(cont_axes),
            Write(cont_label),
            run_time=1.5
        )
        self.play(Create(continuous_signal), run_time=2)

        # Show transformation arrow
        self.play(
            Write(transform_arrow),
            Write(transform_arrow_label),
            run_time=2
        )

        # Show binary signal
        self.play(
            DrawBorderThenFill(bin_axes),
            Write(bin_label),
            run_time=1.5
        )
        self.play(ReplacementTransform(continuous_signal.copy(),binary_lines), run_time=2)

        self.wait(1)

        self.next_slide()

        # Show mathematical formulation
        self.play(Write(math_formula), run_time=2)
        self.play(DrawBorderThenFill(process_steps), run_time=1.5)

        # Highlight the transformation
        for _ in range(2):
            self.play(
                continuous_signal.animate.set_stroke_width(5),
                run_time=0.5
            )
            self.play(
                continuous_signal.animate.set_stroke_width(3),
                binary_lines.animate.set_stroke_width(5),
                run_time=0.5
            )
            self.play(
                binary_lines.animate.set_stroke_width(3),
                run_time=0.5
            )

        self.wait(2)
        self.next_slide()

        # Clear all elements
        all_elements = VGroup(
            hmm_title, hmm_subtitle,
            input_box, input_text, hmm_box, hmm_text, output_box, output_text,
            arrow1, arrow1_label, arrow2, arrow2_label,
            transform_title, cont_axes, continuous_signal, cont_label,
            bin_axes, binary_lines, bin_label, transform_arrow, transform_arrow_label,
            math_formula, process_steps
        )
        self.play(FadeOut(all_elements))
        self.wait()



class PBNInferenceFramework(Slide):
    def construct(self):
        # Define consistent colors for this section
        title_color = BLUE
        subtitle_color = GREEN
        text_color = WHITE
        box_color = ORANGE
        arrow_color = YELLOW
        equation_color = TEAL

        network_colors = {
            "DMN": PURE_BLUE,
            "ECN": PURE_GREEN,
            "SN": ORANGE,
            "MTL": PURPLE_A,
        }

        # ========================================
        # SLIDE 1: LEARNING SUBJECT-LEVEL PBNs (REVISED LAYOUT)
        # Goal: Animate the inference pipeline exactly as in the provided image.
        # ========================================

        # Title
        learning_title = Tex(r"\textbf{Learning Subject-level PBNs}",
                             font_size=44, color=title_color)
        learning_title.to_edge(UP, buff=0.4)

        self.play(Write(learning_title), run_time=2)
        self.wait(0.5)
        self.next_slide()

        # --- Create the pipeline diagram elements based on the image ---

        # Define positions and dimensions
        top_y = 2.0
        mid_y = 0.0
        bottom_y = -2.5

        top_box_width = 4.0
        mid_box_width = 5.0
        bottom_box_width = 11.0
        box_height = 1.0

        # Top Level: Inputs
        corr_box = RoundedRectangle(width=top_box_width, height=box_height, color=box_color, corner_radius=0.2)
        corr_box.move_to([-4.5, top_y, 0])
        corr_text = Tex("Pearson Correlations", font_size=30).move_to(corr_box.get_center())
        corr_group = VGroup(corr_box, corr_text)

        genie_box = RoundedRectangle(width=top_box_width, height=box_height, color=box_color, corner_radius=0.2)
        genie_box.move_to([4.5, top_y, 0])
        genie_text = Tex("dynGENIE3", font_size=30).move_to(genie_box.get_center())
        genie_group = VGroup(genie_box, genie_text)

        # Mid Level: Hybrid Matrix
        hybrid_box = RoundedRectangle(width=mid_box_width, height=box_height, color=box_color, corner_radius=0.2)
        hybrid_box.move_to([0, mid_y, 0])
        hybrid_text = Tex(r"Combine to $\mathbf{W_{hybrid}}$", font_size=30).move_to(hybrid_box.get_center())
        hybrid_group = VGroup(hybrid_box, hybrid_text)

        # Bottom Level: Boolean Inference Steps (single wide box)
        process_box = RoundedRectangle(width=bottom_box_width, height=box_height, color=box_color, corner_radius=0.2)
        process_box.move_to([0, bottom_y, 0])
        process_text = Tex(
            r"Select Top Parents  $\rightarrow$ Evaluate with COD $\rightarrow$ "
            r" Infer Boolean Rules",
            font_size=30).move_to(process_box.get_center())
        process_group = VGroup(process_box, process_text)

        # Arrows and Labels
        arrow1 = Arrow(corr_box.get_bottom(), hybrid_box.get_top() + LEFT * 1.5, buff=0.2, color=arrow_color)
        arrow1_label = MathTex(r"\mathbf{A_{con}} \text{ (Structural)}", font_size=30, color=text_color).next_to(arrow1,
                                                                                                                 DOWN,
                                                                                                                 buff=0.1).shift(
            LEFT * 0.5)

        arrow2 = Arrow(genie_box.get_bottom(), hybrid_box.get_top() + RIGHT * 1.5, buff=0.2, color=arrow_color)
        arrow2_label = MathTex(r"\mathbf{W_{dyn}} \text{ (Data-driven)}", font_size=30, color=text_color).next_to(
            arrow2, DOWN, buff=0.1).shift(RIGHT * 0.5)

        arrow3 = Arrow(hybrid_box.get_bottom(), process_box.get_top(), buff=0.2, color=arrow_color)

        # Equations
        hybrid_eq = MathTex(
            r"\mathbf{W_{hybrid}} = \alpha \mathbf{W_{dyn,norm}} + (1-\alpha) \mathbf{A_{con}}",
            font_size=30, color=equation_color
        ).to_edge(LEFT).shift(DOWN*1.5)

        cod_eq = MathTex(
            r"\text{COD} = 1 - \frac{\sum_t (x_i(t+1) - f_i^k(x(t)))^2}{\sum_t (x_i(t+1) - \bar{x}_i)^2}",
            font_size=30, color=equation_color
        ).to_edge(RIGHT).shift(DOWN*1.5)

        # --- Animate the pipeline construction ---

        self.play(
            DrawBorderThenFill(corr_box), Write(corr_text),
            DrawBorderThenFill(genie_box), Write(genie_text),
            run_time=2
        )
        self.wait(0.5)
        self.next_slide()

        self.play(
            GrowArrow(arrow1), Write(arrow1_label),
            GrowArrow(arrow2), Write(arrow2_label),
            run_time=2
        )
        self.play(DrawBorderThenFill(hybrid_box), Write(hybrid_text), run_time=2)
        self.wait(0.5)
        self.next_slide()

        self.play(GrowArrow(arrow3), run_time=1.0)
        self.play(Write(hybrid_eq), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        self.play(Create(process_box), DrawBorderThenFill(process_text),
                  run_time=1.5)
        self.wait(0.5)

        self.play(DrawBorderThenFill(cod_eq),run_time=1.5)
        self.wait()

        self.next_slide()

        # Fade out all elements from the first slide
        all_learning_elements = VGroup(
            learning_title, corr_group, genie_group, hybrid_group, process_group,
            arrow1, arrow2, arrow3, arrow1_label, arrow2_label,
            hybrid_eq, cod_eq
        )
        self.play(FadeOut(all_learning_elements))
        self.wait(0.5)

        # ========================================
        # SLIDE 2: INFLUENCE MATRIX AND NETWORK GRAPH (REVISED MATRIX)
        # Goal: Show how the PBN translates to a weighted, directed graph.
        # ========================================

        # Title
        influence_title = Tex(r"\textbf{Influence Matrix and Network Graph}",
                              font_size=44, color=title_color)
        influence_title.to_edge(UP, buff=0.4)

        self.play(Write(influence_title), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        # --- Influence Equation and Matrix ---

        # Influence Equation
        influence_eq_desc = Tex("Quantifies connectivity of node $i$ to node $j$:", font_size=28)
        influence_eq_desc.next_to(influence_title,DOWN,buff=0.5)
        influence_eq = MathTex(
            r"I(v_j \rightarrow v_i) = \sum_{k=1}^{4} p_i^k \cdot \mathbb{I}_{f_i^k}(v_j)",
            font_size=36, color=equation_color
        ).next_to(influence_eq_desc, DOWN, buff=0.3)

        self.play(FadeIn(influence_eq_desc,shift=UP*2,run_time=1))
        self.wait(0.5)
        self.next_slide()
        self.play(DrawBorderThenFill(influence_eq),run_time=2.5)
        self.wait(1)
        self.next_slide()

        # Influence Matrix (using the requested cell-based style)
        matrix_desc = Tex("Builds a weighted, directed influence matrix (18x18):", font_size=28)
        matrix_desc.move_to(UP * 0.5)

        # Create simplified influence matrix visualization
        matrix_size = 18  # Use 18x18 as stated
        cell_size = 0.25
        matrix_group = VGroup()

        # Generate random influence values for visualization
        np.random.seed(42)  # For reproducibility
        influence_values = np.random.rand(matrix_size, matrix_size)
        influence_values = influence_values ** 2  # Skew towards lower values for realism

        for i in range(matrix_size):
            for j in range(matrix_size):
                value = influence_values[i][j]
                cell = Rectangle(
                    width=cell_size, height=cell_size,
                    stroke_color=DARK_GRAY, stroke_width=0.5,
                    fill_opacity=value,
                    fill_color=interpolate_color(BLUE, RED, value)  # Gradient from Blue (low) to Red (high)
                )
                cell.move_to([
                    (j - matrix_size / 2) * cell_size,
                    (-i + matrix_size / 2) * cell_size,
                    0
                ])
                matrix_group.add(cell)

        matrix_group.scale(0.6).move_to(DOWN * 2)

        # Matrix labels
        matrix_label_from = Tex("From (j)", font_size=20, color=WHITE).next_to(matrix_group, UP, buff=0.3)
        matrix_label_to = Tex("To (i)", font_size=20, color=WHITE).next_to(matrix_group, LEFT, buff=0.3).rotate(
            PI / 2).next_to(matrix_group, LEFT, buff=0.3)


        self.play(ReplacementTransform(influence_eq.copy(), matrix_desc))
        self.play(

            Write(VGroup(matrix_label_from, matrix_label_to,
                         matrix_group)),
            run_time=2.5
        )
        self.wait(1)

        self.next_slide()

        # --- Network Graph Visualization ---

        graph_desc = Tex("Visualized as a directed graph based on matrix:", font_size=28).move_to(UP * 2.5)
        self.play(ReplacementTransform(VGroup(matrix_desc, influence_eq,influence_eq_desc),
                                       graph_desc),
                  FadeOut(VGroup(matrix_group, matrix_label_from, matrix_label_to),
                          shift=DOWN*2))

        self.wait(0.5)
        self.next_slide()

        # Create nodes in a circular layout
        num_nodes = 18
        radius = 2.5
        nodes = VGroup()
        node_positions = []
        for i in range(num_nodes):
            angle = 2 * PI * i / num_nodes
            pos = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
            node_positions.append(pos)

        # Assign colors based on network
        # DMN: 6, ECN: 4, SN: 4, MTL: 4
        colors = ([network_colors["DMN"]] * 6 + [network_colors["ECN"]] * 4 +
                  [network_colors["SN"]] * 4 + [network_colors["MTL"]] * 4)

        for i in range(num_nodes):
            node = Dot(point=node_positions[i], color=colors[i], radius=0.12)
            nodes.add(node)

        nodes.move_to(ORIGIN + DOWN * 0.5)
        self.play(LaggedStart(*[Write(node) for node in nodes], lag_ratio=0.1))

        # Create edges
        edges = VGroup()
        # Add some random, weak connections
        for _ in range(25):
            i, j = np.random.choice(num_nodes, 2, replace=False)
            edge = Arrow(nodes[i].get_center(), nodes[j].get_center(), buff=0.15,tip_length=0.2,
                         stroke_width=1, color=GRAY)
            edges.add(edge)

        # Add the 5 significant connections from the paper (with made-up node indices for visualization)
        # DMN->MTL (3), ECN->MTL (1), MTL->ECN (1)
        significant_edges = VGroup(
            # DMN (0-5) -> MTL (14-17)
            Arrow(nodes[0].get_center(), nodes[14].get_center(), tip_length=0.3, buff=0.15, stroke_width=3, color=YELLOW),
            # PREC R -> HIPP L
            Arrow(nodes[2].get_center(), nodes[14].get_center(), buff=0.15, tip_length=0.3,stroke_width=3, color=YELLOW),
            # FMO R -> HIPP L
            Arrow(nodes[4].get_center(), nodes[14].get_center(), buff=0.15, tip_length=0.3,stroke_width=3, color=YELLOW),
            # ANG R -> HIPP L
            # MTL (14-17) -> ECN (6-9)
            Arrow(nodes[16].get_center(), nodes[7].get_center(), buff=0.15, tip_length=0.3,stroke_width=3, color=YELLOW),
            # PHC R -> PARS L
            # ECN (6-9) -> MTL (14-17)
            Arrow(nodes[7].get_center(), nodes[15].get_center(), buff=0.15, tip_length=0.3,stroke_width=3, color=YELLOW)
            # PARS L -> HIPP R
        )

        self.play(LaggedStart(*[GrowArrow(edge) for edge in edges], lag_ratio=0.05), run_time=2)
        self.wait(0.5)
        self.next_slide()
        self.play(LaggedStart(*[GrowArrow(edge) for edge in significant_edges], lag_ratio=0.2), run_time=2)

        # --- Create Legend ---
        # This section creates a legend for the network node colors.
        # The alignment is fixed by anchoring each item to a specific x-coordinate.

        # A VGroup to hold all legend elements for easy animation
        legend = VGroup()

        # Define starting position for the top of the legend
        legend_y_start = 1.5
        legend_x_pos = -6.0  # A fixed horizontal position for all dots

        # A dictionary mapping network names to their colors (ensure this is defined earlier in your code)
        network_colors = {
            "DMN": PURE_BLUE,
            "ECN": PURE_GREEN,
            "SN": ORANGE,
            "MTL": PURPLE_A,
        }

        # Loop through the network items to create each line of the legend
        for i, (name, color) in enumerate(network_colors.items()):
            # Create the colored dot for the current network
            dot = Dot(color=color, radius=0.1)

            # Position the dot. The x-coordinate is fixed, and the y-coordinate is decremented for each item.
            # This is the crucial step for vertical alignment of the dots.
            dot.move_to(np.array([legend_x_pos, legend_y_start - i * 0.6, 0]))

            # Create the text label for the network
            text = Tex(name, font_size=24)

            # Position the text to the right of the dot with a small buffer.
            # Since each dot is vertically aligned, the text will also appear left-aligned.
            text.next_to(dot, RIGHT, buff=0.2)

            # Add the dot and text for this line to the main legend VGroup
            legend.add(dot, text)

        # Animate the legend appearing on the screen
        self.play(FadeIn(legend, shift=RIGHT))

        # Highlight the significant DMN -> MTL pathway
        highlight_box = SurroundingRectangle(VGroup(nodes[0], nodes[2], nodes[4], nodes[14]), buff=0.2, color=YELLOW,
                                             stroke_width=3)
        highlight_text = Tex("Significant DMN $\\rightarrow$ MTL Decline", font_size=24, color=YELLOW).next_to(
            highlight_box, DOWN, buff=0.2)

        self.play(Create(highlight_box), Write(highlight_text))
        self.wait()

        self.next_slide()

        # Final fade out for the section
        all_influence_elements = VGroup(
            influence_title, graph_desc, nodes, edges, significant_edges, legend, highlight_box, highlight_text
        )
        self.play(
            LaggedStart(
                *[FadeOut(elem, scale=0.8) for elem in all_influence_elements],
                lag_ratio=0.1,
                run_time=2.5
            )
        )
        self.wait(0.5)


class ResultsInterpretation(Slide):
    def construct(self):
        # Define consistent colors (avoiding PURE_BLUE for better visibility)
        title_color = BLUE
        subtitle_color = GREEN
        text_color = WHITE
        significant_color = YELLOW
        decline_color = RED

        network_colors = {
            "DMN": BLUE_A,  # Changed from PURE_BLUE for better visibility
            "ECN": GREEN_A,
            "SN": ORANGE,
            "MTL": PURPLE_A,
        }

        # ========================================
        # SLIDE 1: STATISTICAL ANALYSIS
        # ========================================

        # Title
        stats_title = Tex(
            r"\textbf{Statistical Analysis}",
            font_size=44, color=title_color
        )
        stats_title.to_edge(UP, buff=0.3)

        # Analysis overview
        analysis_desc = Tex(
            r"$17\times 18=306$ directed edges compared across NC, MCI, AD groups",
            font_size=30, color=text_color
        )
        analysis_desc.next_to(stats_title, DOWN, buff=0.3)

        # Statistical method
        method_text = Tex(
            r"ANOVA or Welch ANOVA (variance-checked), then FDR correction",
            font_size=28, color=GREEN_A
        )
        method_text.next_to(analysis_desc, DOWN, buff=0.3)

        # Results table title
        results_title = Tex(
            r"\textbf{Five significant connections (q $<$ 0.05):}",
            font_size=32, color=significant_color
        )
        results_title.next_to(method_text, DOWN, buff=0.5)

        # Create results table with better formatting
        table_data = [
            ["Connection", "Pathway", "q-value"],
            [r"PREC R $\rightarrow$ HIPP L", r"DMN$\rightarrow$MTL", "0.0017"],
            [r"FMO R $\rightarrow$ HIPP L", r"DMN$\rightarrow$MTL", "0.0089"],
            [r"PHC R $\rightarrow$ PARS L", r"MTL$\rightarrow$ECN", "0.0089"],
            [r"ANG R $\rightarrow$ HIPP L", r"DMN$\rightarrow$MTL", "0.0239"],
            [r"PARS L $\rightarrow$ HIPP R", r"ECN$\rightarrow$MTL", "0.0239"]
        ]

        # Table positioning
        table_start_y = 0.5
        col_widths = [4, 2.5, 1.5]
        row_height = 0.5

        table_elements = VGroup()

        # Create table with boxes and text
        for i, row in enumerate(table_data):
            row_elements = VGroup()
            x_start = -4

            for j, (cell, width) in enumerate(zip(row, col_widths)):
                # Header row
                if i == 0:
                    cell_box = Rectangle(
                        width=width, height=row_height,
                        stroke_color=WHITE, stroke_width=2,
                        fill_color=BLUE, fill_opacity=0.3
                    )
                    cell_text = Tex(f"\\textbf{{{cell}}}", font_size=24, color=WHITE)

                else:
                    # Color code pathways
                    if j == 1:
                        if r"DMN$\rightarrow$MTL" in cell:
                            fill_color = network_colors["DMN"]
                            text_color_cell = WHITE
                        elif r"MTL$\rightarrow$ECN" in cell:
                            fill_color = network_colors["MTL"]
                            text_color_cell = WHITE
                        elif r"ECN$\rightarrow$MTL" in cell:
                            fill_color = network_colors["ECN"]
                            text_color_cell = WHITE
                        else:
                            fill_color = GRAY
                            text_color_cell = WHITE
                    else:
                        fill_color = DARK_GRAY
                        text_color_cell = WHITE

                    cell_box = Rectangle(
                        width=width, height=row_height,
                        stroke_color=WHITE, stroke_width=1,
                        fill_color=fill_color, fill_opacity=0.2
                    )

                    # Highlight significant q-values
                    if j == 2 and i > 0:
                        cell_text = Tex(f"\\textbf{{{cell}}}", font_size=22, color=significant_color)
                    else:
                        cell_text = Tex(cell, font_size=22, color=text_color_cell)

                cell_box.move_to([x_start + width / 2, table_start_y - i * row_height, 0])
                cell_text.move_to(cell_box.get_center())

                row_elements.add(cell_box, cell_text)
                x_start += width

            table_elements.add(row_elements)

        # Animation sequence
        self.play(Write(stats_title), run_time=1.5)
        self.play(FadeIn(analysis_desc, shift=UP * 2), run_time=1)
        self.play(DrawBorderThenFill(method_text), run_time=1)
        self.wait(0.5)
        self.next_slide()

        self.play(Write(results_title), run_time=2)
        self.wait(0.5)

        # ========================================
        # Simplified Table Animation (Draw Border + Fill only)
        # ========================================

        # Draw all table boxes at once with borders and fills
        self.play(
            DrawBorderThenFill(
                VGroup(*[m for group in table_elements for m in group if isinstance(m, Rectangle)])
            ),
            run_time=2
        )

        # Then write all table text labels
        self.play(
            FadeIn(
                VGroup(*[m for group in table_elements for m in group if not isinstance(m, Rectangle)]),
                shift=UP*1
            ),
            run_time=1.5
        )

        self.wait(0.5)
        self.next_slide()

        # ========================================
        # Continue normally (unchanged)
        # ========================================



        # Highlight box around all DMN→MTL connections
        dmn_mtl_rows = [1, 2, 4]  # Indices of DMN→MTL connections
        highlight_group = VGroup()
        for i in dmn_mtl_rows:
            highlight_group.add(*table_elements[i])

        highlight_box = SurroundingRectangle(
            highlight_group,
            color=network_colors["DMN"],
            stroke_width=3,
            buff=0.1
        )

        emphasis_text = Tex(
            r"\textbf{Dominant DMN$\rightarrow$MTL disconnection pattern}",
            font_size=28, color=network_colors["DMN"]
        )
        emphasis_text.next_to(table_elements, DOWN, buff=0.5)



        self.play(Create(highlight_box), run_time=1)
        self.play(DrawBorderThenFill(emphasis_text), run_time=1.5)
        self.wait()

        self.next_slide()

        # Clear screen
        all_stats_elements = VGroup(
            stats_title, analysis_desc, method_text, results_title,
            table_elements, highlight_box, emphasis_text
        )
        self.play(FadeOut(all_stats_elements))

        # ========================================
        # SLIDE 2: PROGRESSIVE LINEAR DECLINE
        # ========================================

        # Title
        decline_title = Tex(r"\textbf{Progressive Linear Decline in Connectivity}",
                            font_size=44, color=decline_color)
        decline_title.to_edge(UP, buff=0.3)

        # Subtitle
        decline_subtitle = Tex(
            r"All significant connections show consistent degradation across disease stages",
            font_size=26, color=text_color, tex_environment='minipage}{15cm}'
        )
        decline_subtitle.next_to(decline_title, DOWN, buff=0.4)

        # Create main content area divided into left (graph) and right (explanation)
        # Graph on the left side
        axes = Axes(
            x_range=[0, 2, 1],
            y_range=[-0.15, 0.05, 0.05],
            x_length=6,
            y_length=4.5,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": []},
            tips=False
        )
        axes.to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)

        # Add horizontal reference line at y=0
        ref_line = DashedLine(
            axes.c2p(0, 0), axes.c2p(2, 0),
            color=WHITE, stroke_width=2, dash_length=0.1
        )

        # Group labels
        group_labels = ["Normal", "MCI", "AD"]
        group_label_texts = VGroup()
        for i, label in enumerate(group_labels):
            label_text = Tex(f"\\textbf{{{label}}}", font_size=22, color=WHITE)
            label_text.move_to(axes.c2p(i, -0.18))
            group_label_texts.add(label_text)

        # X-axis label
        x_label = Tex(r"\textbf{Disease Stage}", font_size=18, color=WHITE)
        x_label.next_to(axes, DOWN, buff=0.3)

        # Y-axis label
        y_label = Tex(r"Cumulative Change in PBN Influence\\(from Normal Baseline)",
                      font_size=16, color=WHITE)
        y_label.rotate(PI / 2)
        y_label.next_to(axes, LEFT, buff=0.3)

        # Create decline patterns
        decline_data = {
            r"PREC R $\rightarrow$ HIPP L": ([0, -0.045, -0.135], BLUE_A),
            r"FMO R $\rightarrow$ HIPP L": ([0, 0.055, -0.065], ORANGE),
            r"PHC R $\rightarrow$ PARS L": ([0, 0.035, -0.055], GREEN)
        }

        decline_lines = VGroup()
        decline_dots = VGroup()

        for connection, (values, color) in decline_data.items():
            points = [axes.c2p(i, val) for i, val in enumerate(values)]
            line = VMobject()
            line.set_points_as_corners(points)
            line.set_stroke(color=color, width=4)
            decline_lines.add(line)

            connection_dots = VGroup()
            for i, val in enumerate(values):
                dot = Dot(point=axes.c2p(i, val), color=color, radius=0.06)
                connection_dots.add(dot)

                error_sizes = [0.015, 0.02, 0.015]
                error_size = error_sizes[i]

                error_bar = Line(
                    axes.c2p(i, val - error_size), axes.c2p(i, val + error_size),
                    color=color, stroke_width=2
                )
                connection_dots.add(error_bar)

                cap_width = 0.02
                cap_top = Line(
                    axes.c2p(i - cap_width, val + error_size),
                    axes.c2p(i + cap_width, val + error_size),
                    color=color, stroke_width=2
                )
                cap_bottom = Line(
                    axes.c2p(i - cap_width, val - error_size),
                    axes.c2p(i + cap_width, val - error_size),
                    color=color, stroke_width=2
                )
                connection_dots.add(cap_top, cap_bottom)

            decline_dots.add(connection_dots)

        # Right side explanation panel
        explanation_panel = RoundedRectangle(
            width=5.5, height=5.5,
            color=WHITE, stroke_width=2,
            fill_opacity=0.1, corner_radius=0.1
        )
        explanation_panel.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.2)

        # Panel title
        panel_title = Tex(r"\textbf{Key Findings}", font_size=28, color=decline_color)
        panel_title.next_to(explanation_panel.get_top(), DOWN, buff=0.3)

        # Connection legend with q-values
        legend_title = Tex(r"\textbf{3 Most Significant Connections}", font_size=28, color=WHITE)
        legend_title.next_to(panel_title, DOWN)

        # Individual connection entries
        connection_entries = VGroup()

        prec_entry = VGroup(
            Circle(radius=0.08, color=BLUE_A, fill_opacity=1),
            Tex(r"PREC R $\rightarrow$ HIPP L", font_size=28, color=BLUE_A),
            MathTex(r"(q = 0.0017)", font_size=28, color=WHITE)
        )
        prec_entry.arrange(RIGHT, buff=0.2)

        fmo_entry = VGroup(
            Circle(radius=0.08, color=ORANGE, fill_opacity=1),
            Tex(r"FMO R $\rightarrow$ HIPP L", font_size=28, color=ORANGE),
            MathTex(r"(q = 0.0089)", font_size=28, color=WHITE)
        )
        fmo_entry.arrange(RIGHT, buff=0.2)

        phc_entry = VGroup(
            Circle(radius=0.08, color=GREEN, fill_opacity=1),
            Tex(r"PHC R $\rightarrow$ PARS L", font_size=28, color=GREEN),
            MathTex(r"(q = 0.0089)", font_size=28, color=WHITE)
        )
        phc_entry.arrange(RIGHT, buff=0.2)

        connection_entries.add(prec_entry, fmo_entry, phc_entry)
        connection_entries.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        connection_entries.next_to(legend_title, DOWN, buff=0.4)

        # Key insights
        insights_title = Tex(r"\textbf{Insights}", font_size=28, color=significant_color)
        insights_title.next_to(connection_entries, DOWN, buff=0.3)

        # ✅ Only keep the progressive pattern insight
        insights = VGroup(
            Tex(r"$\circ$ \textbf{Progressive pattern:} All 5 connections",
                font_size=28, color=WHITE),
            Tex(r"show linear decline from Normal $\rightarrow$ MCI $\rightarrow$ AD",
                font_size=28, color=WHITE)
        )
        insights.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        insights.next_to(insights_title, DOWN, buff=0.3)

        # Animation sequence
        self.play(Write(decline_title), run_time=2)
        self.play(DrawBorderThenFill(decline_subtitle), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        self.play(
            Create(axes),
            Create(ref_line),
            Write(y_label),
            Write(x_label),
            run_time=1.5
        )
        self.play(*[Write(label) for label in group_label_texts], run_time=1)

        self.play(
            Write(panel_title),
            Write(legend_title),
            run_time=1.5
        )

        for i in range(len(decline_lines)):
            line = decline_lines[i]
            dots = decline_dots[i]
            legend_entry = connection_entries[i]

            self.play(
                Create(line),
                *[GrowFromCenter(dot) for dot in dots[::4]],
                Write(legend_entry),
                run_time=1.2
            )
            error_bars = dots[1::4] + dots[2::4] + dots[3::4]
            self.play(*[FadeIn(bar) for bar in error_bars], run_time=0.3)
            self.wait(0.3)

        self.wait(0.5)
        self.next_slide()

        # Show insights
        self.play(Write(insights_title), run_time=1.5)
        self.play(
            LaggedStart(*[Write(insight) for insight in insights], lag_ratio=0.2),
            run_time=2
        )

        self.wait()
        self.next_slide()

        # Clear slide
        all_decline_elements = VGroup(
            decline_title, decline_subtitle, axes, ref_line,
            y_label, x_label, group_label_texts, decline_lines, decline_dots,
            panel_title, legend_title, connection_entries, insights_title, insights
        )
        self.play(FadeOut(all_decline_elements))

        # ========================================
        # SLIDE 3: NETWORK-LEVEL INTERPRETATION
        # ========================================

        # Title
        network_title = Tex(r"\textbf{Network-Level Interpretation}",
                            font_size=44, color=subtitle_color)
        network_title.to_edge(UP, buff=0.3)

        # Create brain network visualization
        # Central brain schematic
        brain_outline = Ellipse(width=6, height=4, color=GRAY, stroke_width=3)
        brain_outline.move_to([-1, 0, 0])

        # Network nodes with labels
        network_positions = {
            "DMN": {
                "PREC": [-3, 1.5, 0],
                "ANG": [-3.5, 0.5, 0],
                "FMO": [-2.5, 2, 0]
            },
            "MTL": {
                "HIPP": [1, -1, 0],
                "PHC": [1.5, -0.2, 0]
            },
            "ECN": {
                "PARS": [-2, -1.5, 0],
                "FSG": [-1.5, -1, 0]
            }
        }

        # Create nodes
        all_network_nodes = VGroup()
        node_labels = VGroup()

        for network, nodes in network_positions.items():
            color = network_colors[network]
            for node_name, pos in nodes.items():
                # Node circle
                node = Circle(radius=0.3, color=color, fill_opacity=0.7, stroke_width=2)
                node.move_to(pos)
                all_network_nodes.add(node)

                # Node label
                label = Tex(node_name, font_size=16, color=WHITE)
                label.move_to(pos)
                node_labels.add(label)

        # Create declining influence arrows (the significant connections)
        significant_connections = [
            (network_positions["DMN"]["PREC"], network_positions["MTL"]["HIPP"], r"PREC$\rightarrow$HIPP"),
            (network_positions["DMN"]["FMO"], network_positions["MTL"]["HIPP"], r"FMO$\rightarrow$HIPP"),
            (network_positions["DMN"]["ANG"], network_positions["MTL"]["HIPP"], r"ANG$\rightarrow$HIPP"),
            (network_positions["MTL"]["PHC"], network_positions["ECN"]["PARS"], r"PHC$\rightarrow$PARS"),
            (network_positions["ECN"]["PARS"], network_positions["MTL"]["HIPP"], r"PARS$\rightarrow$HIPP")
        ]

        influence_arrows = VGroup()
        for start_pos, end_pos, connection_name in significant_connections:
            # Use regular Arrow
            arrow = Arrow(
                start_pos, end_pos,
                color=decline_color, stroke_width=4,
                tip_length=0.2, buff=0.3
            )
            influence_arrows.add(arrow)

        # Key findings text boxes - REVISED SECTION
        findings = [
            ("DMN Hub Vulnerability", r"High metabolic activity makes DMN hubs\\primary sites for amyloid-$\beta$ deposition",
             network_colors["DMN"]),
            ("ECN-MTL Disconnection", r"Disrupted ECN-MTL pathways contribute to\\executive and memory deficits",
             network_colors["ECN"]),
            ("Progressive Pathology Spread", r"Network dysfunction spreads from\\allocortical to association cortices", network_colors["MTL"])
        ]

        finding_elements = VGroup()
        start_y = 1.5

        for i, (title, description, color) in enumerate(findings):
            # Finding box
            finding_box = RoundedRectangle(
                width=4, height=1.2,
                color=color, stroke_width=2,
                fill_opacity=0.1, corner_radius=0.1
            )
            finding_box.to_edge(RIGHT, buff=0.3)
            finding_box.move_to([finding_box.get_center()[0], start_y - i * 1.5, 0])

            # Finding title
            title_text = Tex(f"\\textbf{{{title}}}", font_size=22, color=color)
            title_text.move_to(finding_box.get_center() + UP * 0.3)

            # Finding description
            desc_text = Tex(description, font_size=18, color=WHITE)
            desc_text.move_to(finding_box.get_center() + DOWN * 0.2)

            finding_elements.add(VGroup(finding_box, title_text, desc_text))

        # Animation sequence
        self.play(Write(network_title), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        # Show brain and networks
        self.play(Create(brain_outline), run_time=1)
        self.play(
            LaggedStart(*[FadeIn(node, scale=1.5) for node in all_network_nodes], lag_ratio=0.1),
            LaggedStart(*[Write(label) for label in node_labels], lag_ratio=0.1),
            run_time=2
        )

        # ============================================
        # Add legend for DMN, MTL, and ECN networks
        # ============================================

        legend_items = VGroup()

        # Define legend entries (label + color)
        legend_data = [
            ("DMN", network_colors["DMN"]),
            ("MTL", network_colors["MTL"]),
            ("ECN", network_colors["ECN"])
        ]

        # Build legend with colored circles and labels
        for text, color in legend_data:
            legend_circle = Circle(radius=0.2, color=color, fill_opacity=1)
            legend_label = Tex(text, font_size=30, color=WHITE)
            entry = VGroup(legend_circle, legend_label)
            entry.arrange(RIGHT, buff=0.25)
            legend_items.add(entry)

        # Arrange legend vertically and position it on the left
        legend_items.arrange(DOWN, buff=0.25, aligned_edge=LEFT)



        legend_group = VGroup( legend_items)
        legend_group.to_edge(LEFT, buff=0.5)
        legend_group.shift(UP * 0.5)

        # Use self.play to show legend
        self.play(FadeIn(legend_group, shift=RIGHT * 0.3), run_time=1.5)



        # Show declining connections
        self.play(
            LaggedStart(*[Write(arrow) for arrow in influence_arrows], lag_ratio=0.2),
            run_time=2
        )
        self.wait()

        # Show findings
        for i, finding_group in enumerate(finding_elements):
            self.next_slide()
            self.play(
                FadeIn(finding_group, shift=LEFT * 0.5),
                run_time=1.2
            )
            self.wait(0.5)

        # Highlight AD vulnerability hypothesis - REVISED TEXT
        vulnerability_text = Tex(
            r"\textbf{Validates AD as progressive disconnection syndrome}",
            font_size=28, color=significant_color, tex_environment='minipage}{20cm}'
        )
        vulnerability_text.to_edge(DOWN, buff=0.5)
        self.wait(0.5)
        self.next_slide()

        self.play(DrawBorderThenFill(vulnerability_text), run_time=2)

        self.wait(0.5)
        self.next_slide()

        # Final fadeout
        all_network_elements = VGroup(legend_group,
            network_title, brain_outline, all_network_nodes, node_labels,
            influence_arrows, finding_elements, vulnerability_text
        )

        self.play(
            LaggedStart(
                *[FadeOut(element, scale=0.8) for element in all_network_elements],
                lag_ratio=0.05,
                run_time=2
            )
        )
        self.wait(0.5)


class DiscussionConclusion(Slide):
    def construct(self):
        # Define consistent colors for this section
        title_color = BLUE
        subtitle_color = GREEN
        text_color = WHITE
        highlight_color = YELLOW
        conclusion_color = ORANGE

        # ========================================
        # SLIDE 1: ADVANTAGES OF THE PBN FRAMEWORK
        # ========================================

        # Title
        advantages_title = Tex(r"\textbf{Advantages of the PBN Framework}",
                               font_size=44, color=title_color)
        advantages_title.to_edge(UP, buff=0.4)

        # Icons created with native Manim shapes
        icons = {
            "gear": VGroup(
                RegularPolygon(n=8, stroke_width=8, color=WHITE),
                Circle(radius=0.3, stroke_width=6, color=WHITE)
            ).scale(0.4),
            "graph-down": VGroup(
                Line(UP + LEFT, DOWN + LEFT, stroke_width=8),
                Line(DOWN + LEFT, DOWN + RIGHT, stroke_width=8),
                Arrow(UP, DOWN + RIGHT * 0.5, stroke_width=8, tip_length=0.4)
            ).scale(0.4),
            "magnifying-glass": VGroup(
                Circle(radius=0.8, stroke_width=8, color=WHITE),
                Line(
                    start=np.array([0.5, -0.5, 0]),
                    end=np.array([1.2, -1.2, 0]),
                    stroke_width=10
                )
            ).scale(0.4),
            "chart-line": VGroup(
                Line(UP + LEFT, DOWN + LEFT, stroke_width=8),
                Line(DOWN + LEFT, DOWN + RIGHT, stroke_width=8),
                VMobject().set_points_as_corners([
                    LEFT * 0.8 + DOWN * 0.2,
                    LEFT * 0.2 + UP * 0.5,
                    RIGHT * 0.3 + DOWN * 0.5,
                    RIGHT * 0.8 + UP * 0.2
                ]).set_stroke(width=8)
            ).scale(0.4)
        }

        # Advantage points with icons
        advantages_data = [
            (r"\textbf{Efficiently handles}", r"nonlinear and stochastic dynamics with short fMRI series.", "gear"),
            (
            r"\textbf{Reduces complexity}", r"compared to computationally heavy models like DCM or DBN.", "graph-down"),
            (r"\textbf{Provides interpretable}", r"causal connectivity estimates (e.g., influence matrix).",
             "magnifying-glass"),
            (r"\textbf{Objectively detects}", r"progressive network degradation across disease stages.", "chart-line")
        ]

        advantage_elements = VGroup()
        start_y = 2.0
        left_margin = -5.5

        for i, (header, desc, icon_key) in enumerate(advantages_data):
            icon = icons[icon_key].copy()
            icon.set_color(highlight_color)
            icon.move_to([left_margin, start_y - i * 1.5, 0])

            text_block = Tex(
                f"\\begin{{flushleft}}{header}\\\\{desc}\\end{{flushleft}}",
                font_size=28, color=text_color, tex_environment='minipage}{10cm}'
            )
            text_block.next_to(icon, RIGHT, buff=0.4)
            text_block.align_to(icon, UP)
            text_block.set_color_by_tex(header, highlight_color)

            advantage_elements.add(VGroup(icon, text_block))

        # Animation
        self.play(Write(advantages_title), run_time=2)
        self.wait(0.5)

        for element in advantage_elements:
            self.play(
                FadeIn(element[0], scale=1.5),
                FadeIn(element[1], shift=RIGHT * 0.5),
                run_time=1.2
            )
            self.wait(0.4)

        self.wait()
        self.next_slide()

        self.play(FadeOut(VGroup(advantages_title, advantage_elements)))

        # ========================================
        # SLIDE 2: CLINICAL IMPLICATIONS
        # ========================================

        implications_title = Tex(r"\textbf{Clinical Implications}",
                                 font_size=44, color=title_color)
        implications_title.to_edge(UP, buff=0.4)

        implication_data = [
            ("Early Detection", r"Connectivity biomarkers for\\preclinical AD identification.", BLUE_A),
            ("Therapeutic Monitoring", r"Quantitative metrics to track\\disease progression and\\treatment response.",
             GREEN_A),
            ("Mechanism-driven Trials", r"Enables smaller, targeted trials\\focused on network repair.", PURPLE_A),
            ("Intervention Target", r"DMN-MTL circuit preservation\\as a potential therapeutic goal.", RED_A)
        ]

        implication_panels = VGroup()
        # --- MODIFICATION: Increased panel width for a better layout ---
        panel_width = 4.0  # Changed from 3.2 to 4.0
        panel_height = 3.5

        positions = [
            [-panel_width / 2 - 0.2, panel_height / 2, 0],
            [panel_width / 2 + 0.2, panel_height / 2, 0],
            [-panel_width / 2 - 0.2, -panel_height / 2, 0],
            [panel_width / 2 + 0.2, -panel_height / 2, 0]
        ]

        for i, (title, desc, color) in enumerate(implication_data):
            panel = RoundedRectangle(
                width=panel_width, height=panel_height,
                color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.1,
                corner_radius=0.2
            )
            panel.move_to(positions[i])

            title_text = Tex(f"\\textbf{{{title}}}", font_size=28, color=color)
            title_text.move_to(panel.get_center() + UP * 1.2)

            desc_text = Tex(desc, font_size=22, color=text_color)
            desc_text.move_to(panel.get_center() + DOWN * 0.2)

            implication_panels.add(VGroup(panel, title_text, desc_text))

        implication_panels.move_to(ORIGIN).shift(DOWN * 0.3)

        self.play(Write(implications_title), run_time=1.5)
        self.wait(0.5)
        self.next_slide()

        self.play(
            LaggedStart(
                *[DrawBorderThenFill(panel[0]) for panel in implication_panels],
                lag_ratio=0.2
            ),
            LaggedStart(
                *[FadeIn(panel[1:], shift=UP * 0.3) for panel in implication_panels],
                lag_ratio=0.2
            ),
            run_time=3
        )

        self.wait()
        self.next_slide()

        self.play(FadeOut(VGroup(implications_title, implication_panels)))

        # =======================================================
        # SLIDE 3 (FANCIER): CONCLUSION & FUTURE DIRECTIONS
        # =======================================================

        # Main title for the slide
        main_title = Tex(r"\textbf{Conclusion \& Future Directions}", font_size=44, color=title_color)
        main_title.to_edge(UP, buff=0.4)

        # --- Create two panels for a side-by-side layout ---

        # Panel 1: Conclusion
        conclusion_panel = RoundedRectangle(
            width=6, height=4.5, corner_radius=0.2,
            color=conclusion_color, stroke_width=3,
            fill_color=conclusion_color, fill_opacity=0.15
        )
        conclusion_title = Tex(r"\textbf{Conclusion}", font_size=34, color=conclusion_color)
        conclusion_points = VGroup(
            Tex(r"$\bullet$ First \textbf{PBN-based approach} for AD.", font_size=26),
            Tex(r"$\bullet$ Identified \textbf{DMN$\rightarrow$MTL} degradation.", font_size=26),
            Tex(r"$\bullet$ Quantified \textbf{progressive disconnection}.", font_size=26)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)

        # Arrange elements within the conclusion panel
        conclusion_group = VGroup(conclusion_title, conclusion_points).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        conclusion_group.move_to(conclusion_panel).shift(LEFT * 0.2)
        conclusion_title.align_to(conclusion_points, LEFT)
        VGroup(conclusion_panel, conclusion_group).to_edge(LEFT, buff=0.5)

        # Panel 2: Future Directions
        future_panel = RoundedRectangle(
            width=6, height=4.5, corner_radius=0.2,
            color=subtitle_color, stroke_width=3,
            fill_color=subtitle_color, fill_opacity=0.15
        )
        future_title = Tex(r"\textbf{Future Directions}", font_size=34, color=subtitle_color)
        future_points = VGroup(
            Tex(r"$\circ$ Integrate \textbf{hybrid models}.", font_size=26),
            Tex(r"$\circ$ Validate on \textbf{multimodal data}.", font_size=26)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)

        # Arrange elements within the future panel
        future_group = VGroup(future_title, future_points).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        future_group.move_to(future_panel).shift(LEFT * 0.2)
        future_title.align_to(future_points, LEFT)
        VGroup(future_panel, future_group).to_edge(RIGHT, buff=0.5)

        # Align panels vertically
        panels = VGroup(conclusion_panel, future_panel).center().shift(DOWN * 0.2)
        conclusion_group.move_to(conclusion_panel)
        future_group.move_to(future_panel)

        # --- Animation Sequence ---
        self.play(Write(main_title), run_time=2)
        self.wait(0.5)
        self.next_slide()

        # Animate panels drawing, then titles, then points
        self.play(
            DrawBorderThenFill(conclusion_panel),
            Write(conclusion_title),
            run_time=2
        )

        self.wait(0.2)
        self.play(
            LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in conclusion_points],
                        lag_ratio=0.5),
            run_time=2
        )

        self.wait()
        self.next_slide()

        # Animate panels drawing, then titles, then points
        self.play(
            DrawBorderThenFill(future_panel),
            Write(future_title),
            run_time=2
        )

        self.wait(0.2)
        self.play(
            LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in future_points], lag_ratio=0.5),
            run_time=2
        )
        self.wait()
        self.next_slide()

        # Clear screen for the final slide
        self.play(FadeOut(VGroup(main_title, conclusion_panel, future_panel,
                                 conclusion_group, future_group)))

        # =======================================================
        # SLIDE 4 (FANCIER): ACKNOWLEDGMENTS & Q&A
        # =======================================================

        # --- Create Acknowledgments section ---
        ack_title = Tex(r"\textbf{Acknowledgments}", font_size=44, color=title_color)
        ack_underline = Underline(ack_title, color=title_color)

        ack_items = VGroup(
            Tex(r"Undergraduate Research Fellowship Programme (URFP), HKU", font_size=28),
            Tex(r"Collaboration with National University of Singapore", font_size=28),
            Tex(r"HKU Information Technology Services", font_size=28),
            Tex(r"With heartfelt gratitude to Prof.\ Zhang and Prof.\ Ching \\"
                r"for their invaluable mentorship",
                font_size=28)
        ).arrange(DOWN, buff=0.5)

        ack_group = VGroup(ack_title, ack_underline, ack_items).arrange(DOWN, buff=0.6).center()

        # --- Create Final "Thank You" section (initially invisible) ---
        thank_you_text = Tex(r"\textbf{Thank You}", font_size=80, color=highlight_color)
        questions_text = Tex(r"\textbf{Questions?}", font_size=52, color=text_color)
        final_group = VGroup(thank_you_text, questions_text).arrange(DOWN, buff=1.0).center()

        # --- Animation Sequence ---
        self.play(
            Write(ack_title),
            Create(ack_underline),
            run_time=1.5
        )
        self.play(
            LaggedStart(*[FadeIn(item, shift=RIGHT) for item in ack_items], lag_ratio=0.4),
            run_time=3
        )
        self.wait()
        self.next_slide()

        # --- Smoother Transition ---
        # Animate acknowledgments moving up and fading out, while the final text appears
        self.play(
            ack_group.animate.shift(UP * 2).fade(1),
            run_time=1.5
        )
        self.play(
            Write(thank_you_text),
            run_time=2
        )
        self.play(
            FadeIn(questions_text, shift=UP * 0.5),
            run_time=1
        )
        self.wait(3)




