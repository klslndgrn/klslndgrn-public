import matplotlib.pyplot as plt


# Example plot function
def update_plot(data):
    plt.clf()  # Clear the current plot
    # Plot data
    plt.plot(data["x"], data["y"])
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("24-hour Plot")
    plt.grid(True)
    plt.draw()  # Redraw the plot
    plt.pause(0.1)  # Pause to allow the plot to update
