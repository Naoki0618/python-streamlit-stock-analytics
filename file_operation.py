class FileOperation():

    def remove_all_zero_col(df):
        """全て0の列を削除"""
        df = df.copy()
        for col in df.columns:
            if (df[col] == 0).all():
                df.drop(col, axis=1, inplace=True)
        return df
