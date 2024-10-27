from manim import *
from manim.mobject.text.text_mobject import remove_invisible_chars
class ValentineCardioid(Scene):
    def construct(self):
        a = 2
        polar_plane = PolarPlane(
            size=6,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.6
            }
        ).add_coordinates()
        polar_plane.shift(LEFT * 2)

        cardioid = polar_plane.plot_polar_graph(
            lambda theta: a * (1 - np.sin(theta)),
            [0, TAU],
            color=RED
        )
        text = MathTex(r"\rho = a(1 - \sin(\theta))").scale(0.8).to_corner(UL, buff=0.5)
        svg_image = SVGMobject("assets/rose.svg")
        self.play(Write(text))
        self.add(svg_image)
        self.play(text.animate.set_color_by_gradient(RED, GREEN, BLUE), run_time=2)
        self.play(Create(polar_plane))
        self.play(Create(cardioid), run_time=3)    
        rose_path = SVGMobject("assets/rose.svg")
        rose_path.set_color(WHITE)
        rose_path.set_stroke(width=1)
        self.play(Create(rose_path.scale(3).shift(RIGHT*4)), run_time=1)
        self.wait(1)
        self.play(FadeOut(cardioid), FadeOut(polar_plane), FadeOut(text), FadeOut(rose_path), run_time=2)
        code = '''
from manim import *
from manim.mobject.text.text_mobject import remove_invisible_chars
class ValentineCardioid(Scene):
    def construct(self):
        a = 2
        polar_plane = PolarPlane(
            size=6,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.6
            }
        ).add_coordinates()
        polar_plane.shift(LEFT * 2)

        cardioid = polar_plane.plot_polar_graph(
            lambda theta: a * (1 - np.sin(theta)),
            [0, TAU],
            color=RED
        )
        text = MathTex(r"\rho = a(1 - \sin(\theta))").scale(0.8).to_corner(UL, buff=0.5)
        svg_image = SVGMobject("assets/rose.svg")
        self.play(Write(text))
        self.add(svg_image)
        self.play(text.animate.set_color_by_gradient(RED, GREEN, BLUE), run_time=2)
        self.play(Create(polar_plane))
        self.play(Create(cardioid), run_time=3)    
        rose_path = SVGMobject("assets/rose.svg")
        rose_path.set_color(WHITE)
        rose_path.set_stroke(width=1)
        self.play(Create(rose_path.scale(3).shift(LEFT*1.5)), run_time=1)
        self.wait(1)
        self.play(FadeOut(cardioid), FadeOut(polar_plane), FadeOut(text), FadeOut(rose_path), run_time=2)
'''
        textSourceCode = Text("Source Code Here").scale(0.8).to_corner(UL, buff=0.5)

        window_frame = RoundedRectangle(corner_radius=0.1, height=7, width=9, fill_color=WHITE, fill_opacity=0.9)
        window_frame.set_color(BLACK)
        
        macode = Code(
            code=code,
            language="python",
            background="window",
            tab_width=4,
            font="Monospace"
        )
        macode.code = remove_invisible_chars(macode.code)
        macode.scale(0.72)
        example_code = VGroup(
            window_frame,
            macode
        ).arrange(aligned_edge=LEFT)\
            .scale(0.72)

        example_code.center()
        
        self.play(Write(textSourceCode.to_corner(UL, buff=0.5)))
        self.play(Write(example_code.shift(LEFT * 2, DOWN * 0.5)), run_time=5, rate_func=linear)
        self.wait(3)


if __name__ == "__main__":
    from manim import config
    config.media_width = "75%"
    config.verbosity = "WARNING"
    scene = ValentineCardioid()
    scene.render()

