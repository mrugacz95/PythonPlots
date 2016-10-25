import csv
from matplotlib.pyplot import *
from numpy import *


class Plot:
    data_list = []

    def __init__(self, fileName, colorAndShape, label, marker):
        self.marker = marker
        self.label = label
        self.averages = []
        self.fileName = fileName
        self.colorAndShape = colorAndShape

    def calculateData(self):
        with open(self.fileName + '.csv', 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='\n')
            self.data_list = list(reader)
            self.data_list.pop(0)
            for data in self.data_list:
                data.pop(0)  # generation
                data.pop(0)  # afford
                data = list(map(lambda x: float(x) * 100, data))
                av = average(array(data).astype(float))
                self.averages.append(av)
                if len(self.averages) > 200:
                    break

    def drawOnPlot(self):
        plot(range(0, len(self.averages)), self.averages, self.colorAndShape, marker=self.marker, markevery=30,
             label=self.label)

    def getData(self):
        return np.array(self.data_list[-1]).astype(float)


def main():
    files = {
        Plot("rsel", "b", "1-Evol-RS", 'o'),
        Plot("cel-rs", "g", "1-Coev-RS", "v"),
        Plot("2cel-rs", "r", "2-Coev-RS", 'D'),
        Plot("cel", "k", "1-Coev", 's'),
        Plot("2cel", 'm', "2-Coev", 'd')
    }

    figure(figsize=(15, 9))
    subplot(121)
    for file in files:
        file.calculateData()
        file.drawOnPlot()
    legend(loc=0, borderaxespad=0.5)
    xlabel("Rozegranych gier x 1000")
    ylabel("Odsetek wygranych gier [%]")
    grid()
    subplot(122)
    dataBox = []
    labels = []
    for file in files:
        dataBox.append(file.getData())
        labels.append(file.label)
    dataBox.sort(key=lambda x: median(x), reverse=True)
    boxplot(dataBox, notch=True, showmeans=True)
    xticks(range(1, 6), labels, rotation=45)
    grid()
    savefig("myplot.pdf")
    show()


if __name__ == "__main__":
    main()
