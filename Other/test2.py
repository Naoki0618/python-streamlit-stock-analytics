import streamlit as st

class TextInput:
    instances = {}

    def __new__(cls, label):
        if label not in cls.instances:
            instance = super().__new__(cls)
            instance.label = label
            instance.text_input = st.text_input(label, key=label)
            cls.instances[label] = instance
        return cls.instances[label]

    def render(self):
        if st.button('Submit', key=self.label+"_buton"):
            # ここにボタンがクリックされたときの処理を記述する
            st.write('You entered:', self.text_input)
