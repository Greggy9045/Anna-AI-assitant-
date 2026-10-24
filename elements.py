
import tkinter as tk

def create_circle_animation(parent, background="#2c3142"):
    canvas = tk.Canvas(parent, width=310, height=310, bg=background, highlightthickness=0,)
    radius = 45
    direction = 1
    min_radius = 40
    max_radius = 50
    colours = [
        (255, 255, 255), (255, 210, 242), (255, 145, 225),
        (226, 105, 255), (178, 70, 250), (122, 48, 210),]

    def blend_colour(colour1, colour2, amount):
        r1, g1, b1 = colour1
        r2, g2, b2 = colour2
        r = int(r1 + (r2 - r1) * amount)
        g = int(g1 + (g2 - g1) * amount)
        b = int(b1 + (b2 - b1) * amount)
        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_circle(x, y, circle_radius, **kwargs):
        return canvas.create_oval(
            x - circle_radius, y - circle_radius, x + circle_radius,
            y + circle_radius, **kwargs,)

    def animate():
        nonlocal radius, direction

        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width <= 1 or height <= 1:
            canvas.after(16, animate)
            return

        radius += direction * 0.25
        if radius >= max_radius:
            radius = max_radius
            direction = -1
        elif radius <= min_radius:
            radius = min_radius
            direction = 1

        center_x = (width / 2) 
        center_y = (height / 2) - 15
        canvas.delete("all")
        glow_width = 40
        layers = 100

        for layer in range(layers):
            glow_position = layer / (layers - 1)
            colour_position = 1 - glow_position
            section = colour_position * (len(colours) - 1)
            index = min(int(section), len(colours) - 2)
            blend = section - index
            colour = blend_colour(colours[index], colours[index + 1], blend)
            glow_radius = radius + 2 + glow_width * (1 - glow_position)
            draw_circle(
                center_x, center_y, glow_radius,
                fill=colour, outline="",)

        draw_circle(
            center_x, center_y, radius,
            fill="#ffffff", outline="",)
        canvas.after(16, animate)

    canvas.after(0, animate)
    return canvas
