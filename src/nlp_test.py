import sys
from conversation_smach.search import NLPProcessor


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        nlp_processor = NLPProcessor()
        response = nlp_processor.process_query(query)
        print(response)
    else:
        print("Por favor, proporcione un argumento para el prompt.")

