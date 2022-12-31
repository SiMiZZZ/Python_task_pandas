import pandas as pd
from datetime import datetime
from fpdf import FPDF

def make_salary_by_cities(df):
    return df.groupby(['area_name'])[["salary"]].mean().apply(lambda x: round(x))\
        .sort_values(by="salary", ascending=False).head(10).to_dict()['salary']


def vacancies_share_by_cities(df):
    shares = df.groupby(['area_name']).apply(lambda x: len(x)/len(df))
    return shares[shares > 0.01].apply(lambda x: round(x, 3))\
        .sort_values(ascending=False).head(10).to_dict()


def make_salary_by_area_name(df, profession_name, area_name):
    data_dict = df[(df['name'].str.contains(profession_name)) & (df["area_name"] == area_name)]\
        .groupby(['published_at'])\
        .mean().apply(lambda x: round(x, 3)).to_dict()['salary']
    return dict(sorted(data_dict.items()))


def make_quantity_by_area_name(df, profession_name, area_name):
    data_dict =  df[(df['name'].str.contains(profession_name)) & (df["area_name"] == area_name)]\
        .published_at.value_counts().to_dict()
    return dict(sorted(data_dict.items()))


def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 8)
    for i, row in enumerate(text.split("\n")):
        pdf.multi_cell(200, 10, txt=row, align="с")
    pdf.output("result_3.4.3.pdf")


file_name = input("Введите название файла: ")
profession_name = input("Введите название професии: ")
country_name = input("Введите название региона: ")

df = pd.read_csv(file_name)
df.published_at = df.published_at.apply(lambda x: str(x)[:str(x).find("-")])
output_text =\
f"""
Уровень зарплат по городам: {make_salary_by_cities(df)}\n
Динамика количества вакансий по годам : {vacancies_share_by_cities(df)}\n
Динамика уровня зарплат по годам для выбранной профессии: {make_salary_by_area_name(df, profession_name, country_name)}\n
Динамика количества вакансий по годам для выбранной профессии: {make_quantity_by_area_name(df, profession_name, country_name)}
"""
create_pdf(output_text)
print(output_text)