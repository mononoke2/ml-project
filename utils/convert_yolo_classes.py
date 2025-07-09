import sys
import os
import argparse
from pathlib import Path


def convert_yolo_annotations(input_file):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File non trovato: {input_file}")
    
    converted_lines = 0
    removed_lines = 0
    output_lines = []
    
    # Leggi il file di input
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        # Salta righe vuote
        if not line:
            continue
            
        # Dividi la riga in componenti
        parts = line.split()
        
        if len(parts) < 5:
            print(f"Attenzione: Riga {line_num} non ha il formato corretto (meno di 5 valori): {line}")
            continue
        
        try:
            class_id = int(parts[0])
        except ValueError:
            print(f"Attenzione: Riga {line_num} ha un ID classe non valido: {parts[0]}")
            continue
        
        # Applica le regole di conversione
        if class_id in [4, 8]:
            # Converte classe 4 e 8 -> classe 0
            parts[0] = '0'
            output_lines.append(' '.join(parts))
            converted_lines += 1
            
        elif class_id == 0:
            # Mantiene classe 0 invariata
            output_lines.append(line)
            
        elif class_id in [1, 2, 3, 5, 6, 7]:
            # Rimuove le righe con queste classi
            removed_lines += 1
            
        else:
            # Classe non riconosciuta - mantieni per sicurezza
            print(f"Attenzione: Riga {line_num} contiene classe non riconosciuta: {class_id}")
            output_lines.append(line)
    

    # Scrivi il file di output
    with open(input_file, 'w', encoding='utf-8') as f:
        for line in output_lines:
            f.write(line + '\n')
    
    return converted_lines, removed_lines


def process_directory(directory_path, recursive=False):
    directory = Path(directory_path)
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory non trovata: {directory_path}")
    
    # Trova tutti i file .txt
    if recursive:
        txt_files = list(directory.rglob("*.txt"))
    else:
        txt_files = list(directory.glob("*.txt"))
    
    if not txt_files:
        print(f"Nessun file .txt trovato in {directory_path}")
        return
    
    total_converted = 0
    total_removed = 0
    processed_files = 0
    
    for txt_file in txt_files:
        try:
            print(f"Processando: {txt_file}")
            converted, removed = convert_yolo_annotations(str(txt_file))
            
            total_converted += converted
            total_removed += removed
            processed_files += 1
            
            if converted > 0 or removed > 0:
                print(f"  - Convertite: {converted} righe (4,8->0)")
                print(f"  - Rimosse: {removed} righe (classi 1,2,3,5,6,7)")
            else:
                print(f"  - Nessuna modifica necessaria")
                
        except Exception as e:
            print(f"Errore processando {txt_file}: {e}")
    
    print(f"\n=== RIEPILOGO ===")
    print(f"File processati: {processed_files}")
    print(f"Totale righe convertite (4,8->0): {total_converted}")
    print(f"Totale righe rimosse (classi 1,2,3,5,6,7): {total_removed}")


def main():
    parser = argparse.ArgumentParser(
        description="Converte le classi nei file di annotazioni YOLO",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:
  python convert_yolo_classes.py --directory ./labels        # Processa tutti i .txt in ./labels
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--directory', '-d', help='Directory contenente i file da processare')

    args = parser.parse_args()
    
    try:
        if args.directory:
            # Modalità directory
            process_directory(args.directory)
    except Exception as e:
        print(f"Errore: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
