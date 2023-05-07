import streamlit as st
import pandas as pd

class FavoriteManager():
    # 1. CSVファイルからお気に入り情報を読み込む
    @classmethod
    def load_favorites(self, file_path):
        df = pd.read_csv(file_path)
        return df

    # 2. お気に入り情報をパースして必要な情報を取得する
    @classmethod
    def parse_favorites(self, df):
        favorites = {}
        for index, row in df.iterrows():
            if row["Favorite Name"] not in favorites:
                favorites[row["Favorite Name"]] = []
            favorites[row["Favorite Name"]].append(str(row["Security Code"]))
        return favorites

    # 3. お気に入り情報を更新するための関数
    @classmethod
    def update_favorites(self, favorites, file_path):
        favorite_names = []
        security_codes = []
        for name, codes in favorites.items():
            for code in codes:
                favorite_names.append(name)
                security_codes.append(str(code))
        df = pd.DataFrame({
            "Favorite Name": favorite_names,
            "Security Code": security_codes
        })
        df.to_csv(file_path, index=False)

    # 4. ユーザーがお気に入りを追加、更新、削除するための関数
    @classmethod
    def edit_favorites(self, favorites):
        favorite_name = st.text_input("お気に入りの名前を入力してください", key='favorite_name_input')
        if not favorite_name:
            return favorites
        security_code = st.text_input("Ticker Codeを入力してください", key='ticker_input')
        if not security_code:
            return favorites
        if favorite_name not in favorites:
            favorites[favorite_name] = []
            favorites[favorite_name].append(str(security_code))
        else:
            if security_code not in favorites[favorite_name]:
                favorites[favorite_name].append(str(security_code))
                
        st.write("Favorites:", favorites)
        return favorites

    # 5. お気に入りを呼び出すための関数
    @classmethod
    def select_favorites(self, favorites):
        if favorites != None:
            favorite_names = list(favorites.keys())
            selected_names = st.multiselect("お気に入りリストを選択して下さい", favorite_names, key="selected_names")
            selected_codes = []
            for name in selected_names:
                selected_codes.extend(favorites[name])
            return selected_codes

