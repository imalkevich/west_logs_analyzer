import matplotlib.pyplot as plt

from operator import add

class StackedBarChartBuilder(object):
    def __init__(self, days, results):
        self.days = days
        self.results = results
        self.chart = None

    def build_chart(self, path):
        ind = range(len(self.days))
        width = 0.35
        bars = []
        texts = []
        bottom = [0 for _ in ind]

        for (idx, _, errors) in self.results:
            texts.append('group_{}'.format(idx))
            counts = [count for (_, count) in errors]
            bars.append(plt.bar(ind, counts, width, bottom=bottom))
            bottom = list(map(add, bottom, counts))
            
        plt.ylabel('Errors')
        plt.title('Errors by date')
        plt.xticks(ind, [day.strftime('%m/%d/%Y') for day in self.days])
        plt.yticks(range(0, max(bottom) + 10, 10))
        plt.legend([b[0] for b in bars], texts)

        plt.savefig(path)

    def save_chart_to_file(self, path):
        pass
