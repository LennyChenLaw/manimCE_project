from manim import *
import numpy as np
from scipy.fftpack import fft

# 处理几何图形
class geometric(Scene):
    # 继承的父类Scene，那Scene里面有什么方法呢？看看manim库里面的scene.py文件
    def construct(self):
        # 创建一个正方形
        square = Square(color=RED).shift(LEFT * 2)
        square.set_fill(PINK, opacity=0.5)
        # 显示动画
        # Write(square)和Create(square)的区别是什么？
        self.play(Create(square))
        # 把正方形移动到右边
        self.play(square.animate.shift(RIGHT * 4), run_time=2)
        # 缩小正方形
        self.play(square.animate.scale(0.5), run_time=2)
        # 2维平面上旋转正方形
        self.play(square.animate.rotate(PI / 4), run_time=2)
        self.play(square.animate.rotate(PI), run_time=2)
        # 透明度变化
        self.play(square.animate.set_fill(GREEN, opacity=0.5), run_time=2)
        # 控制位置
        # animate.shift和animate.move_to的区别是什么？
        self.play(square.animate.move_to(UP * 2), run_time=2)
        # 把正方形转换为圆
        circle = Circle(color=BLUE).shift(RIGHT * 2)
        circle.set_fill(BLUE, opacity=0.5)
        self.play(Transform(square, circle))
        # 淡出动画
        self.play(FadeOut(square), run_time=2)
        # 淡入动画
        self.play(FadeIn(square), run_time=2)
        # 路径动画
        self.play(MoveAlongPath(square, Circle()), run_time=2)
        path = Arc(radius=2, start_angle=PI / 2, angle=PI)
        self.play(MoveAlongPath(square, path), run_time=2)


# 创建复杂几何图形，如剑
class SwordDrawing(Scene):
    def construct(self):
        # 剑刃
        blade = Polygon(
            [-0.1, 0, 0],
            [0.1, 0, 0],
            [0.05, 2, 0],
            [-0.05, 2, 0],
            color=GRAY,
            fill_opacity=1,
        )

        # 剑柄
        hilt = Polygon(
            [-0.5, -0.2, 0],
            [0.5, -0.2, 0],
            [0.5, 0, 0],
            [-0.5, 0, 0],
            color=DARK_BROWN,
            fill_opacity=1,
        )

        # 剑柄的护手部分
        guard = Polygon(
            [-0.3, 0, 0],
            [0.3, 0, 0],
            [0.3, 0.1, 0],
            [-0.3, 0.1, 0],
            color=DARK_BROWN,
            fill_opacity=1,
        )

        # 剑柄的握把
        handle = Polygon(
            [-0.1, -0.8, 0],
            [0.1, -0.8, 0],
            [0.1, -0.2, 0],
            [-0.1, -0.2, 0],
            color=DARK_BROWN,
            fill_opacity=1,
        )

        # 将剑的各个部分组合在一起
        sword = VGroup(blade, hilt, guard, handle)
        # 将剑添加到场景中
        self.play(Create(sword))
        self.wait(2)


class DrawPianoWithFourier(Scene):
    def construct(self):

        piano_path = SVGMobject("assets/piano.svg")
        piano_path.set_color(WHITE)
        piano_path.set_stroke(width=1)
        piano_path.center()  


        points = piano_path.family_members_with_points()[0].get_points()

 
        complex_points = self.extract_complex_points(points)


        fourier_coeffs = fft(complex_points) / len(complex_points)


        num_vectors = 100
        vectors = self.get_fourier_vectors(fourier_coeffs, num_vectors)
        

        self.play(Create(piano_path))
        self.wait(1)
        self.play(FadeOut(piano_path))
        self.wait(1)
        self.animate_fourier(vectors, run_time=10)

    def extract_complex_points(self, points):

        complex_points = [complex(p[0], p[1]) for p in points]
        return np.array(complex_points)

    def get_fourier_vectors(self, coeffs, num_vectors):
        vectors = []
        for k in range(-num_vectors // 2, num_vectors // 2):
            if k != 0:
                freq = k
                coef = coeffs[k % len(coeffs)]
                vectors.append((coef, freq))
        return vectors

    def animate_fourier(self, vectors, run_time=10):
        num_vectors = len(vectors)
        paths = VGroup()
        for i in range(num_vectors):
            path = VMobject()
            path.set_points_smoothly([ORIGIN, ORIGIN])
            paths.add(path)

        self.add(paths)

        def update_paths(paths, dt):
            time = dt * run_time / TAU
            for i, (coef, freq) in enumerate(vectors):
                prev_point = paths[i].get_points()[-1]
                angle = freq * time
                new_point = prev_point + coef * np.exp(1j * angle)
                paths[i].append_vectorized_mobject(
                    Line(start=prev_point, end=new_point, stroke_width=1, color=YELLOW)
                )

        self.play(UpdateFromAlphaFunc(paths, update_paths), run_time=run_time)
        self.wait(1)

class Sincos(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(0.8)
        self.border = Rectangle(width=self.camera.frame.get_width(),
                                height=self.camera.frame.get_height())
        self.add(self.border)
        title=Title("WHY").scale(0.4).shift(DOWN)
        sub_tile=MathTex("\\cos^{2}(\\theta)","+","\\sin^{2}(\\theta)","=1").set_color_by_tex_to_color_map({"cos":PINK,"sin":GREEN}).scale(0.4).next_to(title,DOWN)
        self.play(Write(title))
        self.play(Write(sub_tile))
        circ=Circle()
        line=always_redraw(lambda:Line(ORIGIN,circ.get_end()))
        self.play(Write(line))
        self.play(Create(circ))
        dot=Dot(np.array([np.cos(PI/4),np.sin(PI/4),0])).scale(0.5)
        self.play(FadeIn(dot))
        dashed_line=DashedLine(ORIGIN,dot.get_center())
        unit_label=MathTex("1").scale(0.3).next_to(dashed_line,UP,buff=0).shift(0.1*LEFT+0.3*DOWN)
        angel=Angle(line,dashed_line,radius=0.2).set_stroke(width=2)
        label=MathTex("\\theta").next_to(angel,RIGHT,buff=0).scale(0.3).shift(0.1*UP)
        sincoslabel=MathTex("(","\\cos(\\theta)",",","\\sin(\\theta)",")")\
            .scale(0.3).next_to(dot.get_center(),RIGHT,buff=0.1)\
            .set_color_by_tex("\\cos(\\theta)",BLUE)\
            .set_color_by_tex("\\sin(\\theta)",YELLOW)
        dashed_line_v=DashedLine(RIGHT*np.cos(PI/4),UP*np.cos(PI/4)+RIGHT*np.cos(PI/4))
        # self.add(dashed_line,angel,label,sincoslabel,dashed_line_v,unit_label)
        self.play(Create(dashed_line_v))
        self.play(Create(dashed_line))
        self.play(Create(sincoslabel))
        alu=VGroup(angel,label,unit_label)
        self.play(Create(alu))
        self.play(ApplyMethod(sincoslabel[1].next_to,line,DOWN,0.1))
        self.remove(sincoslabel[2],sincoslabel[0],sincoslabel[-1])
        self.play(ApplyMethod(sincoslabel[3].next_to, dashed_line_v, RIGHT, 0.1))
        tri=VMobject(color=YELLOW).set_points_as_corners([ORIGIN,RIGHT*np.cos(PI/4),UP*np.cos(PI/4)+RIGHT*np.cos(PI/4),ORIGIN]).set_stroke(width=2)
        self.play(Create(tri))
        group=VGroup(tri,angel,label,sincoslabel[1],sincoslabel[3],unit_label)
        self.play(AnimationGroup(*[FadeOut(i) for i in [circ,dashed_line_v,dashed_line,line,dot]]))
        self.play(group.animate.scale(2).move_to(ORIGIN),run_time=2)
        tri_point=tri.get_start_anchors()
        p_point=(1-np.cos(PI/4)**2)*tri_point[0]+np.cos(PI/4)**2*tri_point[2]
        p_line=DashedLine(p_point,tri_point[1]).set_stroke(width=2)
        second=Line(tri_point[0],tri_point[2])
        p_angle=RightAngle(p_line,second,quadrant=(1,-1)).scale(0.2,about_point=p_point).set_stroke(width=2)
        # self.add(p_line,p_angle)
        self.play(Create(p_line))
        self.play(Create(p_angle))
        tri2=VMobject(color=PINK).set_points_as_corners([tri_point[0],tri_point[1],p_point,tri_point[0]])
        la_c=sincoslabel[1].copy()
        cos2=MathTex("\\cos^{2}(\\theta)",color=PINK).scale(0.4).next_to((tri_point[0]+p_point)/2,UP,0.2).shift(0.3*LEFT+0.2*DOWN)
        cos2c=cos2.copy()
        self.play(Create(tri2))
        tri2_group=VGroup(la_c,tri2,p_angle.copy(),angel.copy(),label.copy()).save_state()
        self.play(tri2_group.animate.shift(1.5*DOWN+0.5*LEFT).rotate((135*DEGREES)))
        self.play(tri2_group[0].animate.shift(0.2*DOWN+0.2*RIGHT).rotate(-135*DEGREES))
        tri2_cirner=tri2.get_start_anchors()
        tri2_label=MathTex("A","B","C").set_color_by_tex_to_color_map({"A":RED,"B":PINK,"C":GREEN}).scale(0.4)
        tri2_label[0].next_to(tri2_cirner[0],DOWN,0.1)
        tri2_label[1].next_to(tri2_cirner[1], UP, 0.1)
        tri2_label[2].next_to(tri2_cirner[2], DOWN, 0.1)
        cos2c.next_to(tri2_group,DOWN,0.1)
        soleve_eq = MathTex("\\frac{AC}{BA}", "=", "\\cos(\\theta)").scale(0.4).next_to(tri2, RIGHT, 0.3)
        # self.add(tri2_label,soleve_eq)
        self.play(Create(tri2_label))
        self.play(Create(soleve_eq))
        copy_solv=MathTex(".\\cos(\\theta)").scale(0.4).next_to(soleve_eq[-1],RIGHT,0.1)
        self.play(ApplyMethod(soleve_eq[0][3:].move_to,copy_solv),FadeOut(soleve_eq[0][2]),run_time=2)
        self.play(ApplyMethod(soleve_eq[0][3:].become, copy_solv))
        result_eq=VGroup(soleve_eq[0][3:],soleve_eq[-1])
        cos2c1=MathTex("\\cos^{2}(\\theta)").scale(0.4).move_to(result_eq,aligned_edge=LEFT)
        self.play(Transform(result_eq,cos2c1),ApplyMethod(soleve_eq[0][0:2].shift,0.1*DOWN))
        self.play(ApplyMethod(result_eq.move_to,cos2c),FadeOut(soleve_eq[0][0:2]),run_time=2)
        self.play(ApplyMethod(tri2_group.restore),ApplyMethod(cos2c.become,cos2))
        self.remove(tri2_label,soleve_eq,result_eq,soleve_eq[1])
        sin_lin = Line(tri_point[1], tri_point[2])
        sin_lin2 = Line(tri_point[2], tri_point[0])
        sin_angle = Angle(sin_lin, sin_lin2, quadrant=(-1, 1), other_angle=True)
        sin_angle_l=MathTex("90-\\theta").scale(0.25).next_to(sin_angle,DOWN,0.1).shift(0.1*LEFT)
        self.add(sin_angle,sin_angle_l)
        tri2_s = VMobject(color=GREEN).set_points_as_corners([tri_point[1], tri_point[2], p_point, tri_point[1]])
        sin2=MathTex("\\sin^{2}(\\theta)",color=GREEN).scale(0.4).next_to((tri_point[2]+p_point)/2,UP,0.2).shift(0.3*LEFT+0.2*DOWN)
        sin2c=MathTex("\\cos^{2}(90-\\theta)",color=GREEN).scale(0.4)
        sin2c1=sin2.copy()
        sin2c2 = sin2.copy()
        self.play(Create(tri2_s))
        tri2_s_group=VGroup(tri2_s,sin_angle,sin_angle_l,sincoslabel[3]).save_state()
        self.play(tri2_s_group.animate.shift(2*DOWN).rotate((135*DEGREES)))
        self.play(ApplyMethod(tri2_s_group[2].rotate,-135 * DEGREES),ApplyMethod(tri2_s_group[-1].shift(0.2*DOWN).rotate,-135 * DEGREES))
        sin2c.next_to(tri2_s_group,DOWN,0.1).shift(0.2*RIGHT)
        sin2c1.next_to(tri2_s_group, DOWN, 0.1).shift(0.2 * RIGHT)
        tri2_cirner2 = tri2_s.get_start_anchors()
        tri2_label2 = MathTex("A", "B", "C").set_color_by_tex_to_color_map({"A": RED, "B": PINK, "C": YELLOW}).scale(0.4)
        tri2_label2[0].next_to(tri2_cirner2[0], UP, 0.1)
        tri2_label2[1].next_to(tri2_cirner2[1], DOWN, 0.1)
        tri2_label2[2].next_to(tri2_cirner2[2], DOWN, 0.1).shift(0.2*RIGHT)
        # cos2c.next_to(tri2_group, DOWN, 0.1)
        self.add(tri2_label2)
        soleve_eq_s = MathTex("\\frac{BC}{AB}", "=", "\\cos(90-\\theta)").scale(0.32).next_to(tri2_s_group, LEFT, 0.1)
        self.play(Write(soleve_eq_s),ApplyMethod(tri2_s_group.shift,0.6*RIGHT),ApplyMethod(tri2_label2.shift,0.6*RIGHT))
        self.play(ApplyMethod(soleve_eq_s[0][3:].next_to,soleve_eq_s[-1],RIGHT,0.1),FadeOut(soleve_eq_s[0][2]),ApplyMethod(soleve_eq_s[0][:2].shift,0.1*DOWN))
        sin_t=always_redraw(lambda :MathTex("\\sin(\\theta)").scale(0.4).next_to(soleve_eq_s[-1],RIGHT,0.1))
        sin_tc=MathTex("\\sin(\\theta)").scale(0.4).move_to(soleve_eq_s[-1],aligned_edge=LEFT)
        self.play(Transform(soleve_eq_s[0][3:],sin_t),run_time=2)
        self.play(Transform(soleve_eq_s[-1],sin_tc),run_time=2)
        sint_group=VGroup(soleve_eq_s[0][3:],soleve_eq_s[-1])
        sin2c2.move_to(sint_group,aligned_edge=LEFT)
        self.play(Transform(sint_group,sin2c2),run_time=2)
        self.play(ApplyMethod(sint_group.move_to,sin2c.shift(0.6*RIGHT)),run_time=2)
        # self.play(Write(sin2c.shift(0.6*RIGHT)))
        self.play(ApplyMethod(tri2_s_group.restore),ApplyMethod(sint_group.become,sin2))
        # self.play(soleve_eq_s[0].animate.shift(UP),rate_func=there_and_back)
        self.remove(tri2_label2,soleve_eq_s[1],soleve_eq_s[0])
        self.play(FadeOut(soleve_eq_s[0][0:2]))
        # self.play(ApplyMethod(cos2c.shift,DOWN),ApplyMethod(cos2c.shift,DOWN))
        new_cos=cos2c.copy()
        new_s=sint_group.copy()
        # new_s=always_redraw(lambda :new.next_to(new_cos,RIGHT,0.1))
        # self.add(new_s)
        new_t_sin=MathTex("+","\\sin^{2}(\\theta)",color=GREEN)
        self.play(ApplyMethod(new_cos.shift,2*DOWN))
        new_t_sin.scale(0.4).next_to(new_cos,RIGHT,0)
        self.play(Transform(new_s,new_t_sin),run_time=2)
        # self.play(ApplyMethod(new_s.become,new_t_sin))
        equal_to1=MathTex("=1").scale(0.4).next_to(new_s,RIGHT,0.1)
        copy1=unit_label.copy()
        self.play(Transform(copy1,equal_to1),run_time=2)
        final_group=VGroup(equal_to1,new_s,new_cos)
        sourr_rect=SurroundingRectangle(final_group,color=YELLOW)
        self.play(Create(sourr_rect),rate_func=there_and_back)
        self.wait()


# 处理文字
class text(Scene):
    def construct(self):
        # 用text class渲染，it uses the Pango library
        text1 = Text("Hello World", font_size=100)
        # 修改fonts
        text2 = Text("Noto Sans", font="Noto Sans")
        # 中文、日语测试
        text3 = Text("你好，世界！こんにちは、世界！", font="Noto Sans").to_corner(DR)
        # 颜色渐变
        text4 = Text("Hello World", gradient=(BLUE, GREEN, YELLOW), font_size=100)
        # Italic
        text5 = Text("Hello World", slant=ITALIC).to_corner(UR)
        # 修改text出现在左上角
        text6 = Text("Hello World", t2c={"World": RED}).to_corner(UL)
        # 怎么控制绝对位置？如(x,y)一般的坐标
        text7 = Text("Hello World").shift(UP * 2 + LEFT * 2)
        # 用markuptext
        text8 = MarkupText(
            f'all in red <span fgcolor="{YELLOW}">except this</span>', color=RED
        )
        self.add(text3)
        self.add(text5)
        self.add(text6)

        # 一段长文字
        text9 = Text(
            "This is a very long text to show how the line spacing works."
        ).scale(0.5)
        # line spacing怎么用
        text9[0:6].set_color(RED)
        # 字的动画效果
        self.play(Write(text9))


# 处理LaTeX公式
class formular(Scene):
    def construct(self):
        # 创建一个公式
        formula = MathTex(r"\int_{-\infty}^\infty e^{-x^2} \, dx = \sqrt{\pi}")
        # 显示公式
        self.play(Create(formula))
        # 移动公式
        self.play(formula.animate.shift(UP * 2), run_time=2)
        # 缩小公式
        self.play(formula.animate.scale(0.5), run_time=2)
        self.play(formula.animate.scale(2), run_time=2)
        # 变色
        self.play(formula.animate.set_color_by_tex("pi", RED), run_time=2)
        # 透明度变化
        self.play(formula.animate.set_fill(GREEN, opacity=0.5), run_time=2)
        self.play(formula.animate.set_fill(RED, opacity=1.0), run_time=1)
        # 高亮边框
        highlight = SurroundingRectangle(formula, color=YELLOW, buff=0.2)
        # 用VGroup组合公式和高亮边框
        self.play(Create(highlight), run_time=2)
        formulaHighlightGroup = VGroup(formula, highlight)
        self.play(FadeOut(formulaHighlightGroup), run_time=2)
        # 淡入
        self.play(FadeIn(formula), run_time=2)
        # 旋转公式
        self.play(formula.animate.rotate(PI / 4), run_time=2)
        # 公式颜色渐变
        self.play(formula.animate.set_color_by_gradient(RED, GREEN, BLUE), run_time=2)
        # 路径动画
        self.play(MoveAlongPath(formula, Circle()), run_time=2)
        # 震动动画
        self.play(
            ApplyMethod(formula.shift, UP, rate_func=there_and_back, run_time=0.5)
        )
        self.play(
            ApplyMethod(formula.shift, DOWN, rate_func=there_and_back, run_time=0.5)
        )
