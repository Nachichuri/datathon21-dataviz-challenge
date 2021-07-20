from os import lseek
import plotly.io as pio

def get_flow_template():
    flow_template = pio.templates['plotly_dark']


    flow_template['layout'].update(
        plot_bgcolor='#333333',
        paper_bgcolor='#333333',
        colorway=['#57e0b6', '#00cbc6', '#00b3d6', '#0098df', '#007ad8', '#2d58c0'],
        hoverlabel = {'font': {'color': 'white'}, 'bgcolor': '#202020'},
        title_x=0.5
    )

    flow_template.layout.yaxis.gridcolor = '#202020'

    return flow_template