import pandas as pd
from datetime import datetime
from fpdf import FPDF

def make_salary_by_years(df):
    return df.groupby(['published_at'])[["salary"]].mean().apply(lambda x: round(x)).to_dict()['salary']


def make_quantity_by_years(df):
    return df.published_at.value_counts().to_dict()


def make_salary_by_profession(df, profession_name):
    data_dict = df[df['name'].str.contains(profession_name)]\
        .groupby(['published_at'])\
        .mean().to_dict()['salary']
    return dict(sorted(data_dict.items()))

def make_quantity_by_profession(df, profession_name):
    data_dict =  df[df['name'].str.contains(profession_name)]\
        .published_at.value_counts().to_dict()
    return dict(sorted(data_dict.items()))
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 8)
    for i, row in enumerate(text.split("\n")):
        pdf.multi_cell(200, 10, txt=row, align="с")
    pdf.output("result.pdf")


file_name = input("Введите название файла: ")
profession_name = input("Введите название професии: ")

df = pd.read_csv(file_name)
df.published_at = df.published_at.apply(lambda x: str(x)[:str(x).find("-")])
output_text =\
f"""
Динамика уровня зарплат по годам: {make_salary_by_years(df)}\n
Динамика количества вакансий по годам : {make_salary_by_years(df)}\n
Динамика уровня зарплат по годам для выбранной профессии: {make_quantity_by_profession(df, profession_name)}\n
Динамика количества вакансий по годам для выбранной профессии: {make_quantity_by_profession(df, profession_name)}
"""
create_pdf(output_text)
print(output_text)