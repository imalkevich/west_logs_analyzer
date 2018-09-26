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
            counts = [count for (_, count) in errors]
            texts.append('group_{} ({})'.format(idx, ' '.join([str(c) for c in counts])))
            bars.append(plt.bar(ind, counts, width, bottom=bottom))
            bottom = list(map(add, bottom, counts))
            
        plt.ylabel('Errors')
        plt.title('Errors by date')
        plt.xticks(ind, [day.strftime('%m/%d/%Y') for day in self.days])
        scale = 10 ** max(1, len(str(max(bottom)))-2)
        plt.yticks(range(0, max(bottom) + scale, scale))
        
        art = []
        lgd = plt.legend([b[0] for b in bars], texts, loc=9, bbox_to_anchor=(0.5, -0.1), ncol=10)
        art.append(lgd)

        plt.savefig(path, additional_artists=art, bbox_inches="tight")

    def save_chart_to_file(self, path):
        pass
