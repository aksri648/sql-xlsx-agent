import pandas as pd
import chardet
from typing import Optional
import io


class FileHandler:
    @staticmethod
    def detect_encoding(file_content: bytes) -> str:
        result = chardet.detect(file_content)
        return result.get("encoding", "utf-8")

    @staticmethod
    def read_csv(file_path: str, delimiter: Optional[str] = None) -> pd.DataFrame:
        with open(file_path, "rb") as f:
            raw_content = f.read()
            encoding = FileHandler.detect_encoding(raw_content)

        if delimiter is None:
            sample = raw_content[:4096].decode(encoding, errors="replace")
            potential_delimiters = [",", ";", "\t", "|"]
            delimiter_counts = {}
            for d in potential_delimiters:
                delimiter_counts[d] = sample.count(d)

            if delimiter_counts:
                delimiter = max(delimiter_counts, key=delimiter_counts.get)
            else:
                delimiter = ","

        df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
        return df

    @staticmethod
    def read_excel(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
        else:
            df = pd.read_excel(file_path, sheet_name=0, engine="openpyxl")
        return df

    @staticmethod
    def get_schema(df: pd.DataFrame) -> dict:
        columns = []
        for col in df.columns:
            col_info = {
                "name": col,
                "dtype": str(df[col].dtype),
                "null_count": int(df[col].isnull().sum()),
                "unique_count": int(df[col].nunique()),
                "sample_values": df[col].head(5).tolist(),
            }
            if pd.api.types.is_numeric_dtype(df[col]):
                col_info["min"] = float(df[col].min()) if not pd.isna(df[col].min()) else None
                col_info["max"] = float(df[col].max()) if not pd.isna(df[col].max()) else None
                col_info["mean"] = float(df[col].mean()) if not pd.isna(df[col].mean()) else None
            columns.append(col_info)

        return {
            "columns": columns,
            "row_count": len(df),
            "column_count": len(df.columns),
        }

    @staticmethod
    def profile_dataset(df: pd.DataFrame) -> dict:
        return {
            "schema": FileHandler.get_schema(df),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "memory_usage": int(df.memory_usage(deep=True).sum()),
            "has_missing": bool(df.isnull().any().any()),
        }