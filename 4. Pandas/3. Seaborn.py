import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset('tips')
a = tips.head()
print(a)
sns.histplot(tips['total_bill'])
sns.histplot(tips['total_bill'],kde=False,bins=30)
sns.jointplot(x='total_bill',y='tip',data=tips,kind='scatter')
sns.jointplot(x='total_bill',y='tip',data=tips,kind='hex')
sns.jointplot(x='total_bill',y='tip',data=tips,kind='reg')
sns.pairplot(tips)
sns.pairplot(tips,hue='sex',palette='coolwarm')
sns.rugplot(tips['total_bill'])

# Don't worry about understanding this code!
# It's just for the diagram below
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Create dataset
dataset = np.random.randn(25)

# Create another rugplot
sns.rugplot(dataset);

# Set up the x-axis for the plot
x_min = dataset.min() - 2
x_max = dataset.max() + 2

# 100 equally spaced points from x_min to x_max
x_axis = np.linspace(x_min, x_max, 100)

# Set up the bandwidth, for info on this:
url = 'http://en.wikipedia.org/wiki/Kernel_density_estimation#Practical_estimation_of_the_bandwidth'

bandwidth = ((4 * dataset.std() ** 5) / (3 * len(dataset))) ** .2

# Create an empty kernel list
kernel_list = []

# Plot each basis function
for data_point in dataset:
    # Create a kernel for each point and append to list
    kernel = stats.norm(data_point, bandwidth).pdf(x_axis)
    kernel_list.append(kernel)

    # Scale for plotting
    kernel = kernel / kernel.max()
    kernel = kernel * .4
    plt.plot(x_axis, kernel, color='grey', alpha=0.5)

plt.ylim(0, 1)


# To get the kde plot we can sum these basis functions.

# Plot the sum of the basis function
sum_of_kde = np.sum(kernel_list,axis=0)

# Plot figure
fig = plt.plot(x_axis,sum_of_kde,color='indianred')

# Add the initial rugplot
sns.rugplot(dataset,c = 'indianred')

# Get rid of y-tick marks
plt.yticks([])

# Set title
plt.suptitle("Sum of the Basis Functions")


sns.kdeplot(tips['total_bill'])
sns.rugplot(tips['total_bill'])


sns.kdeplot(tips['tip'])
sns.rugplot(tips['tip'])

plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
tips = sns.load_dataset('tips')
a = tips.head()
print(a)
sns.barplot(x='sex',y='total_bill',data=tips)
import numpy as np
sns.barplot(x='sex',y='total_bill',data=tips,estimator=np.std)
plt.show()
sns.countplot(x='sex',data=tips)
plt.show()
sns.boxplot(x="day", y="total_bill", data=tips)
plt.show()
sns.violinplot(x='day',y='total_bill',data=tips)
plt.show()
sns.stripplot(x='day',y='total_bill',data=tips)
plt.show()
sns.swarmplot(x='day',y='total_bill',data=tips)
plt.show()
sns.violinplot(x='day', y='total_bill', data=tips,hue='smoker',palette='rainbow')
sns.swarmplot(x='day', y='total_bill', data=tips,color='black')
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns

tips = sns.load_dataset('tips')
flights = sns.load_dataset('flights')
print(tips.head())
print(flights.head())
tc = tips.corr()
print(tc)
sns.heatmap(tc)
plt.show()
fp = flights.pivot_table(index='month',columns='year',values='passengers')
print(fp)
sns.heatmap(fp)
plt.show()
sns.clustermap(fp)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

iris = sns.load_dataset('iris')
a = iris.head()
print(a)
print(iris['species'].unique())
sns.pairplot(iris)
plt.show()
sns.PairGrid(iris)
plt.show()
g = sns.PairGrid(iris)
g.map(plt.scatter)
plt.show()
#g = sns.PairGrid(iris)
#g.map_diag(sns.distplot())
#g.map_upper(plt.scatter)
#g.map_lower(sns.kdeplot())
#plt.show()

tips = sns.load_dataset('tips')
b = tips.head()
print(b)
#g = sns.FacetGrid(data='tips',col='time',row='smoker')
#plt.show()
#g.map(sns.distplot,'total_bill')
#g.map(plt.scatter,'total_bill','tip')

sns.lmplot(x='total_bill',y='tip',data=tips)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
tips = sns.load_dataset('tips')
print(tips.head())

# plt.figure(figsize=(12,3))
sns.set_style('whitegrid')
sns.countplot(x='sex',data=tips)
# sns.despine()
sns.set_context('notebook',font_scale=1.5)
plt.tight_layout()
plt.show()


sns.lmplot(x='total_bill',y='tip',data=tips,hue='sex')
plt.show()
