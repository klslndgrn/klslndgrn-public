import main
import kmc_data as md
import tkinter as tk
import GUI_prerequisite


class GUI(GUI_prerequisite.Prerequisite):
    """
    Tkinter file browser.
    """
    def __init__(self):
        GUI_prerequisite.Prerequisite.__init__(self)

        self.master = tk.Tk()
        self.master.title("kMC and kNN for a 9-bus grid")

        self.rightFrame = tk.Frame(self.master)
        self.rightFrame.grid(row=0,
                             rowspan=3,
                             column=1,
                             sticky="e")

        self.leftFrame = tk.Frame(self.master,)
        self.leftFrame.grid(row=0,
                            column=0,
                            sticky="w")

        # Creating Text Output
        self.outputBox = tk.Text(self.leftFrame,
                                 width=self.entry_box_width,
                                 height=self.text_height)
        self.outputBox.grid(row=2,
                            column=0,
                            padx=self.spacingX,
                            pady=self.spacingY)

        entry_str = '\nThis is a GUI for k-Means Clustering (kMC) and \
k-Nearest Neigbor.\n\n\
    - To run both kMC and kNN press "Run kMC and kNN" \n\n\
    - To run kMC press "Run kMC" \n\
    - To run kNN press "Run kMC" \n\n\
    - To show kMC results press "Show kMC results" \n\
    - To show kNN results press "Show kNN results" \n\n\
    - To show analyzed grid press "Show Grid" \n\n\
WARNING:\n\
Running kMC takes about 5-15 minutes! \n\
Pressing any other button will make the program unresponsive.\n\
Use "show results" buttons to show results! \n\n\
Progress for each program can be seen in the terminal.'
        self.outputBox.insert(1.0, entry_str)

        # Create "Run kMC and kNN" button -------------------------------------
        self.createButton = tk.Button(self.rightFrame,
                                      text="Run kMC and kNN",
                                      font=self.text_font,
                                      width=self.button_width,
                                      height=self.button_height,
                                      bg='#ff8000',
                                      command=lambda:
                                          self.run_kmc_knn())
        self.createButton.grid(row=0,
                               rowspan=1,
                               column=0,
                               pady=self.spacingY+40,
                               padx=self.spacingX)

        # Create "Run kMC" button ---------------------------------------------
        self.createButton = tk.Button(self.rightFrame,
                                      text="Run kMC",
                                      font=self.text_font,
                                      width=self.button_width,
                                      height=self.button_height,
                                      bg='#20baab',
                                      command=lambda:
                                          self.run_kmc())
        self.createButton.grid(row=1,
                               rowspan=1,
                               column=0,
                               pady=self.spacingY,
                               padx=self.spacingX)

        # Create "Run kNN" button ---------------------------------------------
        self.createButton = tk.Button(self.rightFrame,
                                      text="Run kNN",
                                      font=self.text_font,
                                      width=self.button_width,
                                      height=self.button_height,
                                      bg='#49ba20',
                                      command=lambda:
                                          self.run_knn())
        self.createButton.grid(row=3,
                               rowspan=1,
                               column=0,
                               pady=self.spacingY,
                               padx=self.spacingX)

        # Create "Show kMC results" button ------------------------------------
        self.Clustering = tk.Button(self.rightFrame,
                                    text="Show kMC results",
                                    font=self.text_font,
                                    width=self.button_width,
                                    height=self.button_height,
                                    bg='#20baab',
                                    command=lambda:
                                        self.kmc_results())
        self.Clustering.grid(row=2,
                             rowspan=1,
                             column=0,
                             pady=self.spacingY,
                             padx=self.spacingX,
                             sticky="s")

        # Create "Show kNN results" button ------------------------------------
        self.plotDetButton = tk.Button(self.rightFrame,
                                       text="Show kNN results",
                                       font=self.text_font,
                                       width=self.button_width,
                                       height=self.button_height,
                                       bg='#49ba20',
                                       command=lambda:
                                           self.knn_results())
        self.plotDetButton.grid(row=4,
                                rowspan=1,
                                column=0,
                                pady=self.spacingY,
                                padx=self.spacingX,
                                sticky="s")

        # Create "Show grid" button -------------------------------------------
        self.plotButton = tk.Button(self.rightFrame,
                                    text="Show Grid",
                                    font=self.text_font,
                                    width=self.button_width,
                                    height=self.button_height,
                                    bg='#99ccff',
                                    command=lambda:
                                        self.plot_grid())
        self.plotButton.grid(row=5,
                             rowspan=1,
                             column=0,
                             pady=self.spacingY+20,
                             padx=self.spacingX,
                             sticky="s")

        self.master.mainloop()

    def run_kmc_knn(self):
        '''
        Run both kMC and kNN from GUI.
        '''

        kNN, Precision, cluster_score, main_cluster = main.main_run_all()
        string, cluster_scores = main.main_kmc_results()
        self.outputBox.delete("1.0", "end")
        self.outputBox.insert(1.0, string)
        md.plot_elbow(cluster_scores)

        string2 = f'\n---- k-Nearest Neigbor results from program: ----\n\
\nBest k-number is {kNN} which gives {100*Precision:.2f} accuracy for \
classifications.\n'

        self.outputBox.delete("1.0", "end")
        self.outputBox.insert(1.0, string2)

    def print_kmc_knn(self):
        pass

    def run_kmc(self):
        '''
        Run kMC from GUI.
        '''
        main.main_run_kmc()

        string, cluster_scores = main.main_kmc_results()
        string1 = '\n---- k-Means Clustering results from program: ----\n'
        stringx = string1 + string
        self.outputBox.delete("1.0", "end")
        self.outputBox.insert(1.0, stringx)
        md.plot_elbow(cluster_scores)

    def run_knn(self):
        '''
        Run kNN from GUI.
        '''
        kNN, Precision = main.main_run_knn()

        string = f'\n---- k-Nearest Neigbor results from program: ----\n\
\nBest k-number is {kNN} which gives {100*Precision:.2f} accuracy for \
classifications.\n'
        self.outputBox.delete("1.0", "end")
        self.outputBox.insert(1.0, string)

    def plot_grid(self):
        '''
        Plot created grid
        '''
        main.show_grid()

    def kmc_results(self):
        '''
        Print output in text box
        '''
        string, cluster_scores = main.main_kmc_results()
        string1 = '\n---- k-Means Clustering results from file: ----\n'
        stringx = string1 + string
        self.outputBox.delete("1.0", "end")
        self.outputBox.insert(1.0, stringx)
        md.plot_elbow(cluster_scores)

    def knn_results(self):
        '''
        Print output in text box
        '''
        kNN, Precision, datapoints = main.main_knn_results()

        string = f'\n---- k-Nearest Neigbor results from file: ----\n\
\nBest k-number is {kNN} which gives {100*Precision:.2f} accuracy for \
classifications.\n'

        self.outputBox.delete("1.0", "end")
        self.outputBox.insert(1.0, string)


class InputRow(GUI_prerequisite.Prerequisite):
    '''
    Input button and entry box main.
    '''
    def __init__(self, eframe, row, column):
        super().__init__()

        self.value = tk.StringVar()

        self.entry = tk.Entry(eframe,
                              font=self.text_font,
                              textvariable=self.value,
                              width=self.entry_box_width)

        self.entry.grid(row=row,
                        column=column,
                        padx=self.spacingX,
                        pady=self.spacingY)


if __name__ == "__main__":
    FC = GUI()
