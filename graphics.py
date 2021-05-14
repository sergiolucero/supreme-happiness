import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
plt.autoscale(enable=True, axis='x', tight=True)
sns.set_style('darkgrid')
#################
def label_barplot(ax):
    for patch in ax.patches:
        xy = patch.get_width()-2, patch._y0+0.44
        texto = '%.2f' %patch.get_width()
    #print(xy)
        ax.annotate(texto, xy, color='blue', fontsize=16, weight='bold')
###
