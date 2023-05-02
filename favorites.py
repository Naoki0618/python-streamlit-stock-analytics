import streamlit as st
import pandas as pd

class favorite_manager():
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
            favorites[row["Favorite Name"]].append(row["Security Code"])
        return favorites

    # 3. お気に入り情報を更新するための関数
    @classmethod
    def update_favorites(self, favorites, file_path):
        favorite_names = []
        security_codes = []
        for name, codes in favorites.items():
            for code in codes:
                favorite_names.append(name)
                security_codes.append(code)
        df = pd.DataFrame({
            "Favorite Name": favorite_names,
            "Security Code": security_codes
        })
        df.to_csv(file_path, index=False)

    # 4. ユーザーがお気に入りを追加、更新、削除するための関数
    @classmethod
    def edit_favorites(self, favorites):
        favorite_name = st.text_input("お気に入りの名前を入力してください")
        if not favorite_name:
            return favorites
        security_code = st.text_input("Ticker Codeを入力してください")
        if not security_code:
            return favorites
        if favorite_name not in favorites:
            favorites[favorite_name] = []
            favorites[favorite_name].append(security_code)
        else:
            if int(security_code) not in favorites[favorite_name]:
                favorites[favorite_name].append(security_code)
                
        st.write("Favorites:", favorites)
        return favorites

    # 5. お気に入りを呼び出すための関数
    @classmethod
    def select_favorites(self, favorites):
        if favorites != None:
            favorite_names = list(favorites.keys())
            selected_names = st.multiselect("Select Favorites", favorite_names)
            selected_codes = []
            for name in selected_names:
                selected_codes.extend(favorites[name])
            return selected_codes


# アプリの実行部分
main, favorite = st.sidebar.tabs(["main", "favorite"])

with main:
    # mainタブの処理
    pass
with favorite:
    file_path = "C:/Users/tokyo/Documents/GitHub/Streamlit/favorites.csv"

    # 1. CSVファイルからお気に入り情報を読み込む
    favorite_manager_instance = favorite_manager()
    favorites_df = favorite_manager_instance.load_favorites(file_path)
    favorites = favorite_manager_instance.parse_favorites(favorites_df)

    # 2. お気に入り情報を編集する
    favorites = favorite_manager_instance.edit_favorites(favorites)

    if favorites != None:
        # 3. お気に入り情報を更新する
        favorite_manager_instance.update_favorites(favorites, file_path)

    # 4. お気に入りを呼び出す
    selected_codes = favorite_manager_instance.select_favorites(favorites)

    # 5. 結果を表示する
    st.write("Selected Securities:", selected_codes)
