# App per configurazione pedaliera

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Dizionari di mapping per gli effetti
effects_timeline = {"dDuck": "PC1", "dDual": "PC2", "dSlap": "PC3", "dTape": "PC0"}
effects_looperhino = {"COMP": "PC1", "Low OD": "PC2", "Mid OD": "PC3", "Hi OD": "PC4"}
effects_mobius = {"hTrem": "PC0", "oTrem": "PC1", "tTrem": "PC2", "aChor": "PC3", "Phas": "PC4"}

class PatchConfiguratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Patch Configurator")
        self.patches = []

        # Frames
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="NSEW")

        # Patch Name
        ttk.Label(self.main_frame, text="Nome Patch:").grid(row=0, column=0, sticky="W")
        self.patch_name_entry = ttk.Entry(self.main_frame, width=30)
        self.patch_name_entry.grid(row=0, column=1, sticky="W")

        # Timeline Effect
        ttk.Label(self.main_frame, text="Effetto Timeline:").grid(row=1, column=0, sticky="W")
        self.timeline_effect = ttk.Combobox(self.main_frame, values=list(effects_timeline.keys()), width=25)
        self.timeline_effect.grid(row=1, column=1, sticky="W")

        # Looperhino Effect
        ttk.Label(self.main_frame, text="Effetto Looperhino:").grid(row=2, column=0, sticky="W")
        self.looperhino_effect = ttk.Combobox(self.main_frame, values=list(effects_looperhino.keys()), width=25)
        self.looperhino_effect.grid(row=2, column=1, sticky="W")

        # Mobius Effect
        ttk.Label(self.main_frame, text="Effetto Mobius:").grid(row=3, column=0, sticky="W")
        self.mobius_effect = ttk.Combobox(self.main_frame, values=list(effects_mobius.keys()), width=25)
        self.mobius_effect.grid(row=3, column=1, sticky="W")

        # Buttons
        self.add_patch_button = ttk.Button(self.main_frame, text="Aggiungi Patch", command=self.add_patch)
        self.add_patch_button.grid(row=4, column=0, pady=10)
        self.export_button = ttk.Button(self.main_frame, text="Esporta in Excel", command=self.export_to_excel)
        self.export_button.grid(row=4, column=1, pady=10)
        self.show_patches_button = ttk.Button(self.main_frame, text="Mostra Configurazioni", command=self.show_patches)
        self.show_patches_button.grid(row=4, column=2, pady=10)

    def add_patch(self):
        """Aggiungi una nuova patch."""
        patch_name = self.patch_name_entry.get()
        if not patch_name:
            messagebox.showerror("Errore", "Il nome della patch è obbligatorio!")
            return

        timeline = self.timeline_effect.get()
        looperhino = self.looperhino_effect.get()
        mobius = self.mobius_effect.get()

        if not (timeline or looperhino or mobius):
            messagebox.showerror("Errore", "Devi selezionare almeno un effetto!")
            return

        forms = []
        if timeline:
            forms.append({"FORM": "FORM1", "Canale MIDI": 1, "Tipo": "PC + CC", "Messaggio": f"{effects_timeline[timeline]}, CC102=127 (On)"})
        if looperhino:
            forms.append({"FORM": "FORM3", "Canale MIDI": 3, "Tipo": "PC", "Messaggio": f"{effects_looperhino[looperhino]}"})
        if mobius:
            forms.append({"FORM": "FORM4", "Canale MIDI": 4, "Tipo": "PC + CC", "Messaggio": f"{effects_mobius[mobius]}, CC102=127 (On)"})

        for form in forms:
            self.patches.append({"Patch Name": patch_name, **form})

        # Reset inputs
        self.patch_name_entry.delete(0, tk.END)
        self.timeline_effect.set("")
        self.looperhino_effect.set("")
        self.mobius_effect.set("")

        messagebox.showinfo("Successo", f"La patch '{patch_name}' è stata aggiunta!")

    def export_to_excel(self):
        """Esporta tutte le patch in un file Excel."""
        if not self.patches:
            messagebox.showerror("Errore", "Non ci sono patch da esportare!")
            return

        df = pd.DataFrame(self.patches)
        file_path = "Patch_Configurations_GUI.xlsx"
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Successo", f"Le patch sono state esportate in {file_path}!")

    def show_patches(self):
        """Mostra le configurazioni delle patch in una finestra popup."""
        if not self.patches:
            messagebox.showerror("Errore", "Non ci sono patch da mostrare!")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Configurazioni Patch")

        tree = ttk.Treeview(popup, columns=("FORM", "Canale MIDI", "Tipo", "Messaggio"), show="headings")
        tree.heading("FORM", text="FORM")
        tree.heading("Canale MIDI", text="Canale MIDI")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Messaggio", text="Messaggio")

        for patch in self.patches:
            tree.insert("", "end", values=(patch["FORM"], patch["Canale MIDI"], patch["Tipo"], patch["Messaggio"]))

        tree.pack(fill="both", expand=True)
        ttk.Button(popup, text="Chiudi", command=popup.destroy).pack(pady=10)


# Avvia l'interfaccia grafica
root = tk.Tk()
app = PatchConfiguratorGUI(root)
root.mainloop()
