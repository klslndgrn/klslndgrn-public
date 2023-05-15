import tkinter as tk
import GUI_prerequisite
import psclasses as psc
import main
from tkinter import filedialog


class FileBrowser(GUI_prerequisite.Prerequisite):
    """
    Tkinter file browser.
    """

    def __init__(self):
        GUI_prerequisite.Prerequisite.__init__(self)

        self.master = tk.Tk()
        self.master.title("PowerGrid creator from XML-files")

        self.topFrame = tk.Frame(self.master)
        self.topFrame.grid()

        self.rightFrame = tk.Frame(self.master)
        self.rightFrame.grid(row=0, rowspan=3, column=1, sticky=tk.N)

        input1 = Input(self.topFrame, self.rightFrame, 0, 0, "Select EQ file")
        input2 = Input(self.topFrame, self.rightFrame, 1, 0, "Select SSH file")

        self.bottomFrame = tk.Frame(
            self.master,
        )
        self.bottomFrame.grid(row=2, column=0, sticky="w")

        # Creating Text Output
        self.outputBox = tk.Text(
            self.bottomFrame,
            width=self.entry_box_width,
            height=self.text_height,
        )
        self.outputBox.grid(
            row=2, column=0, padx=self.spacingX, pady=self.spacingY
        )

        # Create Grid Button
        self.createButton = tk.Button(
            self.rightFrame,
            text="Create Grid",
            font=self.text_font,
            width=self.button_width,
            height=self.button_height,
            bg="#00cc00",
            command=lambda: self.compute_files(
                input1.value.get(), input2.value.get()
            ),
        )
        self.createButton.grid(
            row=2,
            rowspan=1,
            column=0,
            pady=self.spacingY + 40,
            padx=self.spacingX,
        )

        # Create Plot Button
        self.plotButton = tk.Button(
            self.rightFrame,
            text="Plot Grid",
            font=self.text_font,
            width=self.button_width,
            height=self.button_height,
            bg="#99ccff",
            command=lambda: self.data_plot(),
        )
        self.plotButton.grid(
            row=3,
            rowspan=1,
            column=0,
            pady=self.spacingY,
            padx=self.spacingX,
            sticky="s",
        )

        # Create Grid Data Button
        self.plotAllButton = tk.Button(
            self.rightFrame,
            text="Show Grid Data",
            font=self.text_font,
            width=self.button_width,
            height=self.button_height,
            bg="#99ccff",
            command=lambda: self.data_print("all"),
        )
        self.plotAllButton.grid(
            row=4,
            rowspan=1,
            column=0,
            pady=self.spacingY,
            padx=self.spacingX,
            sticky="s",
        )

        # Create Detailed Data Button
        self.plotDetButton = tk.Button(
            self.rightFrame,
            text="Show Detailed Data",
            font=self.text_font,
            width=self.button_width,
            height=self.button_height,
            bg="#99ccff",
            command=lambda: self.data_print("details"),
        )
        self.plotDetButton.grid(
            row=5,
            rowspan=1,
            column=0,
            pady=self.spacingY,
            padx=self.spacingX,
            sticky="s",
        )

        self.master.mainloop()

    def compute_files(self, eq_file, ssh_file):
        """
        Computing files from GUI input with both an EQ and SSH file from the
        file browser.
        """

        psc.PSEquipment.GridData, status = main.main(eq_file, ssh_file)

        string = f"Grid created \n\
All XML-data processed = {status} \n \n\
Please select further actions with the buttons on the right: \n   \
        - Plot grid \n   \
        - Show grid data \n   \
        - Show detailed grid data."

        self.outputBox.insert(1.0, string)

    def data_plot(self):
        """
        Plot created grid
        """
        main.main_plot(psc.PSEquipment.GridData)

    def data_print(self, other):
        """
        Print output in text box
        """
        self.outputBox.delete("1.0", "end")
        if other == "details":
            eq = ["bus", "load", "switch", "shunt", "line", "trafo"]
            eq.reverse()
            for i in eq:
                string = main.main_print(psc.PSEquipment.GridData, i)
                self.outputBox.insert(1.0, string)
                self.outputBox.insert(1.0, " \n \n ")
        else:
            string = main.main_print(psc.PSEquipment.GridData, other)
            self.outputBox.insert(1.0, string)


class InputRow(GUI_prerequisite.Prerequisite):
    """
    Input button and entry box main.
    """

    def __init__(self, eframe, row, column):
        super().__init__()

        self.value = tk.StringVar()

        self.entry = tk.Entry(
            eframe,
            font=self.text_font,
            textvariable=self.value,
            width=self.entry_box_width,
        )

        self.entry.grid(
            row=row, column=column, padx=self.spacingX, pady=self.spacingY
        )


class Input(InputRow):
    """
    Subclass for input buttons.
    """

    def __init__(self, eframe, bframe, row, column, button_name):
        super().__init__(eframe, row, column)

        self.window = tk.Label()

        self.button = tk.Button(
            bframe,
            text=button_name,
            command=lambda: self.browse_file(self.value, button_name),
            font=self.text_font,
            height=self.button_height,
            width=self.button_width,
            bg="#ffcc66",
        )

        self.button.grid(
            row=row,
            column=column,
            padx=self.spacingX,
            pady=self.spacingY - 3,
            sticky=tk.N,
        )

    def browse_file(self, var, text):
        var.set(
            filedialog.askopenfilename(
                initialdir=".",
                title=text,
                filetypes=(("xml files", "*.xml"), ("all files", "*.*")),
            )
        )


class Output(InputRow):
    """
    Currently not used, but could be impemented for "save output as..."
    """

    def __init__(self, frame, row, column, button_name):
        super().__init__(frame, row, column)

        self.button = tk.Button(
            frame,
            text=button_name,
            command=lambda: self.browse_output(self.value, button_name),
            font=self.text_font,
            height=self.button_height,
            width=self.button_width,
        )

        self.button.grid(
            row=row, column=column + 1, padx=self.spacingX, pady=self.spacingY
        )
        # self.button.grid_columnconfigure(4, weight=1)

    def browse_output(self, output, text):
        output.set(
            filedialog.asksaveasfilename(
                initialdir=".",
                title=text,
                filetypes=(("xml files", "*.xml"), ("all files", "*.*")),
            )
        )


if __name__ == "__main__":
    FC = FileBrowser()
