import pandas as pd
from scipy import stats
import scipy.stats as scp

df = pd.read_csv(r'C:\Users\annan\MinCode\Python\2023\vgsalesFiltered.csv')
df2=df.loc[df['Genre']=='Shooter']
df3=df.loc[df["Genre"]=="action"]
years = [1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2020]

result = scp.kruskal(shoot_action.loc[1980].values.tolist(),shoot_action.loc[1981].values.tolist(),shoot_action.loc[1982].values.tolist(),shoot_action.loc[1983].values.tolist(),shoot_action.loc[1984].values.tolist(),shoot_action.loc[1985].values.tolist(),shoot_action.loc[1986].values.tolist(),shoot_action.loc[1987].values.tolist(),shoot_action.loc[1988].values.tolist(),shoot_action.loc[1989].values.tolist(), shoot_action.loc[1990].values.tolist(), shoot_action.loc[1991].values.tolist(), shoot_action.loc[1992].values.tolist(), shoot_action.loc[1993].values.tolist(), shoot_action.loc[1994].values.tolist(), shoot_action.loc[1995].values.tolist(), shoot_action.loc[1996].values.tolist(), shoot_action.loc[1997].values.tolist(), shoot_action.loc[1998].values.tolist(), shoot_action.loc[1999].values.tolist(), shoot_action.loc[2000].values.tolist(), shoot_action.loc[2001].values.tolist(), shoot_action.loc[2002].values.tolist(), shoot_action.loc[2003].values.tolist(), shoot_action.loc[2004].values.tolist(), shoot_action.loc[2005].values.tolist(), shoot_action.loc[2006].values.tolist(), shoot_action.loc[2007].values.tolist(), shoot_action.loc[2008].values.tolist(), shoot_action.loc[2009].values.tolist(), shoot_action.loc[2010].values.tolist(),shoot_action.loc[2011].values.tolist(),shoot_action.loc[2012].values.tolist(),shoot_action.loc[2013].values.tolist(),shoot_action.loc[2014].values.tolist(),shoot_action.loc[2015].values.tolist(),shoot_action.loc[2016].values.tolist(),shoot_action.loc[2017].values.tolist())
result
