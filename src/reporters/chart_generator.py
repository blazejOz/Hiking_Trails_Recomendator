from matplotlib import pyplot as plt


class ChartGenerator:
    @staticmethod
    def bar_chart(routes, filename):
        lengths = [r.length_km for r in routes]
        names = [r.name for r in routes]
        plt.figure(figsize=(8, 4))
        plt.bar(names, lengths, color='skyblue')
        plt.xticks(rotation=45, ha='right')
        plt.title('Histogram długości tras')
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    @staticmethod
    def pie_chart(routes, filename):
        categories = [r.terrain_type for r in routes]
        labels = list(set(categories))
        sizes = [categories.count(l) for l in labels]
        plt.figure(figsize=(5, 5))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Wykres kołowy kategorii tras')
        plt.savefig(filename)
        plt.close()