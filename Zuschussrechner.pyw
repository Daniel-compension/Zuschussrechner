import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import os
import json
from datetime import datetime

CONFIG_FILE = "config.json"

# Funktion zum Laden oder Erzeugen der Konfigurationsdatei
def load_or_create_config():
    current_year = datetime.now().year
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            if str(current_year) in config:
                return round((config[str(current_year)] * 0.04) / 12, 2)
    return None

def save_config(yearly_bbg):
    current_year = datetime.now().year
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    config[str(current_year)] = yearly_bbg
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# GUI für die Eingabe der BBG
class SetupWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Einrichtung")
        self.master.geometry("400x150")
        self.master.configure(bg="#f9f9f9")

        ttk.Label(self.master, text="Beitragsbemessungsgrenze (jährlich in €):").pack(pady=10)
        self.bbg_entry = ttk.Entry(self.master)
        self.bbg_entry.insert(0, "96600")
        self.bbg_entry.pack()
        ttk.Button(self.master, text="Weiter", command=self.save_bbg).pack(pady=10)

    def save_bbg(self):
        global BBG_2025
        try:
            bbg = float(self.bbg_entry.get().replace(",", "."))
            save_config(bbg)
            BBG_2025 = round((bbg * 0.04) / 12, 2)
        except ValueError:
            BBG_2025 = 322  # Fallback
        self.master.destroy()
        start_main_gui()

# Haupt-GUI Setup

def start_main_gui():
    root = tk.Tk()
    root.title("Beitragsaufteilung Rechner")
    root.geometry("600x550")
    root.configure(bg="#f9f9f9")

    # Logo einfügen (Pfad ggf. anpassen)
    logo_path = os.path.join(os.path.dirname(__file__), "COMPENSION 2025 - transparenter Hintergrund.png")
    if os.path.exists(logo_path):
        logo_img = PhotoImage(file=logo_path)
        logo_label = tk.Label(root, image=logo_img, bg="#f9f9f9")
        logo_label.image = logo_img
        logo_label.pack(pady=(20, 10))

    # Style (modern)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#ffffff")
    style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#cce600")
    style.map("TButton", background=[("active", "#b5d700")])
    style.configure("TCheckbutton", background="#ffffff", font=("Segoe UI", 10))
    style.configure("TCombobox", font=("Segoe UI", 10))

    outer_frame = tk.Frame(root, bg="#f9f9f9")
    outer_frame.pack(expand=True, fill="both")
    card = tk.Frame(outer_frame, bg="#ffffff")
    card.pack(padx=20, pady=20, fill="both", expand=True)
    card.grid_columnconfigure(1, weight=1)

    def open_setup():
        root.destroy()
        setup = tk.Tk()
        SetupWindow(setup)
        setup.mainloop()

    # Änderung der BBG zulassen
    ttk.Button(card, text="BBG ändern", command=open_setup).grid(row=0, column=3, padx=10, pady=5)

    tk.Label(card, text="Gesamtbeitrag:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    gesamtbeitrag_entry = ttk.Entry(card)
    gesamtbeitrag_entry.grid(row=0, column=1, sticky="ew")
    tk.Label(card, text="€").grid(row=0, column=2, sticky="w")

    ag_zuschuss_var = tk.StringVar()
    ag_zuschuss_combo = ttk.Combobox(card, textvariable=ag_zuschuss_var, values=["15%", "20%", "30%", "Individuell"], state="readonly")
    ag_zuschuss_combo.grid(row=1, column=1, sticky="ew")
    ag_zuschuss_combo.current(1)
    tk.Label(card, text="AG-Zuschuss:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    ag_zuschuss_entry = ttk.Entry(card)
    ag_zuschuss_einheit = tk.Label(card, text="%")

    avwl_var = tk.StringVar()
    avwl_combo = ttk.Combobox(card, textvariable=avwl_var, values=["0,00 €", "13,29 €", "26,59 €", "40 €", "Sonstige"], state="readonly")
    avwl_combo.grid(row=2, column=1, sticky="ew")
    avwl_combo.current(2)
    tk.Label(card, text="AVWL:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    avwl_entry = ttk.Entry(card)
    avwl_einheit = tk.Label(card, text="€")

    zuschuss_auf_avwl_var = tk.BooleanVar()
    check_avwl = ttk.Checkbutton(card, text="AG-Zuschuss auf AVWL rechnen", variable=zuschuss_auf_avwl_var)
    check_avwl.grid(row=3, column=1, columnspan=2, sticky="w", padx=10, pady=(10, 0))

    begrenzen_var = tk.BooleanVar()
    check_bbg = ttk.Checkbutton(card, text="Zuschuss auf 4% BBG begrenzen", variable=begrenzen_var)
    check_bbg.grid(row=4, column=1, columnspan=2, sticky="w", padx=10, pady=(0, 10))

    beitrag_output_var = tk.StringVar()
    ag_zuschuss_prozent_output_var = tk.StringVar()
    ag_zuschuss_output_var = tk.StringVar()
    avwl_output_var = tk.StringVar()
    entgeltumwandlung_output_var = tk.StringVar()

    def update_individuelle_eingaben(*args):
        if ag_zuschuss_var.get() == "Individuell":
            ag_zuschuss_entry.grid(row=1, column=2, padx=5, sticky="w")
            ag_zuschuss_einheit.grid(row=1, column=3, padx=(0, 10), sticky="w")
        else:
            ag_zuschuss_entry.grid_remove()
            ag_zuschuss_einheit.grid_remove()

        if avwl_var.get() == "Sonstige":
            avwl_entry.grid(row=2, column=2, padx=5, sticky="w")
            avwl_einheit.grid(row=2, column=3, padx=(0, 10), sticky="w")
        else:
            avwl_entry.grid_remove()
            avwl_einheit.grid_remove()

    def parse_float(value):
        try:
            return float(value.strip().replace("%", "").replace(" €", "").replace(",", "."))
        except ValueError:
            return None

    def berechne():
        beitrag = parse_float(gesamtbeitrag_entry.get())
        if beitrag is None:
            ag_zuschuss_output_var.set("Ungültige Eingabe")
            entgeltumwandlung_output_var.set("Bitte Zahlen prüfen")
            return

        if ag_zuschuss_var.get() == "Individuell":
            ag_zuschuss_prozent = parse_float(ag_zuschuss_entry.get())
        else:
            ag_zuschuss_prozent = parse_float(ag_zuschuss_var.get())

        if ag_zuschuss_prozent is None:
            ag_zuschuss_output_var.set("Ungültiger Zuschuss")
            entgeltumwandlung_output_var.set("Bitte Zuschuss prüfen")
            return

        ag_zuschuss_prozent /= 100

        if avwl_var.get() == "Sonstige":
            avwl = parse_float(avwl_entry.get())
        else:
            avwl = parse_float(avwl_var.get())

        if avwl is None:
            ag_zuschuss_output_var.set("Ungültige AVWL")
            entgeltumwandlung_output_var.set("Bitte AVWL prüfen")
            return

        ag_zuschuss_euro = 0
        entgeltumwandlung = 0

        if begrenzen_var.get():
            max_bemessung = min(beitrag, BBG_2025)
            x = max_bemessung / (1 + ag_zuschuss_prozent)
            ag_zuschuss_euro = x * ag_zuschuss_prozent
            entgeltumwandlung = beitrag - ag_zuschuss_euro - avwl
        elif zuschuss_auf_avwl_var.get():
            x = beitrag / (1 + ag_zuschuss_prozent)
            ag_zuschuss_euro = x * ag_zuschuss_prozent
            entgeltumwandlung = beitrag - ag_zuschuss_euro - avwl
        else:
            bemessung = beitrag - avwl
            x = bemessung / (1 + ag_zuschuss_prozent)
            ag_zuschuss_euro = x * ag_zuschuss_prozent
            entgeltumwandlung = beitrag - ag_zuschuss_euro - avwl

        ag_zuschuss_output_var.set(f"{ag_zuschuss_euro:.2f} €")
        entgeltumwandlung_output_var.set(f"{entgeltumwandlung:.2f} €")
        ag_zuschuss_prozent_output_var.set(f"{ag_zuschuss_prozent * 100:.2f}%")
        avwl_output_var.set(f"{avwl:.2f} €")
        beitrag_output_var.set(f"{beitrag:.2f} €")

    ag_zuschuss_var.trace("w", update_individuelle_eingaben)
    avwl_var.trace("w", update_individuelle_eingaben)
    update_individuelle_eingaben()

    ttk.Button(card, text="Berechnen", command=berechne).grid(row=5, column=1, pady=10)

    tk.Label(card, text="\nGesamtbeitrag:").grid(row=6, column=0, sticky="e")
    tk.Label(card, textvariable=beitrag_output_var, font=("Segoe UI", 10, "bold")).grid(row=6, column=1, sticky="w")
    tk.Label(card, text="AG-Zuschuss (%):").grid(row=7, column=0, sticky="e")
    tk.Label(card, textvariable=ag_zuschuss_prozent_output_var).grid(row=7, column=1, sticky="w")
    tk.Label(card, text="AG-Zuschuss in €:").grid(row=8, column=0, sticky="e")
    tk.Label(card, textvariable=ag_zuschuss_output_var, font=("Segoe UI", 10, "bold")).grid(row=8, column=1, sticky="w")
    tk.Label(card, text="AVWL:").grid(row=9, column=0, sticky="e")
    tk.Label(card, textvariable=avwl_output_var).grid(row=9, column=1, sticky="w")
    tk.Label(card, text="Entgeltumwandlung:").grid(row=10, column=0, sticky="e")
    tk.Label(card, textvariable=entgeltumwandlung_output_var, font=("Segoe UI", 10, "bold")).grid(row=10, column=1, sticky="w")

    root.mainloop()

# Start mit Einrichtung, wenn nötig
BBG_2025 = load_or_create_config()
if BBG_2025 is None:
    setup = tk.Tk()
    SetupWindow(setup)
    setup.mainloop()
else:
    start_main_gui()
