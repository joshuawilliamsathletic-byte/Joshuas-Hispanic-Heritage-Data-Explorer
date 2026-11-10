import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("A beginner-friendly app for experimenting with names, fonts, backgrounds, and motion.")

with st.sidebar:
    st.header("Customize your display")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender", "Midnight"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=1, max_value=10, value=5,
                      help="Higher values make the animation move faster.")
    st.caption("Animations run continuously in the preview. Change any control to update it.")

backgrounds = {
    "Light": ("#f8fafc", "#172033"),
    "Dark": ("#101218", "#f8fafc"),
    "Ocean": ("#063b5c", "#e7fbff"),
    "Sunset": ("linear-gradient(135deg, #ff9966, #ff5e62)", "#ffffff"),
    "Forest": ("#123524", "#f0fff4"),
    "Lavender": ("#eee7ff", "#34245c"),
    "Midnight": ("#090d2e", "#e8eaff"),
}
bg, foreground = backgrounds[background]
safe_name = html.escape(name.strip() or "Hello World")
font_css = {
    "Arial": "Arial, Helvetica, sans-serif",
    "Courier New": "'Courier New', monospace",
    "Georgia": "Georgia, serif",
    "Times New Roman": "'Times New Roman', serif",
    "Verdana": "Verdana, sans-serif",
    "Trebuchet MS": "'Trebuchet MS', sans-serif",
    "Impact": "Impact, sans-serif",
}[font_family]

# Create particles with CSS-only motion so the animation loops smoothly without rerunning Streamlit.
random.seed(42)
particles = []
particle_count = 0 if effect == "None" else 46
symbols = {
    "Rain": ["💧", "💦"],
    "Snow": ["❄", "❅", "❆", "✳"],
    "Hail": ["●", "◆", "❄"],
    "Wind Gust": ["〰", "〜", "➝", "﹏"],
    "Confetti": ["🎉", "🟡", "🟣", "🟢", "🔵", "🎊", "♦"],
    "Tornado": ["🌪", "〰", "﹏"],
}
for i in range(particle_count):
    symbol = random.choice(symbols[effect])
    left = random.uniform(0, 98)
    delay = random.uniform(-12, 0)
    duration = random.uniform(2.2, 7.0) * (1.25 - speed / 20)
    size = random.randint(12, 25) if effect != "Hail" else random.randint(8, 18)
    drift = random.randint(-90, 90)
    if effect == "Wind Gust":
        animation = "gust"
        duration = random.uniform(2.0, 4.8) * (1.25 - speed / 20)
        top = random.randint(5, 90)
    elif effect == "Tornado":
        animation = "twister"
        top = random.randint(0, 85)
        duration = random.uniform(2.5, 5.0) * (1.25 - speed / 20)
    elif effect == "Confetti":
        animation = "fall-spin"
        top = random.randint(-100, 0)
    else:
        animation = "fall"
        top = random.randint(-100, 0)
    particles.append(
        f'<span class="particle {animation}" style="left:{left:.2f}%;top:{top}%;'
        f'--delay:{delay:.2f}s;--duration:{duration:.2f}s;--drift:{drift}px;'
        f'font-size:{size}px">{symbol}</span>'
    )

if name_mode == "Ticker Tape":
    name_markup = f'<div class="ticker"><span>{safe_name}</span><span aria-hidden="true">{safe_name}</span></div>'
elif name_mode == "Repeated":
    name_markup = '<div class="repeated">' + "".join(f"<span>{safe_name}</span>" for _ in range(6)) + "</div>"
else:
    name_markup = f'<div class="center-name">{safe_name}</div>'

html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; width: 100%; height: 100%; }}
.stage {{
  position: relative; height: 620px; width: 100%; overflow: hidden;
  border-radius: 18px; background: {bg}; color: {foreground};
  font-family: {font_css}; isolation: isolate;
}}
.particles {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 1; }}
.particle {{ position: absolute; display: block; opacity: .82; user-select: none; }}
.fall {{ animation: fall var(--duration) linear var(--delay) infinite; }}
.fall-spin {{ animation: fall-spin var(--duration) linear var(--delay) infinite; }}
.gust {{ animation: gust var(--duration) ease-in-out var(--delay) infinite; }}
.twister {{ animation: twister var(--duration) linear var(--delay) infinite; }}
@keyframes fall {{
  0% {{ transform: translate3d(0,-12vh,0); opacity: 0; }}
  10% {{ opacity: .9; }}
  100% {{ transform: translate3d(var(--drift), 760px,0); opacity: .7; }}
}}
@keyframes fall-spin {{
  0% {{ transform: translate3d(0,-12vh,0) rotate(0deg); opacity: 0; }}
  10% {{ opacity: 1; }}
  100% {{ transform: translate3d(var(--drift),760px,0) rotate(900deg); opacity: .8; }}
}}
@keyframes gust {{
  0%,100% {{ transform: translateX(-120px) rotate(-8deg); opacity: 0; }}
  15%,80% {{ opacity: .85; }}
  50% {{ transform: translateX(110vw) rotate(8deg); }}
}}
@keyframes twister {{
  0% {{ transform: translate(-40px,-10px) rotate(0deg) scale(.65); opacity: 0; }}
  15% {{ opacity: .9; }}
  50% {{ transform: translate(40px, 220px) rotate(360deg) scale(1.15); }}
  100% {{ transform: translate(-25px, 700px) rotate(720deg) scale(.7); opacity: 0; }}
}}
.name-layer {{
  position: absolute; z-index: 3; inset: 0; display: flex; align-items: center;
  justify-content: center; padding: 28px; font-size: {font_size}px; font-weight: 700;
  text-shadow: 0 2px 14px rgba(0,0,0,.14); overflow: hidden;
}}
.center-name {{ text-align: center; overflow-wrap: anywhere; }}
.ticker {{ display: flex; width: max-content; gap: 100px; white-space: nowrap;
  animation: marquee {max(5, 24 - speed * 1.7):.1f}s linear infinite; }}
.ticker span {{ flex-shrink: 0; }}
@keyframes marquee {{ from {{ transform: translateX(55vw); }} to {{ transform: translateX(-100%); }} }}
.repeated {{ width: 100%; display: grid; grid-template-columns: repeat(2,minmax(0,1fr));
  gap: 24px; text-align: center; overflow-wrap: anywhere; }}
.repeated span {{ opacity: .94; }}
.footer {{ position: absolute; z-index: 4; bottom: 12px; left: 16px; font: 12px Arial,sans-serif;
  opacity: .7; }}
@media (prefers-reduced-motion: reduce) {{
  .particle, .ticker {{ animation-duration: 30s !important; }}
}}
</style>
</head>
<body>
<div class="stage">
  <div class="particles">{''.join(particles)}</div>
  <div class="name-layer">{name_markup}</div>
  <div class="footer">Hello World Motion Lab · {html.escape(effect)} effect</div>
</div>
</body>
</html>
"""

components.html(html_doc, height=640, scrolling=False)

st.info("Tip: Try Ticker Tape with Confetti, then switch fonts and backgrounds to see how the preview changes.")
