import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

# Dizionari di mapping per gli effetti
effects_timeline = {"dDuck": "PC1", "dDual": "PC2", "dSlap": "PC3", "dTape": "PC0"}
effects_looperhino = {
    "COMP": "PC1",
    "Low OD": "PC2",
    "Mid OD": "PC3",
    "Hi OD": "PC4",
    "COMP + Low OD": "PC5",
    "COMP + Mid OD": "PC6",
    "Low OD + Mid OD": "PC7",
    "Low OD + Hi OD": "PC8",
    "All Loops On": "PC0"
}
effects_mobius = {"hTrem": "PC0", "oTrem": "PC1", "tTrem": "PC2", "aChor": "PC3", "Phas": "PC4"}

class PatchConfiguratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Patch Configurator")
        self.patches = []

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

        # Buttons
        self.add_patch_button = ttk.Button(self.main_frame, text="Aggiungi Patch", command=self.add_patch)
        self.add_patch_button.grid(row=4, column=0, pady=10)
        self.export_button = ttk.Button(self.main_frame, text="Esporta in Excel", command=self.export_to_excel)
        self.export_button.grid(row=4, column=1, pady=10)

        # Patch List
        self.patch_list = ttk.Treeview(self.main_frame, columns=("Numero", "Nome"), show="headings", height=10)
        self.patch_list.heading("Numero", text="Numero")
        self.patch_list.heading("Nome", text="Nome")
        self.patch_list.bind("<Double-1>", self.show_patch_details)
        self.patch_list.grid(row=5, column=0, columnspan=4, sticky="NSEW")

    def add_patch(self):
        patch_number = self.patch_number_entry.get()
        patch_name = self.patch_name_entry.get()
        if not patch_number.isdigit() or not (1 <= int(patch_number) <= 127):
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

        forms = []

        if timeline:
            cc_value = "127" if timeline_state == "On" else "0"
            forms.append({
                "FORM": "FORM1",
                "Canale MIDI": 1,
                "Tipo": "PC + CC",
                "Messaggio": f"{effects_timeline[timeline]}, CC102={cc_value}"
            })

        if looperhino:
            forms.append({
                "FORM": "FORM3",
                "Canale MIDI": 3,
                "Tipo": "PC",
                "Messaggio": f"{effects_looperhino[looperhino]}"
            })

        if mobius:
            cc_value = "127" if mobius_state == "On" else "0"
            forms.append({
                "FORM": "FORM4",
                "Canale MIDI": 4,
                "Tipo": "PC + CC",
                "Messaggio": f"{effects_mobius[mobius]}, CC102={cc_value}"
            })

        for form in forms:
            self.patches.append({"Patch Number": patch_number, "Patch Name": patch_name, **form})

        self.patch_list.insert("", "end", values=(patch_number, patch_name))

        # Reset inputs
        self.patch_number_entry.delete(0, tk.END)
        self.patch_name_entry.delete(0, tk.END)
        self.timeline_effect.set("")
        self.timeline_state.set("")
        self.looperhino_effect.set("")
        self.mobius_effect.set("")
        self.mobius_state.set("")

        messagebox.showinfo("Successo", f"La patch '{patch_name}' è stata aggiunta!")

    def show_patch_details(self, event):
        selected_item = self.patch_list.selection()[0]
        patch_number, patch_name = self.patch_list.item(selected_item, "values")
        patch_details = [patch for patch in self.patches if patch["Patch Number"] == patch_number]
        details_message = f"Patch Number: {patch_number}\nPatch Name: {patch_name}\n"
        for detail in patch_details:
            details_message += f"\nFORM: {detail['FORM']}, Canale MIDI: {detail['Canale MIDI']}, Tipo: {detail['Tipo']}, Messaggio: {detail['Messaggio']}"
        messagebox.showinfo("Dettagli Patch", details_message)

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


root = tk.Tk()
app = PatchConfiguratorGUI(root)
root.mainloop()
