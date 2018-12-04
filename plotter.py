import matplotlib.pyplot as plt


def hist_plot(values, title=None, xlb=None, ylb=None):
    '''
    xlb -- label for x-axis
    ylb -- label for y-axis
    '''
    plt.hist(values, edgecolor='black', linewidth=0.7, bins=30)
    if title:
        plt.title(title)
    if xlb:
        plt.xlabel(xlb)
    if ylb:
        plt.ylabel(ylb)

    plt.xticks(rotation='vertical')
    plt.grid(axis='y', alpha=1)
    plt.show()
