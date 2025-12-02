#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成应用图标
创建一个体现"file clean"概念的图标
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("需要安装Pillow库: pip install Pillow")
    exit(1)


def create_icon():
    """创建应用图标 - 文件清理主题"""
    # 创建不同尺寸的图标（Windows需要多种尺寸）
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # 创建图像（RGBA模式支持透明）
        img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 计算缩放比例
        scale = size / 256.0
        
        # 绘制背景圆形（现代蓝色渐变）
        margin = int(8 * scale)
        bg_rect = [margin, margin, size - margin, size - margin]
        # 主背景色：现代蓝色
        draw.ellipse(bg_rect, fill=(52, 152, 219, 255))
        
        # 添加内圈高光效果
        highlight_margin = int(20 * scale)
        highlight_rect = [highlight_margin, highlight_margin, 
                          size - highlight_margin, size - highlight_margin]
        draw.ellipse(highlight_rect, fill=(174, 214, 241, 100))
        
        # 绘制文件图标（白色文档）
        file_width = int(100 * scale)
        file_height = int(130 * scale)
        file_x = int(size * 0.3)  # 左侧位置
        file_y = int(size * 0.25)
        
        # 文件主体矩形
        file_rect = [file_x, file_y, file_x + file_width, file_y + file_height]
        draw.rectangle(file_rect, fill=(255, 255, 255, 255))
        
        # 文件折角（右上角）
        corner_size = int(25 * scale)
        corner_points = [
            (file_x + file_width - corner_size, file_y),
            (file_x + file_width, file_y),
            (file_x + file_width, file_y + corner_size),
            (file_x + file_width - corner_size, file_y),
        ]
        draw.polygon(corner_points, fill=(230, 230, 230, 255))
        
        # 文件内容线条（模拟文本）
        for i in range(3):
            line_y = file_y + int((i + 1) * 30 * scale)
            line_width = int(60 * scale)
            draw.rectangle(
                [file_x + int(15 * scale), line_y,
                 file_x + int(15 * scale) + line_width, line_y + int(4 * scale)],
                fill=(200, 200, 200, 255)
            )
        
        # 绘制清理/删除标记（红色X覆盖在文件上）
        x_thickness = int(10 * scale)
        x_margin = int(15 * scale)
        
        # X的第一条线（从左上到右下）
        draw.line(
            [file_x + x_margin, file_y + x_margin,
             file_x + file_width - x_margin, file_y + file_height - x_margin],
            fill=(231, 76, 60, 255), width=x_thickness
        )
        # X的第二条线（从右上到左下）
        draw.line(
            [file_x + file_width - x_margin, file_y + x_margin,
             file_x + x_margin, file_y + file_height - x_margin],
            fill=(231, 76, 60, 255), width=x_thickness
        )
        
        # 绘制第二个文件（右侧，表示清理后的状态）
        file2_x = int(size * 0.55)
        file2_y = int(size * 0.35)
        file2_width = int(80 * scale)
        file2_height = int(100 * scale)
        
        # 第二个文件（更小，表示清理后）
        file2_rect = [file2_x, file2_y, file2_x + file2_width, file2_y + file2_height]
        draw.rectangle(file2_rect, fill=(255, 255, 255, 200))  # 半透明
        
        # 第二个文件的折角
        corner2_size = int(20 * scale)
        corner2_points = [
            (file2_x + file2_width - corner2_size, file2_y),
            (file2_x + file2_width, file2_y),
            (file2_x + file2_width, file2_y + corner2_size),
            (file2_x + file2_width - corner2_size, file2_y),
        ]
        draw.polygon(corner2_points, fill=(240, 240, 240, 200))
        
        # 绘制箭头（从第一个文件指向第二个文件，表示清理过程）
        arrow_start_x = file_x + file_width + int(5 * scale)
        arrow_start_y = file_y + file_height // 2
        arrow_end_x = file2_x - int(5 * scale)
        arrow_end_y = file2_y + file2_height // 2
        
        # 箭头线
        arrow_thickness = int(6 * scale)
        draw.line(
            [arrow_start_x, arrow_start_y, arrow_end_x, arrow_end_y],
            fill=(255, 255, 255, 255), width=arrow_thickness
        )
        
        # 箭头头部
        arrow_head_size = int(12 * scale)
        arrow_points = [
            (arrow_end_x, arrow_end_y),
            (arrow_end_x - arrow_head_size, arrow_end_y - arrow_head_size // 2),
            (arrow_end_x - arrow_head_size, arrow_end_y + arrow_head_size // 2),
        ]
        draw.polygon(arrow_points, fill=(255, 255, 255, 255))
        
        images.append(img)
    
    # 保存为ICO格式（包含所有尺寸）
    images[0].save(
        'icon.ico',
        format='ICO',
        sizes=[(img.size[0], img.size[1]) for img in images]
    )
    
    # 同时保存为PNG格式（用于预览）
    images[-1].save('icon.png', format='PNG')
    
    print("图标生成成功！")
    print("- icon.ico (Windows图标，包含多种尺寸)")
    print("- icon.png (预览图，256x256)")


if __name__ == "__main__":
    create_icon()

