
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import json
import os
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# File per salvare le patch configurate
PATCHES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patches.json")

class PatchConfiguratorGUI:
        self.config_file = CONFIG_FILE
    def __init__(self, root):
        self.root = rootgi
        self.root.title("Patch Configurator")
        self.patches = []

        # Carica le patch salvate
        self.load_patches()

        # Frames
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="NSEW")

        # Patch Number
        ttk.Label(self.main_frame, text="Numero Patch (1-127):").grid(row=0, column=0, sticky="W")
        self.patch_number_entry = ttk.Entry(self.main_frame, width=5)
        self.patch_number_entry.grid(row=0, column=1, sticky="W")

        # Patch Name
        ttk.Label(self.main_frame, text="Nome Patch:").grid(row=0, column=2, sticky="W")
        self.patch_name_entry = ttk.Entry(self.main_frame, width=30)
        self.patch_name_entry.grid(row=0, column=3, sticky="W")

        # Timeline Effect
        ttk.Label(self.main_frame, text="Effetto Timeline:").grid(row=1, column=0, sticky="W")
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
        self.flint_boost_state.grid(row=4, column=1, sticky="W")


        # Looperhino Effect
        ttk.Label(self.main_frame, text="Effetto Looperhino:").grid(row=1, column=0, sticky="W")
        self.looperhino_effect = ttk.Combobox(self.main_frame, values=list(effects_looperhino.keys()), width=25)
        self.looperhino_effect.grid(row=1, column=1, sticky="W")

        # Timeline Effect
        ttk.Label(self.main_frame, text="Effetto Timeline:").grid(row=2, column=0, sticky="W")
        self.timeline_effect = ttk.Combobox(self.main_frame, values=list(effects_timeline.keys()), width=25)
        self.timeline_effect.grid(row=2, column=1, sticky="W")
        self.timeline_state = ttk.Combobox(self.main_frame, values=["On", "Off"], width=10)
        self.timeline_state.grid(row=2, column=2, sticky="W")

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

        # Popola la lista delle patch
        self.populate_patch_list()

    def add_patch(self):
        patch_number = self.patch_number_entry.get()
        patch_name = self.patch_name_entry.get()
        if not patch_number.isdigit() or not (0 <= int(patch_number) <= 127):
            messagebox.showerror("Errore", "Il numero della patch deve essere tra 1 e 127!")
            return
        if not patch_name:
            messagebox.showerror("Errore", "Il nome della patch è obbligatorio!")
            return

        timeline = self.timeline_effect.get()
        timeline_state = self.timeline_state.get()
        looperhino = self.looperhino_effect.get()
        mobius = self.mobius_effect.get()
        mobius_state = self.mobius_state.get()
        flint_boost_state = self.flint_boost_state.get()

        forms = []

        if timeline:
            cc_value = "127" if timeline_state == "On" else "0"
            timeline_effect_desc = f"{effects_timeline[timeline]} ({timeline})"
            forms.append({
                "FORM": "FORM1",
                "Canale MIDI": 1,
                "Tipo": "PC + CC",
                "Messaggio": f"{timeline_effect_desc}, CC102={cc_value} ({'On' if cc_value == '127' else 'Off'})"
            })

        if looperhino:
            looperhino_effect_desc = f"{effects_looperhino[looperhino]} ({looperhino})"
            forms.append({
                "FORM": "FORM3",
                "Canale MIDI": 3,
                "Tipo": "PC",
                "Messaggio": looperhino_effect_desc
            })

        if mobius:
            cc_value = "127" if mobius_state == "On" else "0"
            mobius_effect_desc = f"{effects_mobius[mobius]} ({mobius})"
            forms.append({
                "FORM": "FORM4",
                "Canale MIDI": 4,
                "Tipo": "PC + CC",
                "Messaggio": f"{mobius_effect_desc}, CC102={cc_value} ({'On' if cc_value == '127' else 'Off'})"
            })

        if flint_boost_state:
            cc_value = "127" if flint_boost_state == "On" else "0"
            forms.append({
                "FORM": "FORM2",
                "Canale MIDI": 2,
                "Tipo": "CC",
                "Messaggio": f"CC22={cc_value} (Dynamic Mode 1, {'On' if cc_value == '127' else 'Off'})"
            })

        for form in forms:
            self.patches.append({"Patch Number": patch_number, "Patch Name": patch_name, **form})

        # Salva le patch nel file
        self.save_patches()

        # Aggiorna la lista
        self.patch_list.insert("", "end", values=(patch_number, patch_name))

        # Reset inputs
        self.patch_number_entry.delete(0, tk.END)
        self.patch_name_entry.delete(0, tk.END)
        self.timeline_effect.set("")
        self.timeline_state.set("")
        self.looperhino_effect.set("")
        self.mobius_effect.set("")
        self.mobius_state.set("")
        self.flint_boost_state.set("")

        messagebox.showinfo("Successo", f"La patch '{patch_name}' è stata aggiunta!")

    def on_patch_double_click(self, event):
        selected_item = self.patch_list.selection()[0]
        patch_number, patch_name = self.patch_list.item(selected_item, "values")

        # Popup con opzioni
        popup = tk.Toplevel(self.root)
        popup.title(f"Patch {patch_name} - Opzioni")
        ttk.Label(popup, text=f"Patch {patch_name} - Seleziona un'opzione").pack(pady=10)

        ttk.Button(popup, text="Visualizza", command=lambda: self.show_patch_details(patch_number, popup)).pack(pady=5)
        ttk.Button(popup, text="Elimina", command=lambda: self.delete_patch(patch_number, selected_item, popup)).pack(pady=5)

    def show_patch_details(self, patch_number, popup):
        patch_details = sorted(
            [patch for patch in self.patches if patch["Patch Number"] == patch_number],
            key=lambda x: x["FORM"]
        )
        if not patch_details:
            messagebox.showerror("Errore", "Dettagli non trovati!")
            popup.destroy()
            return

        # Finestra con tabella
        details_popup = tk.Toplevel(self.root)
        details_popup.title(f"Dettagli Patch {patch_number}")
        tree = ttk.Treeview(details_popup, columns=("FORM", "Canale MIDI", "Tipo", "Messaggio"), show="headings")
        tree.heading("FORM", text="FORM")
        tree.heading("Canale MIDI", text="Canale MIDI")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Messaggio", text="Messaggio")

        for detail in patch_details:
            tree.insert("", "end", values=(detail["FORM"], detail["Canale MIDI"], detail["Tipo"], detail["Messaggio"]))

        tree.pack(fill="both", expand=True)
        ttk.Button(details_popup, text="Chiudi", command=details_popup.destroy).pack(pady=10)
        popup.destroy()

    def delete_patch(self, patch_number, selected_item, popup):
        self.patches = [patch for patch in self.patches if patch["Patch Number"] != patch_number]
        self.patch_list.delete(selected_item)
        self.save_patches()
        messagebox.showinfo("Successo", f"La patch {patch_number} è stata eliminata!")
        popup.destroy()

    def export_to_excel(self):
        if not self.patches:
            messagebox.showerror("Errore", "Non ci sono patch da esportare!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx")])
        if not file_path:
            return

        df = pd.DataFrame(self.patches)
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Successo", f"Le patch sono state esportate in {file_path}!")

    def save_patches(self):
        with open(PATCHES_FILE, "w") as file:
            json.dump(self.patches, file)

    def load_patches(self):
        if os.path.exists(PATCHES_FILE):
            with open(PATCHES_FILE, "r") as file:
                self.patches = json.load(file)

    def populate_patch_list(self):
        for patch in self.patches:
            self.patch_list.insert("", "end", values=(patch["Patch Number"], patch["Patch Name"]))


root = tk.Tk()
app = PatchConfiguratorGUI(root)
root.mainloop()
