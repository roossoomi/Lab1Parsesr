import os
import json
from lxml import html
import re
import logging

logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
data = {}

for index, filename in enumerate(os.listdir("html_files")):
    if filename.endswith('.html'):
        with open(os.path.join("html_files", filename), 'r', encoding='utf-8') as file:
            content = file.read()
            htm_pars = html.fromstring(content)

            author = htm_pars.xpath('string(//span[contains(@class, "thumbnail ml-2")]/preceding-sibling::text())')
            grams_protein = htm_pars.xpath('string(//span[@id="nutr_p"])')
            percent_protein = htm_pars.xpath('string(//div[@class="graph-item-wrap proteins"]//span[@id="nutr_ratio_p"])')
            grams_carb = htm_pars.xpath('string(//span[@id="nutr_c"])')
            percent_carb = htm_pars.xpath('string(//div[@class="graph-item-wrap carbs"]//span[@id="nutr_ratio_c"])')
            grams_fat = htm_pars.xpath('string(//span[@id="nutr_f"])')
            percent_fat = htm_pars.xpath('string(//div[@class="graph-item-wrap fats"]//span[@id="nutr_ratio_f"])')
            calories = htm_pars.xpath('string(//span[@id="nutr_kcal"])')
            low_carb = htm_pars.xpath('string(//strong[@title="Низкие углеводы"])')
            medium_carb = htm_pars.xpath('string(//strong[@title="Средние углеводы"])')
            high_carb = htm_pars.xpath('string(//strong[@title="Высокие углеводы"])')
            dish_name = htm_pars.xpath('string(//h1[@itemprop="name"])')
            total_time = htm_pars.xpath('string(//span[contains(text(), "Общее время приготовления")]/strong)')

            steps = htm_pars.xpath('//h4[contains(text(), "Шаг")]/text()')
            if steps:
                max_steps = max(int(re.findall(r'\d+', step)[0]) for step in steps)
            else:
                max_steps = None

            dictionary = {
                'dish_name': dish_name,
                'author': author,
                'grams_protein': grams_protein,
                'percent_protein': percent_protein,
                'grams_carb': grams_carb,
                'percent_carb': percent_carb,
                'grams_fat': grams_fat,
                'percent_fat': percent_fat,
                'calories': calories,
                'low_carb': low_carb,
                'medium_carb': medium_carb,
                'high_carb': high_carb,
                'total_time': total_time,
                'number_of_steps': max_steps,
            }

            data[index+1] = dictionary

with open('parametrs.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Данные успешно собраны и сохранены в parametrs.json")
