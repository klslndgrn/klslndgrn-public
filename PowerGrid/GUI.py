import tkinter as tk
import GUI_prerequisite
from tkinter import filedialog
import main


class FileBrowser(GUI_prerequisite.Prerequisite):
    """
    ipb1/2 Input browser button
    opb output browse button
    """
    def __init__(self):
        GUI_prerequisite.Prerequisite.__init__(self)

        self.master = tk.Tk()

        self.master.title("File Browser")

        self.topFrame = tk.Frame(self.master)

        self.topFrame.grid()

        Ipb1 = Input(self.topFrame, 0, 0, "EQ")
        Ipb2 = Input(self.topFrame, 1, 0, "SSH")
        Opb2 = Output(self.topFrame, 2, 0, "Output")

        self.bottom_frame = tk.Frame(self.master)
        self.bottom_frame.grid(row=2, sticky="w")
        self.output_box = tk.Text(self.bottom_frame)
        self.output_box.grid(row=2, column=0, padx=self.spacingX,
                             pady=self.spacingY)

        self.go_button = tk.Button(self.bottom_frame, text="Create Grid",
                                   font=self.text_font,
                                   width=self.button_width,
                                   height=self.button_height,
                                   command=lambda: self.compute_files())
        self.go_button.grid(row=2, column=1, pady=self.spacingY,
                            padx=self.spacingX)

        self.master.mainloop()

    def compute_files(self):
        # Call on main function
        # Use return value as input for text box
        # Där Ipb1/2.value = patht to file
        # och Opb1.value = path där du vill spara en fil
        # och för output i Text box
        # self.output_box.insert("output från dit arbete")
        main.main()
        pass


class InputRow(GUI_prerequisite.Prerequisite):

    def __init__(self, frame, row, column):
        super().__init__()
        self.value = tk.StringVar()

        self.entry = tk.Entry(frame, font=self.text_font,
                              textvariable=self.value,
                              width=self.entry_box_width)

        self.entry.grid(row=row, column=column, padx=self.spacingX,
                        pady=self.spacingY)


class Output(InputRow):
    def __init__(self, frame, row, column, button_name):
        super().__init__(frame, row, column)

        self.button = tk.Button(frame, text=button_name, command=lambda:
                                self.browse_output(self.value, button_name),
                                font=self.text_font,
                                height=self.button_height,
                                width=self.button_width)

        self.button.grid(row=row, column=column+1, padx=self.spacingX,
                         pady=self.spacingY)

    def browse_output(self, output, text):
        output.set(filedialog.asksaveasfilename(initialdir=".",
                   title=text, filetypes=(("txt files", "*.txt"),
                                          ("all files", "*.*"))))


class Input(InputRow):
    def __init__(self, frame, row, column, button_name):
        super().__init__(frame, row, column)

        self.button = tk.Button(frame, text=button_name, command=lambda:
                                self.browse_file(self.value, button_name),
                                font=self.text_font,
                                height=self.button_height,
                                width=self.button_width)

        self.button.grid(row=row, column=column+1, padx=self.spacingX,
                         pady=self.spacingY)

    def browse_file(self, var, text):
        var.set(filedialog.askopenfilename(initialdir=".", title=text,
                filetypes=(("txt files", "*.txt"), ("all files", "*.*"))))


if __name__ == "__main__":
    FC = FileBrowser()
