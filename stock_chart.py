import streamlit as st
import altair as alt
import pandas as pd


class StockAltairChart:
    def __init__(self, data, x, y, color=None, title=None):
        self.data = data
        self.x = x
        self.y = y
        self.color = color
        self.title = title

    def create_chart(self):
        ymin = self.data[self.y].min()
        ymax = self.data[self.y].max()
        chart = (
            alt.Chart(self.data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x=alt.X(f"{self.x}:T"),
                y=alt.Y(f"{self.y}:Q", stack=None,
                        scale=alt.Scale(domain=[ymin, ymax])),
                color=alt.Color(f"{self.color}:N", scale=alt.Scale(
                    scheme='category10')) if self.color else None
            )
            .configure_axis(
                gridOpacity=0.8,
            )
            .configure_legend(
                titleFontSize=12,
                labelFontSize=11,
                symbolType="circle",
                symbolSize=100,
                padding=5,
                cornerRadius=5,
            )
        )
        if self.title:
            chart = chart.properties(title=alt.TitleParams(text=self.title))
        return chart

    def display_chart(self):
        chart = self.create_chart()
        st.altair_chart(chart.interactive(), use_container_width=True)


class StockAltairChartSimple:
    def __init__(self):
        self.charts = []

    def add_chart(self, subset, stock_symbol):
        chart = alt.Chart(subset).mark_line().encode(
            x='asOfDate',
            y=alt.Y(stock_symbol, scale=alt.Scale(
                domain=[subset[stock_symbol].min()-0.1, subset[stock_symbol].max()+0.1])),
            color=alt.Color('symbol:N', scale=alt.Scale(scheme='category10')),
            tooltip=['symbol', 'asOfDate', stock_symbol],  # ツールチップに表示する列を指定
        )

        self.charts.append(chart)

    def display_chart(self):
        st.altair_chart(alt.layer(*self.charts), use_container_width=True)
