from PIL import Image, ImageDraw

# Параметры в миллиметрах
maze_width_mm = 2910
maze_height_mm = 2910
wall_length_mm = 168
wall_thickness_mm = 12
pillar_size_mm = 12

# Параметры изображения
pixels_per_mm = 1  # 1 мм = 1 пиксель (для простоты)

# Рассчитываем параметры изображения
maze_width_px = maze_width_mm * pixels_per_mm
maze_height_px = maze_height_mm * pixels_per_mm
wall_thickness_px = wall_thickness_mm * pixels_per_mm
pillar_size_px = pillar_size_mm * pixels_per_mm

# Создание изображения
image = Image.new("RGB", (maze_width_px, maze_height_px), "white")
draw = ImageDraw.Draw(image)

# Рисование лабиринта (например, простая сетка)
for x in range(5, maze_width_px, wall_length_mm + pillar_size_mm):
    for y in range(5, maze_height_px, wall_length_mm + pillar_size_mm):
        if y + wall_length_mm + pillar_size_px < maze_width_px:
            # Рисуем вертикальные стены
            draw.rectangle(
                [x, y+pillar_size_px, x + wall_thickness_px, y + wall_length_mm+pillar_size_px],
                fill="red"
            )
        if x + wall_length_mm+pillar_size_px < maze_width_px:
            # Рисуем горизонтальные стены
            draw.rectangle(
                [x+pillar_size_px, y, x + wall_length_mm+pillar_size_px, y + wall_thickness_px],
                fill="red"
            )
        # Рисуем углы (столбики)
        draw.rectangle(
            [x, y, x + pillar_size_px, y + pillar_size_px],
            fill="black"
        )

# Сохранение изображения
image.save("maze.png")
print("Изображение лабиринта создано и сохранено как 'maze.png'.")

