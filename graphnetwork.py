
# coding: utf-8

# In[2]:

from IPython import get_ipython  #This should allow exported .py file to run as python script
get_ipython().magic(u'matplotlib inline')
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


# In[4]:

allresults = pd.read_csv('./results/allresults.csv') 

athletenodes = allresults[['firstname','lastname','yearborn','racecode','Year']] 
racenodes = allresults[['firstname','lastname','yearborn','racecode','Year']] 
#athletenodes.loc[:,'athlete'] = athletenodes['firstname']+athletenodes['lastname']+athletenodes['yearborn'].astype(str)
#athletegraph_df = athletenodes.merge(athletenodes,how='inner',on=['racecode','Year']) 
racegraph_df = racenodes.merge(racenodes,how='inner',on=['firstname','lastname','yearborn']) 
racegraph_df.head()


# In[19]:

racegraph_df.loc[(racegraph_df['racecode_x']=='CH_2004') & (racegraph_df['racecode_y']=='DC_2011')]


# In[11]:

racegraph_series_wt = racegraph_df.groupby(['racecode_x','racecode_y'])['firstname'].count()
racegraph_df_wt = racegraph_series_wt.reset_index()
racegraph_df_wt.columns = ['racecode_x','racecode_y','weight']
racegraph_df_wt[:20]


# In[22]:

nodecolordict = {'CH': 'green',
              'DC': 'blue',
              'NY': 'red'}

racegraph = nx.from_pandas_dataframe(racegraph_df_wt, 'racecode_x', 'racecode_y', edge_attr=True)
node_color = [nodecolordict[node[0:2]] for node in racegraph]
node_size = [racegraph_df_wt.loc[(racegraph_df_wt['racecode_x']==node) & (racegraph_df_wt['racecode_y']==node)]['weight'].values[0] for node in racegraph]

#pos = nx.spring_layout(racegraph)
nx.draw(racegraph, node_color=node_color, node_size=node_size, with_labels=True)

#nx.draw_networkx_labels(racegraph,pos)
plt.show()


# In[23]:

nx.edges(racegraph)


# In[26]:

nx.degree(racegraph, weight='weight')  #without including weight here, sees to count even missing edges


# In[ ]:



