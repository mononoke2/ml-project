import json
from pathlib import Path

def convert_annotations_inplace(json_file):
    # Leggi il file JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # ID delle categorie da eliminare e convertire
    categories_to_remove = {2, 3, 4, 6, 7, 8}
    categories_to_convert = {5, 9}
    
    # Statistiche iniziali
    original_annotations = len(data['annotations'])

    # 1. Filtra e converti le annotazioni
    filtered_annotations = []
    for annotation in data['annotations']:
        category_id = annotation['category_id']
        
        # Salta le annotazioni da eliminare
        if category_id in categories_to_remove:
            continue
        
        # Converti category_id 5 e 9 in 1
        if category_id in categories_to_convert:
            annotation['category_id'] = 1
        
        filtered_annotations.append(annotation)
    
    data['annotations'] = filtered_annotations
    
    # 2. Aggiorna le categorie
    new_categories = []
    for category in data['categories']:
        cat_id = category['id']
        
        # Salta le categorie da rimuovere
        if cat_id in categories_to_remove:
            continue
        
        # Aggiorna la categoria 1 per riflettere la fusione
        if cat_id == 1:
            category['name'] = "pedestrian"
            category['supercategory'] = "pedestrians-"
        
        # Mantieni solo le categorie necessarie
        if cat_id in {0, 1}:
            new_categories.append(category)
    
    data['categories'] = new_categories
    
    
    # Salva il file modificato
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Statistiche finali
    print(f"  Annotazioni: {original_annotations} -> {len(data['annotations'])}")
    print(f"  Categorie: {len(new_categories)}")

def main():
    base_dir = Path(__file__).parent
    
    # Trova tutti i file di annotazioni
    annotation_files = list(base_dir.glob('**/_annotations.coco.json'))
    
    if not annotation_files:
        print("Nessun file di annotazioni trovato")
        return
    
    print(f"\nTrovati {len(annotation_files)} file di annotazioni:")
    for file in annotation_files:
        print(f"  - {file.relative_to(base_dir)}")
    
    print("\nInizio conversione...")
    
    # Converti ogni file
    for json_file in annotation_files:
        convert_annotations_inplace(json_file)
    
    print(f"\n=== Conversione completata ===")
    
    # Mostra un riepilogo delle categorie finali
    if annotation_files:
        sample_file = annotation_files[0]
        with open(sample_file, 'r') as f:
            data = json.load(f)
        
        print(f"\nCategorie finali (esempio da {sample_file.name}):")
        for category in data['categories']:
            print(f"  ID {category['id']}: {category['name']}")

if __name__ == "__main__":
    main()
