import streamlit as st
import pandas as pd
import graphviz

def app():
    st.title("Graphviz Chart App")
    
    # Load previous graph data if available
    if 'graph_data' not in st.session_state:
        st.session_state['graph_data'] = []
    graph_data = st.session_state['graph_data']
    
    # Load previous dataframe if available
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame(columns=['value1', 'value2', "is_widget"])
    df = st.session_state['df']
    
    # Create input text boxes for the two words
    word1 = st.text_input("Enter word 1:")
    word2 = st.text_input("Enter word 2:")
    
    # Create a button to add the new edge to the graph
    if st.button("Add Edge"):
        # Create a new edge and add it to the graph
        new_edge = (word1, word2)
        graph_data.append(new_edge)
        
        # Add new data to the dataframe
        new_data = {'value1': word1, 'value2': word2, 'is_widget': False}
        df = df.append(new_data, ignore_index=True)
        st.session_state['df'] = df
    
    # Create a checkbox to delete rows
    if st.checkbox("Delete Rows"):
        # Identify rows to delete
        rows_to_delete = df[df['is_widget'] == True].index
        # Delete rows
        df.drop(rows_to_delete, inplace=True)
        # Update session state
        st.session_state['df'] = df
    
    # Create a checkbox column in the dataframe
    is_widget = st.checkbox("Delete?")
    df['is_widget'] = is_widget
    
    # Create a Graphviz chart to display the graph
    graph = graphviz.Digraph()
    for edge in graph_data:
        graph.edge(edge[0], edge[1])
    st.graphviz_chart(graph)
    
    # Display the dataframe
    st.dataframe(df)
        
app()