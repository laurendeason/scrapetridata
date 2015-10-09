
# coding: utf-8

# In[75]:

from IPython import get_ipython  #This should allow exported .py file to run as python script
get_ipython().magic(u'matplotlib inline')
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


# In[76]:

allresults = pd.read_csv('./results/allresults.csv') 

athletenodes = allresults[['firstname','lastname','yearborn','racecode','Year']] 
racenodes = allresults[['firstname','lastname','yearborn','racecode','Year']] 
#athletenodes.loc[:,'athlete'] = athletenodes['firstname']+athletenodes['lastname']+athletenodes['yearborn'].astype(str)
#athletegraph_df = athletenodes.merge(athletenodes,how='inner',on=['racecode','Year']) 
racenodes.loc[:,'race'] = racenodes['racecode']+racenodes['Year'].astype(str)
racegraph_df = racenodes.merge(racenodes,how='inner',on=['firstname','lastname','yearborn']) 
racegraph_df.head()


# In[77]:

racegraph_series_wt = racegraph_df.groupby(['race_x','race_y'])['firstname'].count()
racegraph_df_wt = racegraph_series_wt.reset_index()
racegraph_df_wt.columns = ['race_x','race_y','weight']
racegraph_df_wt.head()


# In[78]:

nodecolordict = {'CH': 'green',
              'DC': 'blue',
              'NY': 'red'}

racegraph = nx.from_pandas_dataframe(racegraph_df_wt, 'race_x', 'race_y', edge_attr=True)
node_color = [nodecolordict[node[0:2]] for node in racegraph]
node_size = [racegraph_df_wt.loc[(racegraph_df_wt['race_x']==node) & (racegraph_df_wt['race_y']==node)]['weight'].values[0] for node in racegraph]

#pos = nx.spring_layout(racegraph)
nx.draw(racegraph, node_color=node_color, node_size=node_size, with_labels=True)

#nx.draw_networkx_labels(racegraph,pos)
plt.show()


# In[79]:

nx.degree(racegraph)

