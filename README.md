# PedestriansDET: Sistema di Detection e Conteggio dei pedoni

Questo progetto documenta la progettazione, l’addestramento e la valutazione di modelli di **Object Detection** per il riconoscimento e il conteggio di persone in immagini e video. Sono stati utilizzati sia approcci *single-stage* (YOLO) che *two-stage* (Faster R-CNN), e tutte le fasi di sviluppo sono state condotte interamente su **[Kaggle]([https://www.kaggle.com/](https://www.kaggle.com/code/denisecilia/demo-for-machine-learning-project))**.

## 1. Obiettivo
Sviluppare un sistema accurato ed efficiente per la **rilevazione e il conteggio di pedoni**, sfruttando i seguenti modelli:
- YOLOv8m
- YOLOv10n
- YOLOv11s
- Faster R-CNN con backbone ResNet50

Il conteggio delle persone è stato effettuato in modo frame-by-frame a partire dalle bounding box prodotte dai modelli.

## 2. Sviluppo su Kaggle
L’intero progetto è stato realizzato utilizzando l’ambiente di **Kaggle**, approfittando di:
- GPU NVIDIA Tesla P100 gratuite
- Accesso diretto a dataset, storage e output file
- Notebook interattivi per training, validazione e inferenza
- Rendering video e immagini per demo e visualizzazione dei risultati

Il progetto è **completamente riproducibile su Kaggle**: ogni notebook carica dataset, modelli e produce risultati visivi senza necessità di configurazioni locali.

## 3. Dataset
- Dataset annotato manualmente e formattato sia per YOLO (TXT) che COCO (JSON)
- Strutturato in `train/`, `val/`, `test/` per immagini e annotazioni
- Contiene esclusivamente la classe "persona"

## 4. Modelli testati
| Model           | Precision  | Recall  | mAP50  | mAP50-95 | Fitness |
|-----------------|------------|---------|--------|----------|---------|
| YOLOv8m         | 0.8965     | 0.5368  | 0.6555 | 0.3276   | 0.3604  |
| YOLOv11s        | 0.8035     | 0.5594  | 0.6463 | 0.3333   | 0.3646  |
| YOLOv10n        | 0.8437     | 0.4830  | 0.5871 | 0.2981   | 0.3270  |
| Faster R-CNN    | 0.7956     | 0.7435  | —      | —        | —       |

## 5. Risultati e considerazioni
- **YOLOv8m** eccelle in precisione, ideale per ambienti real-time ad alta affidabilità
- **YOLOv11s** è il miglior compromesso tra accuratezza e leggerezza
- **YOLOv10n** è pensato per dispositivi con risorse limitate
- **Faster R-CNN** ha ottenuto la recall più elevata (0.74), ottimo per applicazioni di **people counting** in ambienti critici

## 6. Conteggio Persone (People Counting)
Implementato attraverso somma delle bounding box nei singoli frame. Anche senza tracking multi-oggetto, il metodo ha fornito una valutazione realistica dei flussi pedonali. I modelli con recall più alta si sono rivelati più adatti a questo task.

## 7. Prospettive Future
- Integrazione con algoritmi di tracking (es. DeepSORT)
- Aumento del dataset e diversificazione dei contesti
- Miglioramento delle performance su dispositivi embedded
- Adozione di architetture Transformer-based per object detection
- Potenziamento dei modelli YOLO tramite ottimizzazione post-training


