import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import deque
import time

class LiveTrafficMonitor:
    def __init__(self, max_points=100):
        self.timestamps = deque(maxlen=max_points)
        self.packet_counts = deque(maxlen=max_points)
        self.byte_counts = deque(maxlen=max_points)
    
    def add_data_point(self, packet_count, byte_count):
        self.timestamps.append(time.time())
        self.packet_counts.append(packet_count)
        self.byte_counts.append(byte_count)
    
    def render(self):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(self.timestamps),
            y=list(self.packet_counts),
            name='Packets/sec',
            line=dict(color='cyan', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=list(self.timestamps),
            y=list(self.byte_counts),
            name='Bytes/sec',
            line=dict(color='orange', width=2),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Live Traffic Monitor',
            xaxis_title='Time',
            yaxis_title='Packets/sec',
            yaxis2=dict(
                title='Bytes/sec',
                overlaying='y',
                side='right'
            ),
            template='plotly_dark',
            height=300
        )
        
        return fig