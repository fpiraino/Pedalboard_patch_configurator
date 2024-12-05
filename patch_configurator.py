
import os
import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import json

# Percorso al file di configurazione
config_path = os.path.join(os.path.dirname(__file__), 'config.py')

# Carica dinamicamente il modulo config
spec = importlib.util.spec_from_file_location('config', config_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

# Ora gli effetti possono essere usati dal modulo config
effects_timeline = config.effects_timeline
effects_looperhino = config.effects_looperhino
effects_mobius = config.effects_mobius

# Resto del codice del configuratore
class PatchConfiguratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Patch Configurator")
        self.patches = []
        self.config_file = config_path

        # Frames
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="NSEW")

        # Patch Number
        ttk.Label(self.main_frame, text="Numero Patch (0-127):").grid(row=0, column=0, sticky="W")
        self.patch_number_entry = ttk.Entry(self.main_frame, width=5)
        self.patch_number_entry.grid(row=0, column=1, sticky="W")

        # Patch Name
        ttk.Label(self.main_frame, text="Nome Patch:").grid(row=0, column=2, sticky="W")
        self.patch_name_entry = ttk.Entry(self.main_frame, width=30)
        self.patch_name_entry.grid(row=0, column=3, sticky="W")

        # Timeline Effect
        ttk.Label(self.main_frame, text="Effetto Timeline:").grid(row=1, column=0, sticky="W")
        self.timeline_effect = ttk.Combobox(self.main_frame, values=list(effects_timeline.keys()), width=25)
        self.timeline_effect.grid(row=1, column=1, sticky="W")
        self.timeline_state = ttk.Combobox(self.main_frame, values=["On", "Off"], width=10)
        self.timeline_state.grid(row=1, column=2, sticky="W")

        # Looperhino Effect
        ttk.Label(self.main_frame, text="Effetto Looperhino:").grid(row=2, column=0, sticky="W")
        self.looperhino_effect = ttk.Combobox(self.main_frame, values=list(effects_looperhino.keys()), width=25)
        self.looperhino_effect.grid(row=2, column=1, sticky="W")

        # Mobius Effect
        ttk.Label(self.main_frame, text="Effetto Mobius:").grid(row=3, column=0, sticky="W")
        self.mobius_effect = ttk.Combobox(self.main_frame, values=list(effects_mobius.keys()), width=25)
        self.mobius_effect.grid(row=3, column=1, sticky="W")
        self.mobius_state = ttk.Combobox(self.main_frame, values=["On", "Off"], width=10)
        self.mobius_state.grid(row=3, column=2, sticky="W")

        # Flint Boost
        ttk.Label(self.main_frame, text="Boost Flint (Dynamic Mode 1):").grid(row=4, column=0, sticky="W")
        self.flint_boost_state = ttk.Combobox(self.main_frame, values=["On", "Off"], width=10)
        self.flint_boost_state.grid(row=4, column=1, sticky="W")

        # Buttons
        self.add_patch_button = ttk.Button(self.main_frame, text="Aggiungi Patch", command=self.add_patch)
        self.add_patch_button.grid(row=5, column=0, pady=10)
        self.export_button = ttk.Button(self.main_frame, text="Esporta in Excel", command=self.export_to_excel)
        self.export_button.grid(row=5, column=1, pady=10)

        # Patch List
        self.patch_list = ttk.Treeview(self.main_frame, columns=("Numero", "Nome"), show="headings", height=10)
        self.patch_list.heading("Numero", text="Numero")
        self.patch_list.heading("Nome", text="Nome")
        self.patch_list.bind("<Double-1>", self.on_patch_double_click)
        self.patch_list.grid(row=6, column=0, columnspan=4, sticky="NSEW")

        # Carica patch salvate
        self.load_patches()
        self.populate_patch_list()

    def load_patches(self):
        # Metodo per caricare patch salvate (implementazione da aggiungere)
        pass

    def populate_patch_list(self):
        # Metodo per popolare la lista delle patch (implementazione da aggiungere)
        pass

    def add_patch(self):
        # Metodo per aggiungere una nuova patch (implementazione da aggiungere)
        pass

    def export_to_excel(self):
        # Metodo per esportare patch in Excel (implementazione da aggiungere)
        pass

    def on_patch_double_click(self, event):
        # Metodo per gestire il doppio click su una patch (implementazione da aggiungere)
        pass


# Avvio dell'applicazione
if __name__ == "__main__":
    root = tk.Tk()
    app = PatchConfiguratorGUI(root)
    root.mainloop()
