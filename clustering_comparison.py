import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st
import plotly.express as px 
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

### Config
st.set_page_config(
    page_title="Clustering analysis",
    layout="centered"
)

### Data upload
@st.cache
def load_data():
    db = pd.read_csv("clustering_result.csv")
    db['KMeans_clusters'] = db['KMeans_clusters'].astype(str)
    db['BisectingKMeans_clusters'] = db['BisectingKMeans_clusters'].astype(str)
    db['KModes_clusters'] = db['KModes_clusters'].astype(str)
    db['DBSCAN_clusters'] = db['DBSCAN_clusters'].astype(str)
    return db

db = load_data()



### Setting personalised palette
palette = ['#00202e', '#003f5c',  '#2c4875',  '#8a508f',  '#bc5090',  '#ff6361',  '#ff8531', ' #ffa600',  '#ffd380', '#A0A0A0']

pio.templates["palette"] = go.layout.Template(
    layout = {
        'title':
            {'font': {'color': '#0F0429'}
            },
        'font': {'color': '#0F0429'},
        'colorway': palette,
    }
)
pio.templates.default = "palette"

#insert title
st.markdown("<h1 style='text-align: center'>Network clustering analysis</h1>", unsafe_allow_html=True)

#insert explanation
st.markdown(""" Visualization of the clustering results of clustering K-Means, Bisecting K-Means, and K-Modes on the "IP Network Traffic Flows Labeled with 75 Apps" dataset from Kaggle. 
The analysis is based on the work of Aouedi et al. and revisits and expands their clustering Proof Of Concept. 
To visualize data about one cluster only, double click on the cluster in the legend.
""")

###Graph 1####################################################################################################
st.subheader("Cluster sizes")

labels = ["Cluster 0", "Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4", "Cluster 5", "Cluster 6", "Outliers"]

# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(rows=1, cols=4, 
specs=[[{'type':'domain'}, {'type':'domain'},{'type':'domain'},{'type':'domain'}]],
subplot_titles=("KMeans", "Bisecting KMeans", "KModes", "DBSCAN"))

fig.add_trace(go.Pie(
    labels=labels, 
    values=db["KMeans_clusters"].value_counts(sort=False).sort_index().tolist(), 
    name="KMeans"),
    1, 1)

fig.add_trace(go.Pie(
    labels=labels, 
    values=db["BisectingKMeans_clusters"].value_counts(sort=False).sort_index().tolist(), 
    name="Bisecting KMeans"),
    1, 2)

fig.add_trace(go.Pie(
    labels=labels, 
    values=db["KModes_clusters"].value_counts(sort=False).sort_index().tolist(), 
    name="KModes clusters"),
    1, 3)

fig.add_trace(go.Pie(
    labels=labels, 
    values=db["DBSCAN_clusters"].value_counts(sort=False).sort_index().tolist(), 
    name="DBSCAN clusters"),
    1, 4)

st.plotly_chart(fig, use_container_width=True)

##############################################################################################################
clusters_order=["0","1","2","3", "4", "5", "6", "outlier"]
clusters_palette = {"0":palette[0], "1":palette[1], "2":palette[2], "3":palette[3], "4":palette[4],"5":palette[5], "6":palette[6], "outlier": palette[9]}
###Graph 2####################################################################################################
st.subheader("Applications")

# create top application list
db_topapps = db.groupby(["ProtocolName"]).size().to_frame().sort_values([0], ascending = False).head(13).reset_index()
top_apps = db_topapps["ProtocolName"].tolist()

histogram_data = db.loc[db.ProtocolName.isin(top_apps)]

#K-Means

fig = px.histogram(db.loc[db.ProtocolName.isin(top_apps)], y="ProtocolName",color="KMeans_clusters",
                   orientation="h", barmode="group", 
                   category_orders={"ProtocolName":top_apps,
                                    "KMeans_clusters":clusters_order
                                   },
                   color_discrete_map=clusters_palette,
                   labels={
                    "ProtocolName": "Applications"},
                    title='K-Means'
                    )

fig.update_xaxes(title_text="Number of flows")
fig.update_yaxes(title_text="")
fig.update_layout(legend={'title_text':''})

st.plotly_chart(fig, use_container_width=True)


#Bisecting K-Means

fig = px.histogram(db.loc[db.ProtocolName.isin(top_apps)], y="ProtocolName",color="BisectingKMeans_clusters",
                   orientation="h", barmode="group", 
                   category_orders={"ProtocolName":top_apps,
                                    "BisectingKMeans_clusters":clusters_order
                                   },
                   color_discrete_map=clusters_palette,
                   labels={
                     "ProtocolName": "Applications"
                     },
                     title='Bisecting K-Means'
                     )

fig.update_xaxes(title_text="Number of flows")
fig.update_yaxes(title_text="")
fig.update_layout(legend={'title_text':''})

st.plotly_chart(fig, use_container_width=True)

#K-Modes

fig = px.histogram(db.loc[db.ProtocolName.isin(top_apps)], y="ProtocolName",color="KModes_clusters",
                   orientation="h", barmode="group", 
                   category_orders={"ProtocolName":top_apps,
                                    "KModes_clusters":clusters_order
                                   },
                   color_discrete_map=clusters_palette,                   
                   labels={
                    "ProtocolName": "Applications"},
                    title="K-Modes"
                    )

fig.update_xaxes(title_text="Number of flows")
fig.update_yaxes(title_text="")
fig.update_layout(legend={'title_text':''})

st.plotly_chart(fig, use_container_width=True)

#DBSCAN

fig = px.histogram(db.loc[db.ProtocolName.isin(top_apps)], y="ProtocolName",color="DBSCAN_clusters",
                   orientation="h", barmode="group", 
                   category_orders={"ProtocolName":top_apps,
                                    "DBSCAN_clusters":clusters_order
                                   },
                   color_discrete_map=clusters_palette,                   
                   labels={
                    "ProtocolName": "Applications"},
                    title="DBSCAN"
                    )

fig.update_xaxes(title_text="Number of flows")
fig.update_yaxes(title_text="")
fig.update_layout(legend={'title_text':''})

st.plotly_chart(fig, use_container_width=True)

###Graph 3####################################################################################################
st.subheader("Destination Ports")

ports_order=["3128", "443", "80", "0", "other"]
#KMeans
fig = px.histogram(db, x="Destination.Port_class",color="KMeans_clusters", 
                   labels={
                     "Destination.Port_class": "Destination Port Number"
                   },
                   category_orders={"Destination.Port_class":ports_order,
                                    "KMeans_clusters":clusters_order
                                   },
                   color_discrete_map=clusters_palette,
                   title="K-Means"
                  )

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
fig.update_layout(xaxis = {'type' : 'category'})

st.plotly_chart(fig, use_container_width=True)

#Bisecting KMeans
fig = px.histogram(db, x="Destination.Port_class",color="BisectingKMeans_clusters", 
                   labels={
                     "Destination.Port_class": "Destination Port Number"
                   },
                   category_orders={"Destination.Port_class":ports_order,
                                    "BisectingKMeans_clusters":clusters_order
                                   },
                   color_discrete_map=clusters_palette,
                   title="Bisecting K-Means"
                  )

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
fig.update_layout(xaxis = {'type' : 'category'})

st.plotly_chart(fig, use_container_width=True)

#KModes
fig = px.histogram(db, x="Destination.Port_class",color="KModes_clusters", 
                   labels={
                     "Destination.Port_class": "Destination Port Number"
                   },
                   category_orders={"Destination.Port_class":ports_order,
                                    "KModes_clusters":clusters_order
                                   },
                   color_discrete_map=clusters_palette,
                   title="K-Modes"
                  )

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
fig.update_layout(xaxis = {'type' : 'category'})

st.plotly_chart(fig, use_container_width=True)

#DBSCAN
fig = px.histogram(db, x="Destination.Port_class",color="DBSCAN_clusters", 
                   labels={
                     "Destination.Port_class": "Destination Port Number"
                   },
                   category_orders={"Destination.Port_class":ports_order,
                                    "DBSCAN_clusters":clusters_order
                                   },
                   color_discrete_map=clusters_palette,
                   title="DBSCAN"
                  )

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
fig.update_layout(xaxis = {'type' : 'category'})

st.plotly_chart(fig, use_container_width=True)

###Graph 4####################################################################################################

st.subheader("Time distribution")
#create column with date and time of day info

timeslots_order=[ "26/04_morning",
                "26/04_afternoon", 
                "27/04_morning", 
                "27/04_afternoon", 
                "28/04_morning", 
                "28/04_afternoon", 
                "09/05_morning", 
                "09/05_afternoon", 
                "11/05_morning", 
                "11/05_afternoon", 
                "15/05_morning", 
                "15/05_afternoon"]

#K-Means

fig = px.density_heatmap(db, x="Timeslot", y="KMeans_clusters",  text_auto=True,
                        category_orders={"Timeslot":timeslots_order,
                                         "KMeans_clusters":clusters_order},
                         color_continuous_scale='YlGn',
                         title="K-Means"
                        )

fig.update_xaxes(title_text="")
fig.update_yaxes(title_text="Cluster")

st.plotly_chart(fig, use_container_width=True)

#Bisecting K-Means

fig = px.density_heatmap(db, x="Timeslot", y="BisectingKMeans_clusters",  text_auto=True,
                        category_orders={"Timeslot":timeslots_order,
                                         "BisectingKMeans_clusters":clusters_order},
                         color_continuous_scale='YlGn',
                         title="Bisecting K-Means"
                        )
            
fig.update_xaxes(title_text="")
fig.update_yaxes(title_text="Cluster")

st.plotly_chart(fig, use_container_width=True)

#K-Modes

fig = px.density_heatmap(db, x="Timeslot", y="KModes_clusters",  text_auto=True,
                        category_orders={"Timeslot":timeslots_order,
                                         "KMeans_clusters":clusters_order},
                         color_continuous_scale='YlGn',
                         title="K-Modes"
                        )
            
fig.update_xaxes(title_text="")
fig.update_yaxes(title_text="Cluster")

st.plotly_chart(fig, use_container_width=True)

#DBSCAN

fig = px.density_heatmap(db, x="Timeslot", y="DBSCAN_clusters",  text_auto=True,
                        category_orders={"Timeslot":timeslots_order,
                                          "DBSCAN_clusters": ["outlier", "6", "5", "4", "3", "2", "1", "0"]
                                         },
                         color_continuous_scale='YlGn',
                         title="DBSCAN"
                        )

fig.update_xaxes(title_text="")
fig.update_yaxes(title_text="Cluster")

st.write(fig, use_container_width=True)

###Graph 5####################################################################################################
st.subheader("Flow duration")

flow_duration_order=["Short", "Medium", "Long"]
#KMeans
fig = px.histogram(db, x="Flow.Duration_class",color="KMeans_clusters", text_auto=True,
                   labels={
                     "Flow.Duration_class": "Flow duration"
                   },
                   category_orders={"Flow.Duration_class":flow_duration_order,
                                    "KMeans_clusters":clusters_order},
                   color_discrete_map=clusters_palette,
                   title="K-Means"
)

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})

st.plotly_chart(fig, use_container_width=True)

#Bisecting KMeans
fig = px.histogram(db, x="Flow.Duration_class",color="BisectingKMeans_clusters", text_auto=True,
                   labels={
                     "Flow.Duration_class": "Flow duration"
                   },
                   category_orders={"Flow.Duration_class":flow_duration_order,
                                    "BisectingKMeans_clusters":clusters_order},
                   color_discrete_map=clusters_palette,
                   title="Bisecting K-Means"
)

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})

st.plotly_chart(fig, use_container_width=True)

#KModes
fig = px.histogram(db, x="Flow.Duration_class",color="KModes_clusters", text_auto=True,
                   labels={
                     "Flow.Duration_class": "Flow duration"
                   },
                   category_orders={"Flow.Duration_class":flow_duration_order,
                                    "KModes_clusters":clusters_order},
                   color_discrete_map=clusters_palette,
                   title="K-Modes"
)

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})

st.plotly_chart(fig, use_container_width=True)

#DBSCAN
fig = px.histogram(db, x="Flow.Duration_class",color="DBSCAN_clusters", text_auto=True,
                   labels={
                     "Flow.Duration_class": "Flow duration"
                   },
                   category_orders={"Flow.Duration_class":flow_duration_order,
                                    "DBSCAN_clusters":clusters_order},
                   color_discrete_map=clusters_palette,
                   title="DBSCAN"
)

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})

st.plotly_chart(fig, use_container_width=True)

###Graph 6####################################################################################################
st.subheader("Maximum time between two packets sent in the flow")

IATMax_order = ["[0-20]","[20-40]", "[40-80]", "[80-100]", "[80-120 000]"]

#KMeans

fig = px.histogram(db, x="FlowIATMax_bins",color="KMeans_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"FlowIATMax_bins":IATMax_order,
                                    "KMeans_clusters":clusters_order },
                   labels={
                     "FlowIATMax_bins": "Max IAT(ms)"
                   },
                    color_discrete_map=clusters_palette,
                   title="K-Means")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#Bisecting KMeans

fig = px.histogram(db, x="FlowIATMax_bins",color="BisectingKMeans_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"FlowIATMax_bins":IATMax_order,
                                    "BisectingKMeans_clusters":clusters_order },
                   labels={
                     "FlowIATMax_bins": "Max IAT(ms)"
                   },
                    color_discrete_map=clusters_palette,
                   title="Bisecting K-Means")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#KModes

fig = px.histogram(db, x="FlowIATMax_bins",color="KModes_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"FlowIATMax_bins":IATMax_order,
                                    "KModes_clusters":clusters_order },
                   labels={
                     "FlowIATMax_bins": "Max IAT(ms)"
                   },
                    color_discrete_map=clusters_palette,
                   title="K-Modes")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#DBSCAN

fig = px.histogram(db, x="FlowIATMax_bins",color="DBSCAN_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"FlowIATMax_bins":IATMax_order,
                                    "DBSCAN_clusters":clusters_order },
                   labels={
                     "FlowIATMax_bins": "Max IAT(ms)"
                   },
                    color_discrete_map=clusters_palette,
                   title="DBSCAN")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

###Graph 7####################################################################################################
st.subheader("Maximum backwards packet lenght")

BwdPacketLengthMax_order = ["<=753", "]753-3765]", ">3765"]

#KMeans

fig = px.histogram(db, x="Bwd.Packet.Length.Max_bins",color="KMeans_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Bwd.Packet.Length.Max_bins":BwdPacketLengthMax_order,
                                    "KMeans_clusters":clusters_order },
                   labels={
                     "Bwd.Packet.Length.Max_bins": "Max Bwd Packet Lenght"
                   },
                    color_discrete_map=clusters_palette,
                   title="K-Means")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#Bisecting KMeans

fig = px.histogram(db, x="Bwd.Packet.Length.Max_bins",color="BisectingKMeans_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Bwd.Packet.Length.Max_bins":BwdPacketLengthMax_order,
                                    "BisectingKMeans_clusters":clusters_order },
                   labels={
                     "Bwd.Packet.Length.Max_bins": "Max Bwd Packet Lenght"
                   },
                    color_discrete_map=clusters_palette,
                   title="Bisecting K-Means")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#KModes

fig = px.histogram(db, x="Bwd.Packet.Length.Max_bins",color="KModes_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Bwd.Packet.Length.Max_bins":BwdPacketLengthMax_order,
                                    "KModes_clusters":clusters_order },
                   labels={
                     "Bwd.Packet.Length.Max_bins": "Max Bwd Packet Lenght"
                   },
                    color_discrete_map=clusters_palette,
                   title="K-Modes")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#DBSCAN
fig = px.histogram(db, x="Bwd.Packet.Length.Max_bins",color="DBSCAN_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Bwd.Packet.Length.Max_bins":BwdPacketLengthMax_order,
                                    "DBSCAN_clusters":clusters_order },
                   labels={
                     "Bwd.Packet.Length.Max_bins": "Max Bwd Packet Lenght"
                   },
                    color_discrete_map=clusters_palette,
                   title="DBSCAN")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)


###Graph 8####################################################################################################
st.subheader("Maximum forward packet lenght")

FwdPacketLengthMax_order = ["<=657", "]657-3940]", ">3940"]

#KMeans

fig = px.histogram(db, x="Fwd.Packet.Length.Max_bins",color="KMeans_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Fwd.Packet.Length.Max_bins":FwdPacketLengthMax_order,
                                    "KMeans_clusters":clusters_order },
                   labels={
                     "Fwd.Packet.Length.Max_bins": "Max Fwd Packet Lenght"
                   },
                    color_discrete_map=clusters_palette,
                   title="K-Means")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#Bisecting KMeans

fig = px.histogram(db, x="Fwd.Packet.Length.Max_bins",color="BisectingKMeans_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Fwd.Packet.Length.Max_bins":FwdPacketLengthMax_order,
                                    "KMeans_clusters":clusters_order },
                   labels={
                     "Fwd.Packet.Length.Max_bins": "Max Fwd Packet Lenght"
                   },
                    color_discrete_map=clusters_palette,
                   title="Bisecting K-Means")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#KModes

fig = px.histogram(db, x="Fwd.Packet.Length.Max_bins",color="KModes_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Fwd.Packet.Length.Max_bins":FwdPacketLengthMax_order,
                                    "KModes_clusters":clusters_order },
                   labels={
                     "Fwd.Packet.Length.Max_bins": "Max Fwd Packet Lenght"
                   },
                    color_discrete_map=clusters_palette,
                   title="K-Modes")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#DBSCAN

fig = px.histogram(db, x="Fwd.Packet.Length.Max_bins",color="DBSCAN_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Fwd.Packet.Length.Max_bins":FwdPacketLengthMax_order,
                                    "DBSCAN_clusters":clusters_order },
                   labels={
                     "Fwd.Packet.Length.Max_bins": "Max Fwd Packet Lenght"
                   },
                    color_discrete_map=clusters_palette,
                   title="DBSCAN")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

###Graph 9####################################################################################################
st.subheader("The total number of bytes sent in initial window in the backward direction")

InitWinbytesbackward_order = ["<=1310", "]1310-5242]", ">5242"]

#KMeans

fig = px.histogram(db, x="Init_Win_bytes_backward_bins",color="KMeans_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Init_Win_bytes_backward_bins":InitWinbytesbackward_order,
                                    "KMeans_clusters":clusters_order },
                   labels={
                     "Init_Win_bytes_backward_bins": "Bytes"
                   },
                    color_discrete_map=clusters_palette,
                   title="K-Means")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#Bisecting KMeans

fig = px.histogram(db, x="Init_Win_bytes_backward_bins",color="BisectingKMeans_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Init_Win_bytes_backward_bins":InitWinbytesbackward_order,
                                    "BisectingKMeans_clusters":clusters_order },
                   labels={
                     "Init_Win_bytes_backward_bins": "Bytes"
                   },
                    color_discrete_map=clusters_palette,
                   title="Bisecting K-Means")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#KModes

fig = px.histogram(db, x="Init_Win_bytes_backward_bins",color="KModes_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Init_Win_bytes_backward_bins":InitWinbytesbackward_order,
                                    "KModes_clusters":clusters_order },
                   labels={
                     "Init_Win_bytes_backward_bins": "Bytes"
                   },
                    color_discrete_map=clusters_palette,
                   title="K-Modes")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#DBSCAN

fig = px.histogram(db, x="Init_Win_bytes_backward_bins",color="DBSCAN_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Init_Win_bytes_backward_bins":InitWinbytesbackward_order,
                                    "DBSCAN_clusters":clusters_order },
                   labels={
                     "Init_Win_bytes_backward_bins": "Bytes"
                   },
                    color_discrete_map=clusters_palette,
                   title="DBSCAN")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)


###Graph 9####################################################################################################
st.subheader("The total number of bytes sent in initial window in the forward direction")

InitWinbytesforward_order = ["<=1310", "]1310-6553]", ">6553"]

#KMeans

fig = px.histogram(db, x="Init_Win_bytes_forward_bins",color="KMeans_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Init_Win_bytes_forward_bins":InitWinbytesforward_order,
                                    "KMeans_clusters":clusters_order },
                   labels={
                     "Init_Win_bytes_forward_bins": "Bytes"
                   },
                    color_discrete_map=clusters_palette,
                   title="K-Means")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#Bisecting KMeans

fig = px.histogram(db, x="Init_Win_bytes_forward_bins",color="BisectingKMeans_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Init_Win_bytes_forward_bins":InitWinbytesforward_order,
                                    "BisectingKMeans_clusters":clusters_order },
                   labels={
                     "Init_Win_bytes_forward_bins": "Bytes"
                   },
                    color_discrete_map=clusters_palette,
                   title="Bisecting K-Means")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#KModes

fig = px.histogram(db, x="Init_Win_bytes_forward_bins",color="KModes_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Init_Win_bytes_forward_bins":InitWinbytesforward_order,
                                    "KModes_clusters":clusters_order },
                   labels={
                     "Init_Win_bytes_forward_bins": "Bytes"
                   },
                    color_discrete_map=clusters_palette,
                   title="K-Modes")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)

#DBSCAN

fig = px.histogram(db, x="Init_Win_bytes_forward_bins",color="DBSCAN_clusters", 
                    barmode="relative", text_auto=True,
                   category_orders={"Init_Win_bytes_forward_bins":InitWinbytesforward_order,
                                    "DBSCAN_clusters":clusters_order },
                   labels={
                     "Init_Win_bytes_forward_bins": "Bytes"
                   },
                    color_discrete_map=clusters_palette,
                   title="DBSCAN")

fig.update_yaxes(title_text="Number of flows")
fig.update_layout(legend={'title_text':''})
st.plotly_chart(fig, use_container_width=True)