#Basic
df.head(3)
df.tail(4)
df.describe()
df.value_counts()     
df.info()
df[(df['a']>50) & (df['b']<70)]
df[(df['a']>50) | (df['b']<70)]
emp['IIDD'] = emp['IIDD'].apply(lambda a:a+1)
CONDITION
df['col1'] = np.where(df['col2']>18,'Eligible','not eligible')

#Multi indexing
outside=['G1','G1','G1','G1','G2','G2','G2','G2']
inside=[1,1,2,2,1,1,2,2]
ins=[1,2,3,4,5,6,7,8]
hier_index=list(zip(outside,inside,ins))
print(hier_index)
hier_index=pd.MultiIndex.from_tuples(hier_index)
df=pd.DataFrame(randn(2,8),['a','b'],hier_index)
print(df)

#Missing value
d = {'A':[1,2,np.nan],'B':[5,np.nan,np.nan],'C':[1,2,3]}
df = pd.DataFrame(d)
print(df)
print(df.dropna())
print(df.dropna(axis=1))
print(df.dropna(thresh=2))
print(df.fillna(value='FILL VALUE'))
print(df['A'].fillna(df['A'].mean()))

# concate
df3 = pd.concat([df1,df2],axis=0)     #column wise concadination
df3 = pd.concat([df1,df2],axis=1)     #row wise concadination

#concatenat
df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3'],
                        'C': ['C0', 'C1', 'C2', 'C3'],
                        'D': ['D0', 'D1', 'D2', 'D3']},
                        index=[0, 1, 2, 3])
df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'],
                        'B': ['B4', 'B5', 'B6', 'B7'],
                        'C': ['C4', 'C5', 'C6', 'C7'],
                        'D': ['D4', 'D5', 'D6', 'D7']},
                         index=[4, 5, 6, 7])
df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'],
                        'B': ['B8', 'B9', 'B10', 'B11'],
                        'C': ['C8', 'C9', 'C10', 'C11'],
                        'D': ['D8', 'D9', 'D10', 'D11']},
                        index=[8, 9, 10, 11])
print(pd.concat([df1,df2,df3],axis=0))
print(pd.concat([df1,df2,df3],axis=1))

#Merging

left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
print(left)
print(right)
print(pd.concat([left,right],axis=1))
print(pd.merge(left,right))

left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                     'key2': ['K0', 'K1', 'K0', 'K1'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                      'key2': ['K0', 'K0', 'K0', 'K0'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
print(left)
print(right)
print(pd.concat([left,right],axis=1))
print(pd.merge(left,right))
print(pd.merge(left,right,on='key1'))

#Joining
left = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2']},
                      index=['K0', 'K1', 'K2'])
right = pd.DataFrame({'C': ['C0', 'C2', 'C3'],
                    'D': ['D0', 'D2', 'D3']},
                      index=['K0', 'K2', 'K3'])
print(right.join(left))
print(right.join(left,how='outer'))

# df to list
dfa = df.values     # it convert df into array
print(dfa)
list(map(lambda a:list(a),list(dfa)))

#indexing
df1.loc[[111],['a','d']]
df1.iloc[:,:]
df.reset_index()
ddff = df.reindex([22,33,111,44])
ddff.index = [11111,22222,333333,444444]
df.set_index('index_name')
ddff.set_axis([1,2,3,4,5],axis=1)        #set column
ddff.set_axis([11,12,13,14,15],axis=0)    #set index

#operations
df =pd.DataFrame({'Col1':[1,2,3,4],
       'Col2':[444,555,666,444],
       'Col3':['abc','def','ghi','xyz']})
print(df.head())
print(df['Col2'].unique())
print(len(df['Col2'].unique()))    # or df['Col2'].nunique()
print(df['Col2'].value_counts())
print(df.drop('Col1',axis=1))
print(df.columns)
print(df.index)
print(df.sort_values('Col2'))  # or df.sort_values(by='Col2')
print(df.isnull())
print(df.pivot_table(values='D',index=['A','B'],columns=['C']))


