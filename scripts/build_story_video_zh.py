"""Render a narrated, animated Chinese marine-heatwave explainer from site assets."""
from __future__ import annotations

import asyncio
import math
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT.parents[1] / "output" / "story-zh-build"
BUILD.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(BUILD / "pydeps"))
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

FFMPEG = Path("E:/FormatFactory/ffmpeg.exe")
W, H, FPS = 1280, 720, 12
FONT = "C:/Windows/Fonts/msyh.ttc"
TITLES = ["一个课堂疑问", "怎样识别海洋热浪", "四个指标，四种含义", "为什么峰值错开", "查看全南海数据", "下一步检验机制"]
NARRATION = [
    "课堂上一张南海北部的季节图让我困惑。五月开始的海洋热浪事件最多，六月的平均热浪天数却最多，四月的平均强度最高。我原以为三个峰值应该一致，为什么会错开？",
    "我先核对定义。海表温度连续至少五天超过随季节变化的阈值，才算一次海洋热浪。单独一天特别热，并不足以构成一次事件。图中的曲线只是识别规则的示意，并非实测数据。",
    "然后我重新读四幅图的纵轴。开始次数统计新事件，持续时间是单次事件的长度，热浪天数累计事件内的日数，强度衡量超过阈值的温度幅度。它们的统计对象和单位都不同。",
    "一次事件可以在五月末开始，跨过月份边界并持续到六月。所以五月可以有更多事件开始，而六月累计更多热浪天数。事件少但持续更久，也能产生同样现象。这是指标解释，还不是物理成因。",
    "我进一步查看了一九九六到二零二五年全南海的 NOAA 海表温度分析。不同海区的热浪天数和事件持续时间并不一致，区域平均值可能掩盖空间差异。课堂季节图没有标出基准期，因此我不据此推算长期趋势。",
    "下一步，我想结合海气热通量、混合层深度、风、海流和垂向混合，检验季风转换期间哪个过程影响了海表增暖。我的结论是：先分清指标，再用独立数据检验机制；一张季节图本身不能证明成因。",
]


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT, size, index=1 if bold else 0)


def put(draw, xy, value, size=34, fill="#f4faf9", bold=False):
    draw.text(xy, value, font=font(size, bold), fill=fill)


def base(scene: int, p: float) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (W, H), "#082d42")
    d = ImageDraw.Draw(image)
    for y in range(H):
        t = y / H
        d.line((0, y, W, y), fill=(round(7+9*t), round(39+42*t), round(61+38*t)))
    for j in range(4):
        wave = [(x, int(560+j*40+10*math.sin(x/90+j+p*2))) for x in range(0, W+10, 10)]
        d.line(wave, fill="#17677b", width=2)
    put(d, (56, 35), "海洋课堂笔记  ·  南海海洋热浪故事会", 22, "#79ddc9", True)
    put(d, (55, 91), TITLES[scene], 47, bold=True)
    d.rounded_rectangle((55, 165, 1225, 635), 20, fill="#eef7f3")
    d.rectangle((0, 695, round(W*(scene+p)/6), 720), fill="#70d9c5")
    put(d, (57, 657), f"0{scene+1} / 06   动画示意与课堂数据请区分", 18, "#cce6e4")
    return image, d


def scene_frame(scene: int, p: float, chart: Image.Image, spatial: Image.Image) -> Image.Image:
    image, d = base(scene, p)
    dark, teal, red, gold = "#17435a", "#14837e", "#df7149", "#c78624"
    if scene == 0:
        labels = [("开始次数", "五月", 480, red), ("热浪天数", "六月", 405, teal), ("平均强度", "四月", 345, gold)]
        for k, (name, month, height, color) in enumerate(labels):
            x = 160+k*350
            d.rounded_rectangle((x, 235, x+240, 550), 14, fill="#d9e9e7")
            h = int((height-285)*min(1, max(0, p*2-k*.25)))
            d.rounded_rectangle((x+26, 530-h, x+214, 530), 9, fill=color)
            put(d, (x+42, 256), name, 27, dark, True)
            put(d, (x+82, 558), month, 29, dark, True)
    elif scene == 1:
        d.line((130, 520, 1125, 520), fill=dark, width=3)
        d.line((130, 260, 130, 520), fill=dark, width=3)
        pts = [(130+i*20, int(393-21*math.sin(i*.17))) for i in range(50)]
        temp = [(x, y+45-(90 if 19 < k < 32 else 0)) for k, (x, y) in enumerate(pts)]
        d.line(pts, fill=gold, width=5)
        n = max(2, int(len(temp)*p))
        d.line(temp[:n], fill=teal, width=7)
        for x, y in temp[20:min(n,32)]: d.ellipse((x-5,y-5,x+5,y+5), fill=red)
        put(d, (175, 212), "连续 ≥ 5 天超过季节阈值", 33, dark, True)
        put(d, (810, 420), "季节阈值", 24, gold)
        put(d, (160, 540), "示意曲线 · 非实测", 22, dark)
    elif scene == 2:
        chart_thumb = chart.copy(); chart_thumb.thumbnail((1050, 395))
        image.paste(chart_thumb, (round(640-chart_thumb.width/2), 198))
        d = ImageDraw.Draw(image)
        x = 75+int(1020*p)
        d.rounded_rectangle((x, 580, min(x+125, 1210), 613), 7, fill=red)
        put(d, (100, 587), "看清单位：次数  ≠  天数  ≠  摄氏度", 22, dark, True)
    elif scene == 3:
        d.line((135, 420, 1145, 420), fill=dark, width=8)
        d.line((650, 273, 650, 530), fill=gold, width=5)
        put(d, (255, 270), "五月", 42, dark, True)
        put(d, (864, 270), "六月", 42, dark, True)
        d.rounded_rectangle((490, 385, 885, 455), 22, fill=red)
        x = 490+int(395*p)
        d.ellipse((x-19, 401, x+19, 439), fill="#fff3d4")
        put(d, (215, 530), "五月开始的一次事件，可能延续到六月", 29, dark, True)
    elif scene == 4:
        crop_width = min(spatial.width, round(spatial.height*1.8))
        max_left = max(0, spatial.width-crop_width)
        left = int(max_left*p)
        panel = spatial.crop((left, 0, left+crop_width, spatial.height))
        panel.thumbnail((1050, 380))
        image.paste(panel, (round(640-panel.width/2), 205))
        d = ImageDraw.Draw(image)
        put(d, (110, 580), "NOAA OISST · 1996—2025 · 全南海", 24, dark, True)
    else:
        causes = ["海气热通量", "混合层深度", "风与海流", "垂向混合"]
        for k, label in enumerate(causes):
            x = 100+(k%2)*560; y = 240+(k//2)*155
            d.rounded_rectangle((x,y,x+480,y+110), 18, fill=teal if p>(k+1)/5 else "#b9d4d1")
            put(d, (x+80,y+32), label, 32, "#ffffff" if p>(k+1)/5 else dark, True)
        put(d, (235, 555), "先定义指标 → 再检验机制", 32, dark, True)
    return image


def duration(path: Path) -> float:
    result = subprocess.run([str(FFMPEG), "-hide_banner", "-i", str(path)], capture_output=True, text=True)
    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
    if not match: raise RuntimeError(f"No duration for {path}")
    h, m, s = match.groups()
    return int(h)*3600+int(m)*60+float(s)


async def make_audio():
    import edge_tts
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        os.environ.pop(key, None)
    for i, line in enumerate(NARRATION, 1):
        target = BUILD / f"zh-{i:02}.mp3"
        await edge_tts.Communicate(line, voice="zh-CN-XiaoxiaoNeural", rate="+8%").save(str(target))
        print("audio", i, target.stat().st_size, flush=True)


def make_video():
    durations = [duration(BUILD / f"zh-{i:02}.mp3") for i in range(1, 7)]
    def vtt_time(value: float) -> str:
        milliseconds = round(value * 1000)
        hours, remainder = divmod(milliseconds, 3600000)
        minutes, remainder = divmod(remainder, 60000)
        seconds, ms = divmod(remainder, 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02}.{ms:03}"
    cues = ["WEBVTT", ""]
    cursor = 0.0
    for i, (line, seconds) in enumerate(zip(NARRATION, durations), 1):
        cues.extend([str(i), f"{vtt_time(cursor)} --> {vtt_time(cursor + seconds)}", line, ""])
        cursor += seconds
    (ROOT / "assets" / "marine-heatwave-story-zh.vtt").write_text("\n".join(cues), encoding="utf-8")
    chart = Image.open(ROOT / "assets" / "marine-heatwaves-seasonal.png").convert("RGB")
    spatial = Image.open(ROOT / "assets" / "local-mhw-spatial-1996-2025.png").convert("RGB")
    poster = scene_frame(0, .75, chart, spatial)
    poster.save(ROOT / "assets" / "marine-heatwave-story-zh-poster.png", optimize=True)
    audio_list = BUILD / "audio.ffconcat"
    audio_list.write_text("ffconcat version 1.0\n" + "\n".join(f"file 'zh-{i:02}.mp3'" for i in range(1,7)) + "\n", encoding="utf-8")
    silent = BUILD / "animated-silent.mp4"
    cmd = [str(FFMPEG), "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-pix_fmt", "yuv420p", str(silent)]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for scene, seconds in enumerate(durations):
        frames = max(1, round(seconds*FPS))
        for frame in range(frames):
            image = scene_frame(scene, frame/max(frames-1,1), chart, spatial)
            process.stdin.write(image.tobytes())
        print("rendered scene", scene+1, flush=True)
    process.stdin.close()
    if process.wait(): raise RuntimeError("Video render failed")
    target = ROOT / "assets" / "marine-heatwave-story-zh-animated.mp4"
    subprocess.run([str(FFMPEG), "-y", "-hide_banner", "-loglevel", "error", "-i", str(silent), "-f", "concat", "-safe", "0", "-i", str(audio_list), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "-shortest", str(target)], check=True)
    print("OUTPUT", target, target.stat().st_size, "duration", sum(durations), flush=True)


if __name__ == "__main__":
    if sys.argv[1:] == ["audio"]: asyncio.run(make_audio())
    elif sys.argv[1:] == ["video"]: make_video()
    else: raise SystemExit("Use: audio or video")
