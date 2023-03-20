import os
import json
import requests
from bs4 import BeautifulSoup


# https://www.ceneo.pl/143471602

class QueryReviews:
    def __init__(self, product_id):
        self.product_id = product_id

    def get_reviews(self):
        self.operate()

        return self.all_reviews

    def extract_element(self, ancestor, selector, attribute=None, return_list=False):
        try:
            if attribute:
                return ancestor.select_one(selector)[attribute]
            elif return_list:
                return [item.text.strip() for item in ancestor.select(selector)]
            else:
                return ancestor.select_one(selector).text.strip()
        except (AttributeError, TypeError):
            return None

    def operate(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"

        self.all_reviews = []

        while url:
            response = requests.get(url)
            page_dom = BeautifulSoup(response.text, 'html.parser')
            reviews = page_dom.select("div.js_product-review")
            for review in reviews:
                single_review = {key: self.extract_element(review, *values)
                                 for key, values in self.review_elements.items()}
                single_review["review_id"] = review["data-entry-id"]

                single_review["recommendation"] = True if single_review["recommendation"] == "Polecam" else False if \
                    single_review["recommendation"] == "Nie polecam" else None
                single_review["stars"] = float(single_review["stars"].split("/").pop(0).replace(",", "."))
                single_review["useful"] = int(single_review["useful"])
                single_review["useless"] = int(single_review["useless"])
                single_review["publish_date"] = single_review["publish_date"].split(" ").pop(0) if single_review[
                                                                                                       "publish_date"] is not None else None
                single_review["purchase_date"] = single_review["purchase_date"].split(" ").pop(0) if single_review[
                                                                                                         "purchase_date"] is not None else None
                self.all_reviews.append(single_review)
            try:
                next_page = page_dom.select_one("a.pagination__next")
                url = "https://www.ceneo.pl" + next_page["href"]
            except TypeError:
                url = None

    review_elements = {
        "author": ["span.user-post__author-name"],
        "recommendation": ["span.user-post__author-recomendation > em"],
        "stars": ["span.user-post__score-count"],
        "content": ["div.user-post__text"],
        "publish_date": ["span.user-post__published > time:nth-child(1)", "datetime"],
        "purchase_date": ["span.user-post__published > time:nth-child(2)", "datetime"],
        "useful": ["button.vote-yes > span"],
        "useless": ["button.vote-no > span"],
        "pros": ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
        "cons": ["div.review-feature__title--negatives ~ div.review-feature__item", None, True]
    }