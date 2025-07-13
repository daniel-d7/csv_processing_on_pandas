import urllib.request

import pandas as pd

response = urllib.request.urlretrieve(
    "https://raw.githubusercontent.com/yinghaoz1/tmdb-movie-dataset-analysis/master/tmdb-movies.csv",
    "raw.csv",
)

data_frame = pd.read_csv("raw.csv")

# Sắp xếp các bộ phim theo ngày phát hành giảm dần rồi lưu ra một file mới
sorted = data_frame.sort_values(by="release_date", ascending=False)
sorted.to_csv("./output/sorted_tmdb-movies.csv")

# Lọc ra các bộ phim có đánh giá trung bình trên 7.5 rồi lưu ra một file mới
over75 = data_frame[data_frame["vote_average"] > 7.5]
over75.to_csv("./output/over_7_5_tmdb-movies.csv")

# Tìm ra phim nào có doanh thu cao nhất và doanh thu thấp nhất
max_revenue_movie = data_frame[
    data_frame["revenue_adj"] == data_frame["revenue_adj"].max()
]

min_revenue_movie = data_frame[
    data_frame["revenue_adj"] == data_frame["revenue_adj"].min()
]

# Tính tổng doanh thu tất cả các bộ phim
total_revenue = data_frame["revenue_adj"].sum()

# Top 10 bộ phim đem về lợi nhuận cao nhất
data_frame["profit"] = data_frame["revenue_adj"] - data_frame["budget_adj"]
top10_profit = data_frame.nlargest(10, "profit")

# Đạo diễn nào có nhiều bộ phim nhất và diễn viên nào đóng nhiều phim nhất
top_director = data_frame["director"].value_counts().idxmax()
movie_count = data_frame["director"].value_counts().max()

data_frame["cast"] = data_frame["cast"].str.split("|")
cast_normalized = data_frame.explode("cast")

top_cast = data_frame["cast"].value_counts().idxmax()
cast_movie_count = data_frame["cast"].value_counts().max()

# Thống kê số lượng phim theo các thể loại. Ví dụ có bao nhiêu phim thuộc thể loại Action, bao nhiêu thuộc thể loại Family, ….
data_frame["genres"] = data_frame["genres"].str.split("|")
genres_normalized = data_frame.explode("genres")
pivot = pd.pivot_table(
    genres_normalized, index="genres", values="original_title", aggfunc="nunique"
)
