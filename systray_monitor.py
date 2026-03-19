import threading
import time
import sys

try:
    import psutil
except ImportError:
    sys.exit("Falta psutil. Ejecuta: pip install psutil")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Falta Pillow. Ejecuta: pip install pillow")

try:
    import pystray
except ImportError:
    sys.exit("Falta pystray. Ejecuta: pip install pystray")


INTERVALO = 2
TAM = 256


def get_font(size):
    for path in [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/consola.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def crear_icono_cpu(val):
    img = Image.new("RGBA", (TAM, TAM), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if val >= 80:
        color = (255, 80, 80)
        fondo = (60, 15, 15, 255)
    elif val >= 50:
        color = (255, 185, 50)
        fondo = (55, 40, 10, 255)
    else:
        color = (80, 215, 120)
        fondo = (12, 45, 22, 255)

    draw.rounded_rectangle([0, 0, TAM - 1, TAM - 1], radius=40, fill=fondo)

    # Numero grande que llena el icono
    f_num = get_font(150)
    draw.text((TAM // 2, TAM // 2), f"{int(val)}", font=f_num, fill=color, anchor="mm")

    # Porcentaje abajo derecha pequeño
    f_pct = get_font(48)
    draw.text((TAM - 18, TAM - 18), "%", font=f_pct, fill=(*color[:3], 180), anchor="rb")

    return img


def crear_icono_ram(val):
    img = Image.new("RGBA", (TAM, TAM), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if val >= 80:
        color = (255, 80, 80)
        fondo = (60, 15, 15, 255)
    elif val >= 60:
        color = (255, 185, 50)
        fondo = (55, 40, 10, 255)
    else:
        color = (90, 165, 255)
        fondo = (10, 25, 55, 255)

    draw.rounded_rectangle([0, 0, TAM - 1, TAM - 1], radius=40, fill=fondo)

    f_num = get_font(150)
    draw.text((TAM // 2, TAM // 2), f"{int(val)}", font=f_num, fill=color, anchor="mm")

    f_pct = get_font(48)
    draw.text((TAM - 18, TAM - 18), "%", font=f_pct, fill=(*color[:3], 180), anchor="rb")

    return img


def actualizar(icono_cpu, icono_ram):
    psutil.cpu_percent(interval=None)
    time.sleep(0.5)
    while getattr(icono_cpu, "_running", True):
        try:
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().percent

            icono_cpu.icon = crear_icono_cpu(cpu)
            icono_cpu.title = f"CPU: {cpu:.1f}%"

            icono_ram.icon = crear_icono_ram(ram)
            icono_ram.title = f"RAM: {ram:.1f}%"
        except Exception:
            pass
        time.sleep(INTERVALO)


def hacer_salir(icono_cpu, icono_ram):
    def salir(icono, item):
        icono_cpu._running = False
        icono_cpu.stop()
        icono_ram.stop()
    return salir


img_cpu = crear_icono_cpu(0)
img_ram = crear_icono_ram(0)

icono_cpu = pystray.Icon("monitor_cpu", img_cpu, "CPU: cargando...")
icono_ram = pystray.Icon("monitor_ram", img_ram, "RAM: cargando...")

salir_fn = hacer_salir(icono_cpu, icono_ram)

icono_cpu.menu = pystray.Menu(
    pystray.MenuItem("CPU — Procesador", None, enabled=False),
    pystray.Menu.SEPARATOR,
    pystray.MenuItem("Salir", salir_fn),
)
icono_ram.menu = pystray.Menu(
    pystray.MenuItem("RAM — Memoria", None, enabled=False),
    pystray.Menu.SEPARATOR,
    pystray.MenuItem("Salir", salir_fn),
)

icono_cpu._running = True

hilo_update = threading.Thread(target=actualizar, args=(icono_cpu, icono_ram), daemon=True)
hilo_update.start()

hilo_ram = threading.Thread(target=icono_ram.run, daemon=True)
hilo_ram.start()

icono_cpu.run()