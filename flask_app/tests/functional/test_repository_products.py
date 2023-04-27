
#TODO: To nie dziala, napisac inne test
# def test_products_repository(app):
#     repo = ProductsRepository.SqlAlchemyRepository(db.session)
#     new_product = Products(name="jakub", category="czlowiek")
#     repo.add(new_product)

#     var = repo.get()
#     assert var.name == "jakub"
#     assert var.category == "czlowiek"


# def test_products_repository_get_by_id(app):
#     repo = ProductsRepository.SqlAlchemyRepository(db.session)
#     new_product = Products(name="jakub", category="czlowiek")
#     repo.add(new_product)

#     var = repo.get_by_id("1")
#     assert var.id == 1
#     assert var.name == "jakub"
#     assert var.category == "czlowiek"


# def test_reviews_repository(app):
#     repo_prod = ProductsRepository.SqlAlchemyRepository(db.session)
#     new_product = Products(name="jakub", category="czlowiek")
#     repo_prod.add(new_product)
#     var = repo_prod.get_by_id(1)

#     assert var.name == "jakub"

#     repo_rev = ReviewsRepository.SqlAlchemyRepository(db.session)
#     new_reviews = [
#         Reviews(name="opisujacy01", stars="5", parent=new_product),
#         Reviews(name="opisujacy02", stars="1", parent=new_product),
#         Reviews(name="opisujacy03", stars="2", parent=new_product),
#         Reviews(name="opisujacy04", stars="4", parent=new_product),
#     ]

#     repo_rev.add_all(new_reviews)

#     var = repo_prod.get_by_name("jakub")
#     assert var.name == "jakub"
#     assert var.children[0].name == "opisujacy01"
#     assert var.children[3].name == "opisujacy04"
#     assert [True for x in var.children if "opisujacy03" in x.name]
