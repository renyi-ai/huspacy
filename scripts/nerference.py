import spacy
from huspacy import components

# import hu_core_news_trf
# nlp = hu_core_news_trf.load()
model_name = "/storage/huspacy/hu_core_news_trf/models/hu_core_news_trf-3.7.0"
nlp = spacy.load(model_name)

# nlp = load_pipeline(use_gpu=False, with_ner=True, model_name=model_name)
nlp.add_pipe("conll_formatter")

def get_ner(ocr_text):
    def clean_text(text):
        text = text.replace('\n', ' ')
        return text

    doc = nlp(ocr_text)

    persons = ";".join([str(ent.text) for ent in doc.ents if ent.label_=="PER"])
    organizations = ";".join([str(ent.text) for ent in doc.ents if ent.label_=="ORG"])
    locations = ";".join([str(ent.text) for ent in doc.ents if ent.label_=="LOC"])
    miscs = ";".join([str(ent.text) for ent in doc.ents if ent.label_=="MISC"])

    return clean_text(persons), clean_text(organizations), clean_text(locations), clean_text(miscs)

if __name__ == "__main__":
    ocr_text = "Péter Orbán a Magyar Nemzeti Bank elnöke. A Magyar Nemzeti Bank egy pénzügyi szervezet."
    persons, organizations, locations, miscs = get_ner(ocr_text)
    print(f"Persons: {persons}")
    print(f"Organizations: {organizations}")
    print(f"Locations: {locations}")
    print(f"Miscs: {miscs}")